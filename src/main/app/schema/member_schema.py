"""Member schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class MemberPage(BaseModel):
    """
    会员管理分页信息
    """
    # 主键
    id: int
    # 名称
    name: Optional[str] = None
    # 国家
    nation: Optional[str] = None
    # 性别
    gender: Optional[int] = None
    # 生日
    birthday: Optional[datetime] = None
    # 爱好
    hobby: Optional[str] = None

class MemberQuery(PageBase):
    """
    会员管理查询参数
    """
    # 主键
    id: Optional[int] = None
    # 名称
    name: Optional[str] = None
    # 国家
    nation: Optional[str] = None
    # 性别
    gender: Optional[int] = None
    # 生日
    birthday: Optional[datetime] = None
    # 爱好
    hobby: Optional[str] = None

class MemberCreate(BaseModel):
    """
    会员管理新增
    """
    # 名称
    name: Optional[str] = None
    # 国家
    nation: Optional[str] = None
    # 性别
    gender: Optional[int] = None
    # 生日
    birthday: Optional[datetime] = None
    # 爱好
    hobby: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class MemberModify(BaseModel):
    """
    会员管理更新
    """
    # 主键
    id: int
    # 名称
    name: Optional[str] = None
    # 国家
    nation: Optional[str] = None
    # 性别
    gender: Optional[int] = None
    # 生日
    birthday: Optional[datetime] = None
    # 爱好
    hobby: Optional[str] = None

class MemberBatchModify(BaseModel):
    """
    会员管理批量更新
    """
    ids: List[int]
    # 名称
    name: Optional[str] = None
    # 国家
    nation: Optional[str] = None
    # 性别
    gender: Optional[int] = None
    # 生日
    birthday: Optional[datetime] = None
    # 爱好
    hobby: Optional[str] = None

class MemberDetail(BaseModel):
    """
    会员管理详情
    """
    # 主键
    id: int
    # 名称
    name: Optional[str] = None
    # 国家
    nation: Optional[str] = None
    # 性别
    gender: Optional[int] = None
    # 生日
    birthday: Optional[datetime] = None
    # 爱好
    hobby: Optional[str] = None