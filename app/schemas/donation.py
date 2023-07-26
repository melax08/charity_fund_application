from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationUserDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperUserDB(DonationUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
