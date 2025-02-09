"""UserRole schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class UserRolePage(BaseModel):
    """
    用户和角色关联分页信息
    """
    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 创建者
    creator: Optional[str] = ''
    # 创建时间
    create_time: Optional[datetime] = None
    # 更新者
    updater: Optional[str] = ''


class UserRoleQuery(PageBase):
    """
    用户和角色关联查询参数
    """
    # 自增编号
    id: Optional[int] = None
    # 角色ID
    role_id: Optional[int] = None
    # 创建者
    creator: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None
    # 更新者
    updater: Optional[str] = None


class UserRoleCreate(BaseModel):
    """
    用户和角色关联新增
    """
    # 角色ID
    role_id: int
    # 创建者
    creator: Optional[str] = ''
    # 更新者
    updater: Optional[str] = ''

    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class UserRoleAssign(BaseModel):
    user_id: int
    role_ids: List[int]

class UserRoleModify(BaseModel):
    """
    用户和角色关联更新
    """
    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 创建者
    creator: Optional[str] = ''
    # 更新者
    updater: Optional[str] = ''


class UserRoleBatchModify(BaseModel):
    """
    用户和角色关联批量更新
    """
    ids: List[int]
    # 角色ID
    role_id: int
    # 创建者
    creator: Optional[str] = ''
    # 更新者
    updater: Optional[str] = ''


class UserRoleDetail(BaseModel):
    """
    用户和角色关联详情
    """
    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 创建者
    creator: Optional[str] = ''
    # 创建时间
    create_time: Optional[datetime] = None
    # 更新者
    updater: Optional[str] = ''
