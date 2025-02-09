"""Role schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class RolePage(BaseModel):
    """
    角色信息分页信息
    """
    # 角色ID
    id: int
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: datetime

class RoleQuery(PageBase):
    """
    角色信息查询参数
    """
    # 角色名称
    name: Optional[str] = None
    # 角色权限字符串
    code: Optional[str] = None
    # 角色状态（0正常 1停用）
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None

class RoleCreate(BaseModel):
    """
    角色信息新增
    """
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 备注
    comment: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

    menu_ids: List[int]

class RoleModify(BaseModel):
    """
    角色信息更新
    """
    # 角色ID
    id: int
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: int
    # 数据范围(指定部门数组)
    data_scope_dept_ids: str
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None

class RoleBatchModify(BaseModel):
    """
    角色信息批量更新
    """
    ids: List[int]
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: int
    # 数据范围(指定部门数组)
    data_scope_dept_ids: str
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None

class RoleDetail(BaseModel):
    """
    角色信息详情
    """
    # 角色ID
    id: int
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: int
    # 数据范围(指定部门数组)
    data_scope_dept_ids: str
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: datetime