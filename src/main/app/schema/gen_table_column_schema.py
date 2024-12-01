"""GenTableColumn domain schema"""

from typing import Optional

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase


class GenTableColumnAdd(BaseModel):
    pass


class GenTableColumnQuery(PageBase):
    pass


class GenTableColumnQueryResponse(BaseModel):
    pass


class GenTableColumnExport(BaseModel):
    pass


class GenTableColumnQueryForm(BaseModel):
    pass


class GenTableColumnModify(BaseModel):
    pass
