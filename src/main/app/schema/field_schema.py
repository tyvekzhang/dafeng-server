"""Field domain schema"""

from typing import Optional

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase


class FieldAdd(BaseModel):
    table_id: int
    name: str
    type: str
    default: Optional[int] = None
    length: Optional[int] = None
    decimals: Optional[int] = None
    not_null: Optional[bool] = None
    key: Optional[bool] = None
    remark: Optional[str] = None


class FieldQuery(PageBase):
    table_id: int


class FieldExport(BaseModel):
    pass


class FieldQueryForm(BaseModel):
    pass


class FieldModify(BaseModel):
    pass


class FieldGenerate(BaseModel):
    name: str
    type: str
    modeltype: Optional[str] = None
    server_type: Optional[str] = None
    default: Optional[int] = None
    length: Optional[int] = None
    decimals: Optional[int] = None
    not_null: Optional[bool] = None
    key: Optional[bool] = None
    remark: Optional[str] = None