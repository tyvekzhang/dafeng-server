"""Table domain schema"""

from pydantic import BaseModel


class TableAdd(BaseModel):
    pass


class TableQuery(BaseModel):
    pass


class TableExport(BaseModel):
    pass


class TableQueryForm(BaseModel):
    pass


class TableModify(BaseModel):
    pass
