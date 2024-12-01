"""Database data object"""

from typing import Optional

from sqlmodel import Field, Column, String, SQLModel, BigInteger
from src.main.app.model.model_base import ModelBase, ModelExt


class DatabaseBase(SQLModel):
    connection_id: int = Field(sa_column=Column(BigInteger, index=True, nullable=False, comment="数据库连接id"))
    database_name: str = Field(sa_column=Column(String(32), nullable=False, comment="数据库名称"))
    character_set: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="字符编码"))
    collation: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="排序规则"))


class DatabaseDO(ModelExt, DatabaseBase, ModelBase, table=True):
    __tablename__ = "db_database"
    __table_args__ = ({"comment": "数据库信息表"},)
