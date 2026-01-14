import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from config.enums import BusinessType, RedisInitKeyConfig
from config.env import AppConfig, JwtConfig
from config.get_db import get_db
from common.annotation.log_annotation import Log
from common.entity.vo.common_vo import CrudResponseModel
from common.entity.vo.login_vo import UserLogin, UserRegister, Token
from common.entity.vo.user_vo import CurrentUserModel, EditUserModel
from common.service.login_service import CustomOAuth2PasswordRequestForm, LoginService, oauth2_scheme
from common.service.user_service import UserService
from utils.log_util import logger
from utils.response_util import ResponseUtil


loginController = APIRouter(prefix='', tags=['前端登录'])


@loginController.post('/login', response_model=Token)
@Log(title='用户登录', business_type=BusinessType.OTHER, log_type='login')
async def login(
    request: Request, form_data: CustomOAuth2PasswordRequestForm = Depends(), query_db: AsyncSession = Depends(get_db)
):
    captcha_enabled = (
        True
        if await request.app.state.redis.get(f'{RedisInitKeyConfig.SYS_CONFIG.key}:sys.account.captchaEnabled')
        == 'true'
        else False
    )
    user = UserLogin(
        userName=form_data.username,
        password=form_data.password,
        code=form_data.code,
        uuid=form_data.uuid,
        loginInfo=form_data.login_info,
        captchaEnabled=captcha_enabled,
    )
    result = await LoginService.authenticate_user(request, query_db, user)
    access_token_expires = timedelta(minutes=JwtConfig.jwt_expire_minutes)
    refresh_token_expires = timedelta(days=JwtConfig.jwt_refresh_expires_days)

    session_id = str(uuid.uuid4())
    access_token = await LoginService.create_access_token(
        data={
            'user_id': str(result[0].user_id),
            'user_name': result[0].user_name,
            'dept_name': result[1].dept_name if result[1] else None,
            'session_id': session_id,
            'login_info': user.login_info,
            'token_type': 'access',
        },
        expires_delta=access_token_expires,
    )
    #刷新token
    refresh_token = await LoginService.create_access_token(
        data={
            'user_id': str(result[0].user_id),
            'token_type': 'refresh',
            'login_module': 'front',
        },
        expires_delta=refresh_token_expires,
    )

    if AppConfig.app_same_time_login:
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}',
            access_token,
            ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
        )
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}',
            refresh_token,
            ex=timedelta(days=JwtConfig.jwt_refresh_expires_days),
        )

    else:
        # 此方法可实现同一账号同一时间只能登录一次
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{result[0].user_id}',
            access_token,
            ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
        )
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.REFRESH_TOKEN.key}:{result[0].user_id}',
            refresh_token,
            ex=timedelta(days=JwtConfig.jwt_refresh_expires_days),
        )
    await UserService.edit_user_services(
        query_db, EditUserModel(userId=result[0].user_id, loginDate=datetime.now(), type='status')
    )
    logger.info('登录成功')

    return ResponseUtil.success(msg='登录成功', dict_content={
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    })


@loginController.post('/refresh_token', response_model=Token)
@Log(title='刷新令牌', business_type=BusinessType.OTHER, log_type='login')
async def refresh_token(request: Request, refresh_token: str):
    # 检查刷新 Token 是否在黑名单
    blacklist_key = f'{RedisInitKeyConfig.BLACKLIST_TOKEN.key}:{refresh_token}'
    if await request.app.state.redis.exists(blacklist_key):
        return ResponseUtil.failure(msg='刷新令牌已失效，请重新登录')

    try:
        payload = jwt.decode(refresh_token, JwtConfig.jwt_secret_key, algorithms=[JwtConfig.jwt_algorithm])
        if payload.get('token_type') != 'refresh':
            return ResponseUtil.failure(msg='无效的刷新令牌')
        user_id = payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return ResponseUtil.failure(msg='刷新令牌已过期，请重新登录')
    except Exception:
        return ResponseUtil.failure(msg='无效的刷新令牌')

    # 生成新的 Access Token
    access_token_expires = timedelta(minutes=JwtConfig.jwt_expire_minutes)
    session_id = str(uuid.uuid4())
    new_access_token = await LoginService.create_access_token(
        data={
            'user_id': user_id,
            'session_id': session_id,
            'token_type': 'access'
        },
        expires_delta=access_token_expires,
    )

    # 存储新的 Access Token
    await request.app.state.redis.set(
        f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}',
        new_access_token,
        ex=access_token_expires,
    )

    return ResponseUtil.success(msg='刷新成功', dict_content={
        'access_token': new_access_token,
        'token_type': 'Bearer'
    })


