"""GlobalWord data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    Index,
    BigInteger,
    String,
    Integer,
)
from src.main.app.common.util.snowflake_util import snowflake_id


class GlobalWordBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    word: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            default=None,
            comment="单词"
        )
    )
    pronunciation: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="国际音标"
        )
    )
    pronunciationUs: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="美式音标"
        )
    )
    definition: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="定义"
        )
    )
    example: Optional[str] = Field(
        sa_column=Column(
            String(500),
            nullable=True,
            default=None,
            comment="例句"
        )
    )
    translation: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="翻译"
        )
    )
    wordSrc: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="单词音频"
        )
    )
    wordSrcUs: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="美式音频"
        )
    )
    exampleSrc: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="例句音频"
        )
    )
    pluralForm: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="复数"
        )
    )
    thirdPersonSingular: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="人称单数"
        )
    )
    presentTenseContinuous: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="进行时"
        )
    )
    pastTense: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="过去式"
        )
    )
    pastParticiple: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
            comment="过去分词"
        )
    )
    level: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="等级"
        )
    )
    version: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="版本"
        )
    )
    tag: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="标签"
        )
    )
    status: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=0,
            comment="状态"
        )
    )
    createTime: Optional[datetime] = Field(
        sa_column=Column(
            String,
            nullable=True,
            default=None,
            comment="创建时间"
        )
    )
    updateTime: Optional[datetime] = Field(
        sa_column=Column(
            String,
            nullable=True,
            default=None,
            comment="更新时间"
        )
    )


class GlobalWordDO(GlobalWordBase, table=False):
    __tablename__ = "read_global_word"
    __table_args__ = (
        Index("idx_word", 'word'),
        {"comment": "阅读词库表"}
    )