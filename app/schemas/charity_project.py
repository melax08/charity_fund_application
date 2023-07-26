from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator, Extra

from app.core.constants import MAX_PROJECT_NAME


class ProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=MAX_PROJECT_NAME)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class ProjectUpdate(ProjectBase):
    pass

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError("Name field can't be null!")
        return value

    @validator('description')
    def description_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError("Description field can't be null!")
        return value


class ProjectCreate(ProjectBase):
    name: str = Field(..., max_length=MAX_PROJECT_NAME)
    description: str
    full_amount: PositiveInt


class ProjectDB(ProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config(ProjectCreate.Config):
        orm_mode = True
