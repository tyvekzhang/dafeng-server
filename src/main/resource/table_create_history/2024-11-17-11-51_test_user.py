"""User data object"""

from typing import Optional
from sqlmodel import (
    Field,
    Column,
    SQLModel,
    String,
    Integer,
    Index,
    UniqueConstraint,
)

from src.main.app.model.model_base import ModelBase, ModelExt
from src.main.app.common.session.db_engine import get_engine_by_database_id


class UserBase(SQLModel):
    remark: Optional[str] = Field(sa_column=Column(String(255), nullable=True, comment="备注"))

    status: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True, comment="状态(0:停用,1:待审核,2:正常,3:已注销)")
    )

    avatar_url: Optional[str] = Field(sa_column=Column(String(63), nullable=True, comment="头像地址"))

    nickname: str = Field(sa_column=Column(String(32), nullable=False, comment="昵称"))

    password: str = Field(sa_column=Column(String(63), nullable=False, comment="密码"))

    username: str = Field(sa_column=Column(String(32), nullable=False, comment="用户名"))


class UserDO(ModelExt, UserBase, ModelBase, table=True):
    __tablename__ = "test_user"
    __table_args__ = (
        UniqueConstraint("username", name="ix_sys_user_username"),
        Index("idx_status_nickname", "status", "nickname"),
        {"comment": "这是一段复原user结构的注释"},
    )


async def main():
    engine = await get_engine_by_database_id(env="dev", database_id=5467156516865)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
