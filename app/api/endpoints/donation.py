from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.donation import (
    DonationSuperUserDB,
    DonationUserDB,
    DonationCreate
)
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.services.donation import new_donate_investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationSuperUserDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.

    Get the list of all user donations.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Only for users.

    Make a donation.
    """
    new_donate = await donation_crud.create(
        donation,
        session,
        user,
        investment_func=new_donate_investment
    )
    return new_donate


@router.get('/my', response_model=List[DonationUserDB])
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Only for users.

    Get the list of current user donations.
    """
    donations = await donation_crud.get_current_user_donations(
        user.id,
        session
    )
    return donations
