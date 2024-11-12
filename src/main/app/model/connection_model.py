"""Connection data object"""

from sqlmodel import Field, Column, String, SQLModel, Integer
from src.main.app.model.model_base import ModelBase, ModelExt


class ConnectionBase(SQLModel):
    connection_name: str = Field(
        sa_column=Column(String(32), index=True, nullable=True, comment="连接名称")
    )
    database_type: str = Field(
        sa_column=Column(String(16), nullable=True, comment="数据库类型")
    )
    server_version: str = Field(
        sa_column=Column(String(16), nullable=True, comment="数据库版本")
    )
    host: str = Field(sa_column=Column(String(16), nullable=True, comment="主机"))
    port: int = Field(sa_column=Column(Integer, nullable=True, comment="端口号"))
    username: str = Field(sa_column=Column(String(32), nullable=True, comment="用户名"))
    password: str = Field(sa_column=Column(String(63), nullable=True, comment="密码"))
    sessions: int = Field(
        sa_column=Column(Integer, nullable=True, comment="活跃连接数")
    )
    client_character_set: str = Field(
        sa_column=Column(String(16), nullable=True, comment="客户端编码")
    )


class ConnectionDO(ModelExt, ConnectionBase, ModelBase, table=True):
    __tablename__ = "sys_connection"
    __table_args__ = ({"comment": "连接信息表"},)
