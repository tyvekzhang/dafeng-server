"""Index data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    BigInteger,
)
from src.main.pkg.model.model_base import ModelBase, ModelExt


class IndexBase(SQLModel):
    table_id: int = Field(sa_column=Column(BigInteger, nullable=True, comment="表id"))
    name: str = Field(sa_column=Column(String(32), nullable=True, comment="索引名称"))
    field: str = Field(sa_column=Column(String(63), nullable=True, comment="索引字段"))
    type: str = Field(sa_column=Column(String(16), nullable=True, comment="索引类型"))
    method: str = Field(sa_column=Column(String(16), nullable=True, comment="索引方法"))
    remark: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class IndexDO(ModelExt, IndexBase, ModelBase, table=True):
    __tablename__ = "sys_index"
    __table_args__ = ({"comment": "索引信息表"},)
