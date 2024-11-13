"""User data object"""

from typing import Optional

from sqlmodel import Field, Column, String, Integer

from src.main.app.model.model_base import ModelBase, ModelExt


class UserBase:
    username: str = Field(
        sa_column=Column(
            String(32), index=True, unique=True, nullable=True, comment="用户名"
        )
    )
    password: str = Field(
        default=None, sa_column=Column(String(64), nullable=True, comment="密码")
    )
    nickname: str = Field(default=None, sa_column=Column(String(32), comment="昵称"))
    avatar_url: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="头像地址")
    )
    status: int = Field(
        default=1,
        sa_column=Column(Integer, comment="状态(0:停用,1:待审核,2:正常,3:已注销)"),
    )
    remark: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class UserDO(ModelExt, UserBase, ModelBase, table=True):
    __tablename__ = "sys_user"
    __table_args__ = {"comment": "用户信息表"}
