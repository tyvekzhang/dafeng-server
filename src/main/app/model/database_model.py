"""Database data object"""

from sqlmodel import Field, Column, String, SQLModel, BigInteger
from src.main.app.model.model_base import ModelBase, ModelExt


class DatabaseBase(SQLModel):
    connection_id: int = Field(
        sa_column=Column(BigInteger, nullable=True, comment="连接id")
    )
    database_name: str = Field(
        sa_column=Column(String(32), index=True, nullable=True, comment="数据库名称")
    )
    character_set: str = Field(
        sa_column=Column(String(16), nullable=True, comment="字符编码")
    )
    collation: str = Field(
        sa_column=Column(String(16), nullable=True, comment="排序规则")
    )


class DatabaseDO(ModelExt, DatabaseBase, ModelBase, table=True):
    __tablename__ = "sys_database"
    __table_args__ = ({"comment": "数据库信息表"},)
