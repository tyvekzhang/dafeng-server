"""NewWord domain schema"""
import random
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
    userId: int =  random.randint(1, 70)
    articleId: int =  random.randint(1, 6)
    wordId: int =  random.randint(1, 60)
    reviewCount: int =  random.randint(1, 60)
    tenantId: int =  random.randint(1, 60)


class NewWordExport(BaseModel):
    pass


class NewWordQueryForm(BaseModel):
    pass


class NewWordModify(BaseModel):
    pass
