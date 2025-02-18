"""NewWord schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class NewWordPage(BaseModel):
    """
    阅读生词分页信息
    """
    # 主键
    id: int
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 租户ID
    tenant: Optional[int] = None
    # 更新时间
    update_time: Optional[datetime] = None

class NewWordQuery(PageBase):
    """
    阅读生词查询参数
    """
    # 主键
    id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 租户ID
    tenant: Optional[int] = None
    # 更新时间
    update_time: Optional[datetime] = None

class NewWordCreate(BaseModel):
    """
    阅读生词新增
    """
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 租户ID
    tenant: Optional[int] = None
    # 更新时间
    update_time: Optional[datetime] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class NewWordModify(BaseModel):
    """
    阅读生词更新
    """
    # 主键
    id: int
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 租户ID
    tenant: Optional[int] = None
    # 更新时间
    update_time: Optional[datetime] = None

class NewWordBatchModify(BaseModel):
    """
    阅读生词批量更新
    """
    ids: List[int]
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 租户ID
    tenant: Optional[int] = None
    # 更新时间
    update_time: Optional[datetime] = None

class NewWordDetail(BaseModel):
    """
    阅读生词详情
    """
    # 主键
    id: int
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 租户ID
    tenant: Optional[int] = None
    # 更新时间
    update_time: Optional[datetime] = None