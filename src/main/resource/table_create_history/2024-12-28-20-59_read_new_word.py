"""New data object"""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional
from sqlmodel import (
    Field,
    Column,
    SQLModel,
    String,
    Integer,
    BigInteger,
    SmallInteger,
    Boolean,
    Float,
    Double,
    Numeric,
    Date,
    DateTime,
    Time,
    LargeBinary,
    JSON,
    Index,
    UniqueConstraint,
    PrimaryKeyConstraint
)

from src.main.app.model.model_base import ModelBase, ModelExt
from src.main.app.common.session.db_engine import get_engine_by_database_id


class NewWordBase(SQLModel):
    user_id: Optional[int] = Field(
        sa_column=Column(
           BigInteger,
            nullable=True,
            comment="用户ID"
        )
    )
    
    article_id: Optional[int] = Field(
        sa_column=Column(
           BigInteger,
            nullable=True,
            comment="文章ID"
        )
    )
    
    word_id: Optional[int] = Field(
        sa_column=Column(
           BigInteger,
            nullable=True,
            comment="词库表ID"
        )
    )
    
    word: Optional[str] = Field(
        sa_column=Column(
           String(32),
            nullable=True,
            comment="单词"
        )
    )
    
    review_count: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            comment="复习次数"
        )
    )
    
    next_review_date: Optional[int] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="复习时间"
        )
    )
    
    tenant_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=1,
            comment="租户ID"
        )
    )
    


class NewWordDO(ModelExt, NewWordBase, ModelBase, table=True):
    __tablename__ = "read_new_word"
    __table_args__ = (
        Index("idx_my_tenantId_userId_word", "tenant_id", "user_id", "word"),
        Index("idx_nd_tenantId_userid_articleId", "tenant_id", "user_id", "article_id"),
        {"comment": "阅读生词表"}
    )

async def main():
    engine = await get_engine_by_database_id(env="dev", database_id=19325383610369)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())