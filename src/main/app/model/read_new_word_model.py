"""NewWord data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    Index,
    BigInteger,
    DateTime,
    Integer,
    String,
)
from src.main.app.common.util.snowflake_util import snowflake_id


class NewWordBase(SQLModel):

    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    user_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="用户ID"
        )
    )
    article_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="文章ID"
        )
    )
    word_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="词库表ID"
        )
    )
    word: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            default=None,
            comment="单词"
        )
    )
    translation: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            default=None,
            comment="翻译"
        )
    )
    review_count: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="复习次数"
        )
    )
    next_review_date: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            default=None,
            comment="复习时间"
        )
    )
    tenant_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="租户ID"
        )
    )
    create_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.now,
        sa_column_kwargs={"comment": "创建时间"},
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.now,
        sa_column_kwargs={
            "onupdate": datetime.now,
            "comment": "更新时间",
        },
    )


class NewWordDO(NewWordBase, table=True):
    __tablename__ = "read_new_word"
    __table_args__ = (
        Index("idx_my_tenantId_userId_word", 'tenant_id', 'user_id', 'word'),
        Index("idx_nd_tenantid_userid_articleid", 'tenant_id', 'user_id', 'article_id'),
        {"comment": "阅读生词表"}
    )