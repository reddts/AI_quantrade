import os
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal, Optional, Union
from pydantic_validation_decorator import ValidateFields
from config.get_db import get_db
from config.enums import BusinessType
from config.env import UploadConfig
from common.annotation.log_annotation import Log
from common.aspect.data_scope import GetDataScope
from common.aspect.interface_auth import CheckUserInterfaceAuth
from common.entity.vo.dept_vo import DeptModel
from common.entity.vo.user_vo import (
    AddUserModel,
    CrudUserRoleModel,
    CurrentUserModel,
    DeleteUserModel,
    EditUserModel,
    ResetPasswordModel,
    ResetUserModel,
    UserDetailModel,
    UserInfoModel,
    UserModel,
    UserPageQueryModel,
    UserProfileModel,
    UserRoleQueryModel,
    UserRoleResponseModel,
)
from common.service.login_service import LoginService
from common.service.user_service import UserService
from common.service.role_service import RoleService
from common.service.dept_service import DeptService
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.pwd_util import PwdUtil
from utils.response_util import ResponseUtil
from utils.upload_util import UploadUtil


userController = APIRouter(prefix='', dependencies=[Depends(LoginService.get_current_user)])


@userController.get('/deptTree', dependencies=[Depends(CheckUserInterfaceAuth('front:user:list'))])
async def get_system_dept_tree(
    request: Request, query_db: AsyncSession = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    dept_query_result = await DeptService.get_dept_tree_services(query_db, DeptModel(**{}), data_scope_sql)
    logger.info('获取成功')

    return ResponseUtil.success(data=dept_query_result)




@userController.put('/resetPwd', dependencies=[Depends(CheckUserInterfaceAuth('system:user:resetPwd'))])
@Log(title='用户管理', business_type=BusinessType.UPDATE)
async def reset_system_user_pwd(
    request: Request,
    reset_user: EditUserModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    data_scope_sql: str = Depends(GetDataScope('SysUser')),
):
    await UserService.check_user_allowed_services(reset_user)
    if not current_user.user.admin:
        await UserService.check_user_data_scope_services(query_db, reset_user.user_id, data_scope_sql)
    edit_user = EditUserModel(
        userId=reset_user.user_id,
        password=PwdUtil.get_password_hash(reset_user.password),
        updateBy=current_user.user.user_name,
        updateTime=datetime.now(),
        type='pwd',
    )
    edit_user_result = await UserService.edit_user_services(query_db, edit_user)
    logger.info(edit_user_result.message)

    return ResponseUtil.success(msg=edit_user_result.message)



#已使用
@userController.get('/profile', response_model=UserProfileModel)
@Log(title='获取当前用户信息', business_type=BusinessType.OTHER)
async def query_detail_system_user_profile(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    profile_user_result = await UserService.user_profile_services(query_db, current_user.user.user_id)
    logger.info(f'获取user_id为{current_user.user.user_id}的信息成功')

    return ResponseUtil.success(model_content=profile_user_result)


#已使用
@userController.post('/profile/avatar')
@Log(title='修改个人头像', business_type=BusinessType.UPDATE)
async def change_system_user_profile_avatar(
    request: Request,
    avatarfile: bytes = File(),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    if avatarfile:
        relative_path = (
            f'avatar/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        )
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass
        avatar_name = f'avatar_{datetime.now().strftime("%Y%m%d%H%M%S")}{UploadConfig.UPLOAD_MACHINE}{UploadUtil.generate_random_number()}.png'
        avatar_path = os.path.join(dir_path, avatar_name)
        with open(avatar_path, 'wb') as f:
            f.write(avatarfile)
        edit_user = EditUserModel(
            userId=current_user.user.user_id,
            avatar=f'{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{avatar_name}',
            updateBy=current_user.user.user_name,
            updateTime=datetime.now(),
            type='avatar',
        )
        edit_user_result = await UserService.edit_user_services(query_db, edit_user)
        logger.info(edit_user_result.message)

        return ResponseUtil.success(dict_content={'imgUrl': edit_user.avatar}, msg=edit_user_result.message)
    return ResponseUtil.failure(msg='上传图片异常，请联系管理员')


#已使用
@userController.put('/profile')
@Log(title='修改个人信息', business_type=BusinessType.UPDATE)
async def change_system_user_profile_info(
    request: Request,
    user_info: UserInfoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_user = EditUserModel(
        **user_info.model_dump(exclude_unset=True, by_alias=True, exclude={'role_ids', 'post_ids'}),
        userId=current_user.user.user_id,
        userName=current_user.user.user_name,
        updateBy=current_user.user.user_name,
        updateTime=datetime.now(),
        
        roleIds=current_user.user.role_ids.split(',') if current_user.user.role_ids else [],
        postIds=current_user.user.post_ids.split(',') if current_user.user.post_ids else [],
        role=current_user.user.role,
    )
    edit_user_result = await UserService.edit_user_services(query_db, edit_user)
    logger.info(edit_user_result.message)

    return ResponseUtil.success(msg=edit_user_result.message)

#已使用
@userController.put('/profile/updatePwd')
@Log(title='修改个人密码', business_type=BusinessType.UPDATE)
async def reset_system_user_password(
    request: Request,
    reset_password: ResetPasswordModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    reset_user = ResetUserModel(
        userId=current_user.user.user_id,
        oldPassword=reset_password.old_password,
        password=reset_password.new_password,
        updateBy=current_user.user.user_name,
        updateTime=datetime.now(),
    )
    reset_user_result = await UserService.reset_user_services(query_db, reset_user)
    logger.info(reset_user_result.message)

    return ResponseUtil.success(msg=reset_user_result.message)







