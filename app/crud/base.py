from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """CRUD class with base operations."""

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            investment_func=None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        if investment_func:
            db_obj = await investment_func(db_obj, session)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_not_closed(self, session: AsyncSession):
        objects = await session.execute(
            select(self.model).where(self.model.fully_invested == False))  # noqa
        return objects.scalars().all()
