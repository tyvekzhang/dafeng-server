"""GenTable domain schema"""

from typing import Optional, List, Union

from pydantic import BaseModel

from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.common_schema import PageBase
from src.main.app.schema.gen_field_schema import FieldGen


class GenTableAdd(BaseModel):
    pass


class GenTableQuery(PageBase):
    pass


class GenTableQueryResponse(BaseModel):
    pass


class GenTableExport(BaseModel):
    pass


class GenTableQueryForm(BaseModel):
    pass


class GenTableModify(BaseModel):
    pass

class TableImport(BaseModel):
    database_id: int
    table_ids: List[int]

class TableGen(BaseModel):
    gen_table: Optional[GenTableDO]
    fields: Union[List[FieldGen], None]
    sub_table: Optional[GenTableDO] = None
    pk_field: Optional[FieldGen] = None
    tree_code: Optional[str] = None
    tree_parent_code: Optional[str] = None
    tree_name: Optional[str] = None
    parent_menu_id: Optional[int] = None
    parent_menu_name: Optional[str] = None
