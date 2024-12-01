"""GenTable domain schema"""

from typing import Optional, List

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase


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
