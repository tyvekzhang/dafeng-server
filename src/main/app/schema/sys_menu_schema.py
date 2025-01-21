"""Menu schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class MenuPage(BaseModel):
    """
    系统菜单分页信息
    """
    # 主键
    id: int
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = '1'
    # 创建时间
    create_time: Optional[datetime] = None

class MenuQuery(PageBase):
    """
    系统菜单查询参数
    """
    # 名称
    name: Optional[str] = None
    # 状态（1正常 0停用）
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None

class MenuCreate(BaseModel):
    """
    系统菜单新增
    """
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[str] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = '1'
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = '1'
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = '1'
    # 备注信息
    comment: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class MenuModify(BaseModel):
    """
    系统菜单更新
    """
    # 主键
    id: int
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[str] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = '1'
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = '1'
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = '1'
    # 备注信息
    comment: Optional[str] = None

class MenuBatchModify(BaseModel):
    """
    系统菜单批量更新
    """
    ids: List[int]
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[str] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = '1'
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = '1'
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = '1'
    # 备注信息
    comment: Optional[str] = None

class MenuDetail(BaseModel):
    """
    系统菜单详情
    """
    # 主键
    id: int
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[str] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = '1'
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = '1'
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = '1'
    # 创建时间
    create_time: Optional[datetime] = None
    # 备注信息
    comment: Optional[str] = None