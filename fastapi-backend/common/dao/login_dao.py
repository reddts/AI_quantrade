from sqlalchemy import and_, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from common.entity.do.dept_do import SysDept
from common.entity.do.user_do import SysUser


async def login_by_account(db: AsyncSession, user_name: str):
    """
    根据用户名查询用户信息

    :param db: orm对象
    :param user_name: 用户名
    :return: 用户对象
    """
    user = (
        await db.execute(
            select(SysUser, SysDept)
            .where(SysUser.user_name == user_name, SysUser.del_flag == '0')
            .join(
                SysDept,
                and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == '0', SysDept.del_flag == '0'),
                isouter=True,
            )
            .distinct()
        )
    ).first()

    return user

#调用验证用户名和手机号码是否存在
async def check_user_exists(db: AsyncSession, username: str, phonenumber: str):
    """
    检查用户是否存在

    :param db: orm对象
    :param user_name: 用户名
    :param phone_number: 手机号码
    :return: 用户是否存在
    """
    user = await db.execute(
        select(SysUser).where(
            or_(
                SysUser.user_name == username,
                SysUser.phonenumber == phonenumber
            ),
            SysUser.del_flag == '0'
        )
    )
    return user.first() is not None
