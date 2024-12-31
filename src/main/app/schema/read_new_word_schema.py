"""NewWord domain schema"""
import random
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase, PageQuery


class NewWordAdd(BaseModel):
    pass


class NewWordQuery(PageQuery):
    word: Optional[str] = None


class NewWordQueryResponse(BaseModel):
    id: int
    word: str = uuid.uuid4()
    nextReviewDate: datetime = datetime.now()
    userId: int =  random.randint(1, 70)
    articleId: int =  random.randint(1, 6)
    wordId: int =  random.randint(1, 60)
    reviewCount: int =  random.randint(1, 60)
    tenantId: int =  random.randint(1, 60)


class NewWordExport(BaseModel):
    word: str = uuid.uuid4()
    nextReviewDate: datetime = datetime.now()
    userId: int =  random.randint(1, 70)
    articleId: int =  random.randint(1, 6)
    wordId: int =  random.randint(1, 60)
    reviewCount: int =  random.randint(1, 60)
    tenantId: int =  random.randint(1, 60)

class NewWordCreate(BaseModel):
    word: str = str(uuid.uuid4())[:6]
    nextReviewDate: datetime = datetime.now()
    userId: int =  random.randint(1, 70)
    articleId: int =  random.randint(1, 6)
    wordId: int =  random.randint(1, 60)
    reviewCount: int =  random.randint(1, 60)
    tenantId: int =  random.randint(1, 60)



class NewWordQueryForm(BaseModel):
    ids: List[int]


class NewWordModify(BaseModel):
    id: int
    word: str

class NewWordBatchModify(BaseModel):
    ids: List[int]
    word: str
