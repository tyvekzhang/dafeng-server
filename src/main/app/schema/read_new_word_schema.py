"""NewWord schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.schema.common_schema import PageBase

class NewWordQuery(PageBase):
    """
    阅读生词查询参数
    """
    # 主键
    id: Optional[int] = None
    # 文章ID
    article_id: Optional[int] = None
    # 词库表ID
    word_id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习次数
    review_count: Optional[int] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 创建时间
    create_time: Optional[datetime] = None

class NewWordCreate(BaseModel):
    """
    阅读生词新增
    """
    # 文章ID
    article_id: Optional[int] = None
    # 词库表ID
    word_id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习次数
    review_count: Optional[int] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")

class NewWordModify(BaseModel):
    """
    阅读生词更新
    """
    # 主键
    id: int
    # 文章ID
    article_id: Optional[int] = None
    # 词库表ID
    word_id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习次数
    review_count: Optional[int] = None
    # 复习时间
    next_review_date: Optional[datetime] = None

class NewWordBatchModify(BaseModel):
    """
    阅读生词批量更新
    """
    ids: List[int]
    # 文章ID
    article_id: Optional[int] = None
    # 词库表ID
    word_id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习次数
    review_count: Optional[int] = None
    # 复习时间
    next_review_date: Optional[datetime] = None

class NewWordDetail(BaseModel):
    """
    阅读生词详情
    """
    # 主键
    id: int
    # 文章ID
    article_id: Optional[int] = None
    # 词库表ID
    word_id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习次数
    review_count: Optional[int] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 创建时间
    create_time: Optional[datetime] = None

class NewWordPage(BaseModel):
    """
    阅读生词分页信息
    """
    # 主键
    id: int
    # 文章ID
    article_id: Optional[int] = None
    # 词库表ID
    word_id: Optional[int] = None
    # 单词
    word: Optional[str] = None
    # 翻译
    translation: Optional[str] = None
    # 复习次数
    review_count: Optional[int] = None
    # 复习时间
    next_review_date: Optional[datetime] = None
    # 创建时间
    create_time: Optional[datetime] = None