"""NewWord domain schema"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase, PageQuery


class NewWordAdd(BaseModel):
    pass


class NewWordQuery(PageQuery):
    word: Optional[str] = None


class NewWordQueryResponse(BaseModel):
    word: str
    nextReviewDate: datetime


class NewWordExport(BaseModel):
    pass


class NewWordQueryForm(BaseModel):
    pass


class NewWordModify(BaseModel):
    pass
