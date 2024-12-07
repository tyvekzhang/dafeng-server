"""GenField mapper"""
from typing import Union, List, Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.gen_field_model import GenFieldDO


class GenFieldMapper(SqlModelMapper[GenFieldDO]):
    async def select_by_db_field_ids(self, *, ids: List[int], db_session: Union[AsyncSession, None] = None) -> List[GenFieldDO]:
        db_session = db_session or self.db.session
        stmt = select(GenFieldDO).where(self.model.db_field_id.in_(ids))
        exec_result = await db_session.exec(stmt)
        return exec_result.all()



genFieldMapper = GenFieldMapper(GenFieldDO)
