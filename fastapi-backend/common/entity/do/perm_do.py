from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from config.database import Base


class SysPerm(Base):
    """
    权限表
    """

    __tablename__ = 'sys_permission'

    perm_id = Column(Integer, primary_key=True, autoincrement=True, comment='权限ID')
    perm_name = Column(String(50), nullable=False, default='', comment='权限名称')
    parent_id = Column(Integer, default=0, comment='父权限ID')
    order_num = Column(Integer, default=0, comment='显示顺序')
    path = Column(String(200), nullable=True, default='', comment='路由地址')
    component = Column(String(255), nullable=True, default=None, comment='组件路径')
    query = Column(String(255), nullable=True, default=None, comment='路由参数')
    route_name = Column(String(50), nullable=True, default='', comment='路由名称')
    is_frame = Column(Integer, default=1, comment='是否为外链（0是 1否）')
    is_cache = Column(Integer, default=0, comment='是否缓存（0缓存 1不缓存）')
    perm_type = Column(String(1), nullable=True, default='', comment='权限类型（M目录 C菜单 F按钮）')
    visible = Column(String(1), nullable=True, default='0', comment='权限状态（0显示 1隐藏）')
    status = Column(String(1), nullable=True, default='0', comment='权限状态（0正常 1停用）')
    perms = Column(String(100), nullable=True, default=None, comment='权限标识')
    icon = Column(String(100), nullable=True, default='#', comment='权限图标')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    remark = Column(String(500), nullable=True, default='', comment='备注')
