from datetime import datetime
from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.enums import BusinessType
from config.get_db import get_db
from common.annotation.log_annotation import Log
from common.aspect.interface_auth import CheckUserInterfaceAuth
from common.entity.vo.perm_vo import DeletePermModel, PermModel, PermQueryModel
from common.entity.vo.user_vo import CurrentUserModel
from common.service.login_service import LoginService
from common.service.perm_service import PermService
from utils.log_util import logger
from utils.response_util import ResponseUtil


permController = APIRouter(prefix='/system/perm', dependencies=[Depends(LoginService.get_current_user)])


@permController.get('/treeselect')
async def get_system_perm_tree(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    perm_query_result = await PermService.get_perm_tree_services(query_db, current_user)
    logger.info('获取成功')

    return ResponseUtil.success(data=perm_query_result)


@permController.get('/rolePermTreeselect/{role_id}')
async def get_system_role_perm_tree(
    request: Request,
    role_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    role_perm_query_result = await PermService.get_role_perm_tree_services(query_db, role_id, current_user)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=role_perm_query_result)


@permController.get(
    '/list', response_model=List[PermModel], dependencies=[Depends(CheckUserInterfaceAuth('system:perm:list'))]
)
async def get_system_perm_list(
    request: Request,
    perm_query: PermQueryModel = Depends(PermQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    perm_query_result = await PermService.get_perm_list_services(query_db, perm_query, current_user)
    logger.info('获取成功')

    return ResponseUtil.success(data=perm_query_result)


@permController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:perm:add'))])
@ValidateFields(validate_model='add_perm')
@Log(title='权限管理', business_type=BusinessType.INSERT)
async def add_system_perm(
    request: Request,
    add_perm: PermModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_perm.create_by = current_user.user.user_name
    add_perm.create_time = datetime.now()
    add_perm.update_by = current_user.user.user_name
    add_perm.update_time = datetime.now()
    add_perm_result = await PermService.add_perm_services(query_db, add_perm)
    logger.info(add_perm_result.message)

    return ResponseUtil.success(msg=add_perm_result.message)


@permController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:perm:edit'))])
@ValidateFields(validate_model='edit_perm')
@Log(title='权限管理', business_type=BusinessType.UPDATE)
async def edit_system_perm(
    request: Request,
    edit_perm: PermModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_perm.update_by = current_user.user.user_name
    edit_perm.update_time = datetime.now()
    edit_perm_result = await PermService.edit_perm_services(query_db, edit_perm)
    logger.info(edit_perm_result.message)

    return ResponseUtil.success(msg=edit_perm_result.message)


@permController.delete('/{perm_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:perm:remove'))])
@Log(title='权限管理', business_type=BusinessType.DELETE)
async def delete_system_perm(request: Request, perm_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_perm = DeletePermModel(permIds=perm_ids)
    delete_perm_result = await PermService.delete_perm_services(query_db, delete_perm)
    logger.info(delete_perm_result.message)

    return ResponseUtil.success(msg=delete_perm_result.message)


@permController.get(
    '/{perm_id}', response_model=PermModel, dependencies=[Depends(CheckUserInterfaceAuth('system:perm:query'))]
)
async def query_detail_system_perm(request: Request, perm_id: int, query_db: AsyncSession = Depends(get_db)):
    perm_detail_result = await PermService.perm_detail_services(query_db, perm_id)
    logger.info(f'获取perm_id为{perm_id}的信息成功')

    return ResponseUtil.success(data=perm_detail_result)
