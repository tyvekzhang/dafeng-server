"""Field data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    Integer,
    Boolean,
    BigInteger,
)
from src.main.pkg.model.model_base import ModelBase, ModelExt


class FieldBase(SQLModel):
    table_id: int = Field(sa_column=Column(BigInteger, nullable=True, comment="表id"))
    name: str = Field(sa_column=Column(String(64), nullable=True, comment="字段名称"))
    type: str = Field(sa_column=Column(String(32), nullable=True, comment="类型"))
    length: int = Field(sa_column=Column(Integer, comment="长度"))
    decimals: int = Field(sa_column=Column(Integer, comment="小数位数"))
    not_null: bool = Field(
        default=False, sa_column=Column(Boolean, comment="允许为空(0:允许, 1:不允许)")
    )
    key: bool = Field(
        default=False, sa_column=Column(Boolean, comment="是否主键(0:否, 1:是)")
    )
    remark: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class FieldDO(ModelExt, FieldBase, ModelBase, table=True):
    __tablename__ = "sys_field"
    __table_args__ = ({"comment": "表字段信息表"},)
