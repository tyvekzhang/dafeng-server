"""Member data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
)
from src.main.app.common.util.snowflake_util import snowflake_id


class MemberBase(SQLModel):
    
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    name: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="名称"
        )
    )
    nation: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="国家"
        )
    )
    gender: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="性别"
        )
    )
    birthday: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            default=None,
            comment="生日"
        )
    )
    hobby: Optional[str] = Field(
        sa_column=Column(
            String(255),
            nullable=True,
            default=None,
            comment="爱好"
        )
    )


class MemberDO(MemberBase, table=True):
    __tablename__ = "member"
    __table_args__ = (
        {"comment": "会员管理"}
    )