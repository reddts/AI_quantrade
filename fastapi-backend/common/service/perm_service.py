from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from config.constant import CommonConstant, PermConstant
from exceptions.exception import ServiceException, ServiceWarning
from common.dao.perm_dao import PermDao
from common.dao.role_dao import RoleDao
from common.entity.vo.common_vo import CrudResponseModel
from common.entity.vo.perm_vo import DeletePermModel, PermQueryModel, PermModel
from common.entity.vo.role_vo import RolePermQueryModel
from common.entity.vo.user_vo import CurrentUserModel
from utils.common_util import CamelCaseUtil
from utils.string_util import StringUtil


class PermService:
    """
    权限管理模块服务层
    """

    @classmethod
    async def get_perm_tree_services(cls, query_db: AsyncSession, current_user: Optional[CurrentUserModel] = None):
        """
        获取权限树信息service

        :param query_db: orm对象
        :param current_user: 当前用户对象
        :return: 权限树信息对象
        """
        perm_list_result = await PermDao.get_perm_list_for_tree(
            query_db, current_user.user.user_id, current_user.user.role
        )
        perm_tree_result = cls.list_to_tree(perm_list_result)

        return perm_tree_result

    @classmethod
    async def get_role_perm_tree_services(
        cls, query_db: AsyncSession, role_id: int, current_user: Optional[CurrentUserModel] = None
    ):
        """
        根据角色id获取权限树信息service

        :param query_db: orm对象
        :param role_id: 角色id
        :param current_user: 当前用户对象
        :return: 当前角色id的权限树信息对象
        """
        perm_list_result = await PermDao.get_perm_list_for_tree(
            query_db, current_user.user.user_id, current_user.user.role
        )
        perm_tree_result = cls.list_to_tree(perm_list_result)
        role = await RoleDao.get_role_detail_by_id(query_db, role_id)
        role_perm_list = await RoleDao.get_role_perm_dao(query_db, role)
        checked_keys = [row.perm_id for row in role_perm_list]
        result = RolePermQueryModel(perms=perm_tree_result, checkedKeys=checked_keys)

        return result

    @classmethod
    async def get_perm_list_services(
        cls, query_db: AsyncSession, page_object: PermQueryModel, current_user: Optional[CurrentUserModel] = None
    ):
        """
        获取权限列表信息service

        :param query_db: orm对象
        :param page_object: 分页查询参数对象
        :param current_user: 当前用户对象
        :return: 权限列表信息对象
        """
        perm_list_result = await PermDao.get_perm_list(
            query_db, page_object, current_user.user.user_id, current_user.user.role
        )

        return CamelCaseUtil.transform_result(perm_list_result)

    @classmethod
    async def check_perm_name_unique_services(cls, query_db: AsyncSession, page_object: PermModel):
        """
        校验权限名称是否唯一service

        :param query_db: orm对象
        :param page_object: 权限对象
        :return: 校验结果
        """
        perm_id = -1 if page_object.perm_id is None else page_object.perm_id
        perm = await PermDao.get_perm_detail_by_info(query_db, PermModel(permName=page_object.perm_name))
        if perm and perm.perm_id != perm_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_perm_services(cls, query_db: AsyncSession, page_object: PermModel):
        """
        新增权限信息service

        :param query_db: orm对象
        :param page_object: 新增权限对象
        :return: 新增权限校验结果
        """
        if not await cls.check_perm_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增权限{page_object.perm_name}失败，权限名称已存在')
        elif page_object.is_frame == PermConstant.YES_FRAME and not StringUtil.is_http(page_object.path):
            raise ServiceException(message=f'新增权限{page_object.perm_name}失败，地址必须以http(s)://开头')
        else:
            try:
                await PermDao.add_perm_dao(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def edit_perm_services(cls, query_db: AsyncSession, page_object: PermModel):
        """
        编辑权限信息service

        :param query_db: orm对象
        :param page_object: 编辑部门对象
        :return: 编辑权限校验结果
        """
        edit_perm = page_object.model_dump(exclude_unset=True)
        perm_info = await cls.perm_detail_services(query_db, page_object.perm_id)
        if perm_info.perm_id:
            if not await cls.check_perm_name_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改权限{page_object.perm_name}失败，权限名称已存在')
            elif page_object.is_frame == PermConstant.YES_FRAME and not StringUtil.is_http(page_object.path):
                raise ServiceException(message=f'修改权限{page_object.perm_name}失败，地址必须以http(s)://开头')
            elif page_object.perm_id == page_object.parent_id:
                raise ServiceException(message=f'修改权限{page_object.perm_name}失败，上级权限不能选择自己')
            else:
                try:
                    await PermDao.edit_perm_dao(query_db, edit_perm)
                    await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='权限不存在')

    @classmethod
    async def delete_perm_services(cls, query_db: AsyncSession, page_object: DeletePermModel):
        """
        删除权限信息service

        :param query_db: orm对象
        :param page_object: 删除权限对象
        :return: 删除权限校验结果
        """
        if page_object.perm_ids:
            perm_id_list = page_object.perm_ids.split(',')
            try:
                for perm_id in perm_id_list:
                    if (await PermDao.has_child_by_perm_id_dao(query_db, int(perm_id))) > 0:
                        raise ServiceWarning(message='存在子权限,不允许删除')
                    elif (await PermDao.check_perm_exist_role_dao(query_db, int(perm_id))) > 0:
                        raise ServiceWarning(message='权限已分配,不允许删除')
                    await PermDao.delete_perm_dao(query_db, PermModel(permId=perm_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入权限id为空')

    @classmethod
    async def perm_detail_services(cls, query_db: AsyncSession, perm_id: int):
        """
        获取权限详细信息service

        :param query_db: orm对象
        :param perm_id: 权限id
        :return: 权限id对应的信息
        """
        perm = await PermDao.get_perm_detail_by_id(query_db, perm_id=perm_id)
        if perm:
            result = PermModel(**CamelCaseUtil.transform_result(perm))
        else:
            result = PermModel(**dict())

        return result

    @classmethod
    def list_to_tree(cls, permission_list: list) -> list:
        """
        工具方法：根据权限列表信息生成树形嵌套数据

        :param permission_list: 权限列表信息
        :return: 权限树形嵌套数据
        """
        permission_list = [
            dict(id=item.perm_id, label=item.perm_name, parentId=item.parent_id) for item in permission_list
        ]
        # 转成id为key的字典
        mapping: dict = dict(zip([i['id'] for i in permission_list], permission_list))

        # 树容器
        container: list = []

        for d in permission_list:
            # 如果找不到父级项，则是根节点
            parent: dict = mapping.get(d['parentId'])
            if parent is None:
                container.append(d)
            else:
                children: list = parent.get('children')
                if not children:
                    children = []
                children.append(d)
                parent.update({'children': children})

        return container
