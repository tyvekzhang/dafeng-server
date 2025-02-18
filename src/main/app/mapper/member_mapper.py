"""Member mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.member_model import MemberDO


class MemberMapper(SqlModelMapper[MemberDO]):
    pass


memberMapper = MemberMapper(MemberDO)