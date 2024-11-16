"""User data object"""

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
from sqlalchemy.ext.asyncio import create_async_engine


class UserBase(SQLModel):
    
    remark: Optional[str] = Field(
        sa_column=Column(
           String(255),
            nullable=True,
            
            comment="备注"
        )
    )
    
    status: Optional[int] = Field(
        sa_column=Column(
           Integer,
            nullable=True,
            
            comment="状态(0:停用,1:待审核,2:正常,3:已注销)"
        )
    )
    
    avatar_url: Optional[str] = Field(
        sa_column=Column(
           String(63),
            nullable=True,
            
            comment="头像地址"
        )
    )
    
    nickname: str = Field(
        sa_column=Column(
           String(32),
            nullable=False,
            
            comment="昵称"
        )
    )
    
    password: str = Field(
        sa_column=Column(
           String(63),
            nullable=False,
            
            comment="密码"
        )
    )
    
    username: str = Field(
        sa_column=Column(
           String(32),
            nullable=False,
            
            comment="用户名"
        )
    )
    


class UserDO(ModelExt, UserBase, ModelBase, table=True):
    __tablename__ = "test_user"
    __table_args__ = (
        
        
        
        UniqueConstraint('username', name="ix_sys_user_username"),
        
        
        
        Index("idx_status_nickname", 'status', 'nickname'),
        
        
        
        
        {"comment": "这是一段复原user结构的注释"}
        
    )

async def main():
    engine = create_async_engine(url="mysql+aiomysql://root:123456@localhost:3306/df")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())