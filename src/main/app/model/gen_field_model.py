"""Gen table column data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    BigInteger,
    Boolean,
    SmallInteger
)
from src.main.app.model.model_base import ModelBase, ModelExt


class GenFieldBase(SQLModel):
    db_field_id: int = Field(sa_column=Column(BigInteger, nullable=False, index=True, comment="数据库字段id"))
    field_name: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="字段名称"))
    field_type: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="字段类型"))
    js_type: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="JS类型"))
    primary_key: Optional[int] = Field(default=0, sa_column=Column(SmallInteger, comment="是否主键(0否,1是)"))
    creatable: Optional[int] = Field(default=0, sa_column=Column(SmallInteger, comment="是否创建字段(0否,1是)"))
    queryable: Optional[int] = Field(default=0, sa_column=Column(SmallInteger, comment="是否查询字段(0否,1是)"))
    pageable: Optional[int] = Field(default=0, sa_column=Column(SmallInteger, comment="是否列表字段(0否,1是)"))
    detailable: Optional[int] = Field(default=0, sa_column=Column(SmallInteger, comment="是否详情字段(0否,1是)"))
    modifiable: Optional[int] = Field(default=0, sa_column=Column(SmallInteger, comment="是否修改字段(0否,1是)"))
    query_type: Optional[str] = Field(default=0, sa_column=Column(String(64), comment="查询方式（等于、不等于、大于、小于、范围）"))
    html_type: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="显示类型(文本框、文本域、下拉框、复选框、单选框、日期控件)"))
    dict_type: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="字典类型"))


class GenFieldDO(ModelExt, GenFieldBase, ModelBase, table=True):
    __tablename__ = "gen_field"
    __table_args__ = ({"comment": "代码生成字段表"},)
