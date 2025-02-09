"""RoleMenu schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class RoleMenuPage(BaseModel):
    """
    角色和菜单关联分页信息
    """
    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建者
    creator: Optional[str] = ''
    # 创建时间
    create_time: datetime
    # 更新者
    updater: Optional[str] = ''

class RoleMenuQuery(PageBase):
    """
    角色和菜单关联查询参数
    """
    # 自增编号
    id: Optional[int] = None
    # 角色ID
    role_id: Optional[int] = None
    # 菜单ID
    menu_id: Optional[int] = None
    # 创建者
    creator: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None
    # 更新者
    updater: Optional[str] = None


class RoleMenuCreate(BaseModel):
    """
    角色和菜单关联新增
    """
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建者
    creator: Optional[str] = ''
    # 更新者
    updater: Optional[str] = ''
    # None
    deleted: str
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class RoleMenuModify(BaseModel):
    """
    角色和菜单关联更新
    """
    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建者
    creator: Optional[str] = ''
    # 更新者
    updater: Optional[str] = ''
    # None
    deleted: str

class RoleMenuBatchModify(BaseModel):
    """
    角色和菜单关联批量更新
    """
    ids: List[int]
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建者
    creator: Optional[str] = ''
    # 更新者
    updater: Optional[str] = ''
    # None
    deleted: str

class RoleMenuDetail(BaseModel):
    """
    角色和菜单关联详情
    """
    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建者
    creator: Optional[str] = ''
    # 创建时间
    create_time: datetime
    # 更新者
    updater: Optional[str] = ''
    # None
    deleted: str