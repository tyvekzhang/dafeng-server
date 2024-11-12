"""Connection domain schema"""

from pydantic import BaseModel


class ConnectionAdd(BaseModel):
    pass


class ConnectionQuery(BaseModel):
    pass


class ConnectionExport(BaseModel):
    pass


class ConnectionQueryForm(BaseModel):
    pass


class ConnectionModify(BaseModel):
    pass
