"""Table data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    Integer,
    BigInteger,
)
from src.main.pkg.model.model_base import ModelBase, ModelExt


class TableBase(SQLModel):
    database_id: int = Field(
        sa_column=Column(BigInteger, nullable=True, comment="数据库id")
    )
    name: str = Field(sa_column=Column(String(64), nullable=True, comment="表名称"))
    rows: int = Field(sa_column=Column(Integer, nullable=True, comment="行数"))
    index_length: str = Field(
        sa_column=Column(String(32), nullable=True, comment="索引长度")
    )
    data_length: str = Field(
        sa_column=Column(String(32), nullable=True, comment="数据长度")
    )
    remark: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class TableDO(ModelExt, TableBase, ModelBase, table=True):
    __tablename__ = "sys_table"
    __table_args__ = ({"comment": "表结构信息"},)
