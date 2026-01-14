from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from common.entity.do.perm_do import SysPerm
from common.entity.do.role_do import SysRole, SysRolePerm
from common.entity.do.user_do import SysUser, SysUserRole
from common.entity.vo.perm_vo import PermModel, PermQueryModel


class PermDao:
    """
    权限管理模块数据库操作层
    """

    @classmethod
    async def get_perm_detail_by_id(cls, db: AsyncSession, perm_id: int):
        """
        根据权限id获取权限详细信息

        :param db: orm对象
        :param perm_id: 权限id
        :return: 权限信息对象
        """
        perm_info = (await db.execute(select(SysPerm).where(SysPerm.perm_id == perm_id))).scalars().first()

        return perm_info

    @classmethod
    async def get_perm_detail_by_info(cls, db: AsyncSession, perm: PermModel):
        """
        根据权限参数获取权限信息

        :param db: orm对象
        :param perm: 权限参数对象
        :return: 权限信息对象
        """
        perm_info = (
            (
                await db.execute(
                    select(SysPerm).where(
                        SysPerm.parent_id == perm.parent_id if perm.parent_id else True,
                        SysPerm.perm_name == perm.perm_name if perm.perm_name else True,
                        SysPerm.perm_type == perm.perm_type if perm.perm_type else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return perm_info

    @classmethod
    async def get_perm_list_for_tree(cls, db: AsyncSession, user_id: int, role: list):
        """
        根据角色信息获取所有在用权限列表信息

        :param db: orm对象
        :param user_id: 用户id
        :param role: 用户角色列表信息
        :return: 权限列表信息
        """
        role_id_list = [item.role_id for item in role]
        if 1 in role_id_list:
            perm_query_all = (
                (await db.execute(select(SysPerm).where(SysPerm.status == '0').order_by(SysPerm.order_num).distinct()))
                .scalars()
                .all()
            )
        else:
            perm_query_all = (
                (
                    await db.execute(
                        select(SysPerm)
                        .select_from(SysUser)
                        .where(SysUser.status == '0', SysUser.del_flag == '0', SysUser.user_id == user_id)
                        .join(SysUserRole, SysUser.user_id == SysUserRole.user_id, isouter=True)
                        .join(
                            SysRole,
                            and_(
                                SysUserRole.role_id == SysRole.role_id, SysRole.status == '0', SysRole.del_flag == '0'
                            ),
                            isouter=True,
                        )
                        .join(SysRolePerm, SysRole.role_id == SysRolePerm.role_id, isouter=True)
                        .join(SysPerm, and_(SysRolePerm.perm_id == SysPerm.perm_id, SysPerm.status == '0'))
                        .order_by(SysPerm.order_num)
                        .distinct()
                    )
                )
                .scalars()
                .all()
            )

        return perm_query_all

    @classmethod
    async def get_perm_list(cls, db: AsyncSession, page_object: PermQueryModel, user_id: int, role: list):
        """
        根据查询参数获取权限列表信息

        :param db: orm对象
        :param page_object: 不分页查询参数对象
        :param user_id: 用户id
        :param role: 用户角色列表
        :return: 权限列表信息对象
        """
        role_id_list = [item.role_id for item in role]
        if 1 in role_id_list:
            perm_query_all = (
                (
                    await db.execute(
                        select(SysPerm)
                        .where(
                            SysPerm.status == page_object.status if page_object.status else True,
                            SysPerm.perm_name.like(f'%{page_object.perm_name}%') if page_object.perm_name else True,
                        )
                        .order_by(SysPerm.order_num)
                        .distinct()
                    )
                )
                .scalars()
                .all()
            )
        else:
            perm_query_all = (
                (
                    await db.execute(
                        select(SysPerm)
                        .select_from(SysUser)
                        .where(SysUser.status == '0', SysUser.del_flag == '0', SysUser.user_id == user_id)
                        .join(SysUserRole, SysUser.user_id == SysUserRole.user_id, isouter=True)
                        .join(
                            SysRole,
                            and_(
                                SysUserRole.role_id == SysRole.role_id, SysRole.status == '0', SysRole.del_flag == '0'
                            ),
                            isouter=True,
                        )
                        .join(SysRolePerm, SysRole.role_id == SysRolePerm.role_id, isouter=True)
                        .join(
                            SysPerm,
                            and_(
                                SysRolePerm.perm_id == SysPerm.perm_id,
                                SysPerm.status == page_object.status if page_object.status else True,
                                SysPerm.perm_name.like(f'%{page_object.perm_name}%') if page_object.perm_name else True,
                            ),
                        )
                        .order_by(SysPerm.order_num)
                        .distinct()
                    )
                )
                .scalars()
                .all()
            )

        return perm_query_all

    @classmethod
    async def add_perm_dao(cls, db: AsyncSession, perm: PermModel):
        """
        新增权限数据库操作

        :param db: orm对象
        :param perm: 权限对象
        :return:
        """
        db_perm = SysPerm(**perm.model_dump())
        db.add(db_perm)
        await db.flush()

        return db_perm

    @classmethod
    async def edit_perm_dao(cls, db: AsyncSession, perm: dict):
        """
        编辑权限数据库操作

        :param db: orm对象
        :param perm: 需要更新的权限字典
        :return:
        """
        await db.execute(update(SysPerm), [perm])

    @classmethod
    async def delete_perm_dao(cls, db: AsyncSession, perm: PermModel):
        """
        删除权限数据库操作

        :param db: orm对象
        :param perm: 权限对象
        :return:
        """
        await db.execute(delete(SysPerm).where(SysPerm.perm_id.in_([perm.perm_id])))

    @classmethod
    async def has_child_by_perm_id_dao(cls, db: AsyncSession, perm_id: int):
        """
        根据权限id查询权限关联子权限的数量

        :param db: orm对象
        :param perm_id: 权限id
        :return: 权限关联子权限的数量
        """
        perm_count = (
            await db.execute(select(func.count('*')).select_from(SysPerm).where(SysPerm.parent_id == perm_id))
        ).scalar()

        return perm_count

    @classmethod
    async def check_perm_exist_role_dao(cls, db: AsyncSession, perm_id: int):
        """
        根据权限id查询权限关联角色数量

        :param db: orm对象
        :param perm_id: 权限id
        :return: 权限关联角色数量
        """
        role_count = (
            await db.execute(select(func.count('*')).select_from(SysRolePerm).where(SysRolePerm.perm_id == perm_id))
        ).scalar()

        return role_count
