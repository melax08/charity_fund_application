from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.constants import (
    MIN_PASSWORD_LENGTH,
    JWT_TOKEN_LIFETIME,
    JWT_TOKEN_URL,
    JWT_BACKEND_NAME
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl=JWT_TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=JWT_TOKEN_LIFETIME
    )


auth_backend = AuthenticationBackend(
    name=JWT_BACKEND_NAME,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason=(f'Password should be at least '
                        f'{MIN_PASSWORD_LENGTH} characters')
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
