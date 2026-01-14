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
# from module_admin.entity.vo.common_vo import CrudResponseModel
# from module_admin.entity.vo.login_vo import UserLogin, UserRegister, Token
# from module_admin.entity.vo.user_vo import CurrentUserModel, EditUserModel
# from module_admin.service.login_service import CustomOAuth2PasswordRequestForm, LoginService, oauth2_scheme
# from module_admin.service.user_service import UserService
from utils.log_util import logger
from utils.response_util import ResponseUtil


indexController = APIRouter(prefix='', tags=['前端首页'])


@indexController.get('/index')
@Log(title='首页', business_type=BusinessType.OTHER, log_type='operation')
async def index(
    request: Request
):
       
    
    logger.info('访问首页')
    
    return ResponseUtil.success(msg='访问首页成功')

