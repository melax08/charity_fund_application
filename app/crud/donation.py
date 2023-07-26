from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    """Extended CRUD class with operations related to donation actions."""

    @staticmethod
    async def get_current_user_donations(
            user_id: int,
            session: AsyncSession
    ) -> List[Donation]:
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id))
        return user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
