"""User operation mapper"""

from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.user_model import UserDO


class UserMapper(SqlModelMapper[UserDO]):
    async def get_user_by_username(
        self, *, username: str, db_session: Union[AsyncSession, None] = None
    ) -> Union[UserDO, None]:
        """
        Retrieve a user record by username.

        Args:
            username (str): The username to query.
            db_session (AsyncSession or None, optional): The database session instance. If None, use the default
            session.

        Returns:
            Union[UserDO, None]: The UserDO instance if found, otherwise None.
        """
        db_session = db_session or self.db.session
        user = await db_session.exec(select(UserDO).where(UserDO.username == username))
        return user.one_or_none()

    async def get_user_by_usernames(
        self, *, usernames: list[str], db_session: Union[AsyncSession, None] = None
    ) -> Union[list[UserDO], None]:
        """
        Query user by usernames
        """
        db_session = db_session or self.db.session
        statement = select(UserDO).where(UserDO.username.in_(usernames))
        results = await db_session.exec(statement)
        return results.all()


userMapper = UserMapper(UserDO)
