"""NewWord schema"""
import random
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageQuery


class NewWordQuery(PageQuery):
    pass

class NewWordPage(BaseModel):
    pass

class NewWordDetail(BaseModel):
    pass

class NewWordCreate(BaseModel):
    err_msg: str = Optional[str]

class NewWordExport(BaseModel):
    word: str = uuid.uuid4()
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