@loginController.get('/getInfo', response_model=CurrentUserModel)
async def get_login_user_info(
    request: Request, current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    logger.info('获取成功')

    return ResponseUtil.success(model_content=current_user)


@loginController.get('/getRouters')
async def get_login_user_routers(
    request: Request,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info('获取成功')
    user_routers = await LoginService.get_current_user_routers(current_user.user.user_id, query_db)

    return ResponseUtil.success(data=user_routers)


@loginController.post('/register', response_model=CrudResponseModel)
async def register_user(request: Request, user_register: UserRegister, query_db: AsyncSession = Depends(get_db)):
    user_register_result = await LoginService.register_user_services(request, query_db, user_register)
    logger.info(user_register_result.message)

    return ResponseUtil.success(data=user_register_result, msg=user_register_result.message)


# @loginController.post("/getSmsCode", response_model=SmsCode)
# async def get_sms_code(request: Request, user: ResetUserModel, query_db: AsyncSession = Depends(get_db)):
#     try:
#         sms_result = await LoginService.get_sms_code_services(request, query_db, user)
#         if sms_result.is_success:
#             logger.info('获取成功')
#             return ResponseUtil.success(data=sms_result)
#         else:
#             logger.warning(sms_result.message)
#             return ResponseUtil.failure(msg=sms_result.message)
#     except Exception as e:
#         logger.exception(e)
#         return ResponseUtil.error(msg=str(e))
#
#
# @loginController.post("/forgetPwd", response_model=CrudResponseModel)
# async def forget_user_pwd(request: Request, forget_user: ResetUserModel, query_db: AsyncSession = Depends(get_db)):
#     try:
#         forget_user_result = await LoginService.forget_user_services(request, query_db, forget_user)
#         if forget_user_result.is_success:
#             logger.info(forget_user_result.message)
#             return ResponseUtil.success(data=forget_user_result, msg=forget_user_result.message)
#         else:
#             logger.warning(forget_user_result.message)
#             return ResponseUtil.failure(msg=forget_user_result.message)
#     except Exception as e:
#         logger.exception(e)
#         return ResponseUtil.error(msg=str(e))



@loginController.post('/logout')
async def logout(request: Request, token: Optional[str] = Depends(oauth2_scheme)):
    payload = jwt.decode(
        token, JwtConfig.jwt_secret_key, algorithms=[JwtConfig.jwt_algorithm], options={'verify_exp': False}
    )
    session_id: str = payload.get('session_id')
    user_id: str = payload.get('user_id')

    # 删除 Access Token
    await LoginService.logout_services(request, session_id)

    # 获取 Refresh Token 并加入黑名单
    refresh_token_key = f'{RedisInitKeyConfig.REFRESH_TOKEN.key}:{user_id}'
    refresh_token = await request.app.state.redis.get(refresh_token_key)
    if refresh_token:
        expire_seconds = await request.app.state.redis.ttl(refresh_token_key)
        blacklist_key = f'{RedisInitKeyConfig.BLACKLIST_TOKEN.key}:{refresh_token}'
        await request.app.state.redis.set(blacklist_key, 'blacklisted', ex=expire_seconds)
        # 删除 Redis 中的 Refresh Token
        await request.app.state.redis.delete(refresh_token_key)

    logger.info('退出成功')
    return ResponseUtil.success(msg='退出成功')