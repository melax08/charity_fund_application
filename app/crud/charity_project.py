from datetime import timedelta
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """Extended CRUD class with operations related to charity projects."""

    @staticmethod
    async def get_project_id_by_name(
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(select(
            CharityProject.id).where(CharityProject.name == project_name))
        return project_id.scalars().first()

    @staticmethod
    async def remove(
            project_obj: CharityProject,
            session: AsyncSession
    ) -> CharityProject:
        await session.delete(project_obj)
        await session.commit()
        return project_obj

    @staticmethod
    async def update(db_obj, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def get_projects_by_completion_rate(
            session: AsyncSession
    ) -> list[list[str]]:
        closed_projects = await session.execute(
            select([CharityProject.name,
                    (func.extract('epoch',
                                  CharityProject.close_date) - func.extract(
                        'epoch', CharityProject.create_date)).label(
                        'diff_seconds'),
                    CharityProject.description]
                   ).where(
                CharityProject.fully_invested == True).order_by('diff_seconds')  # noqa
        )
        closed_projects = closed_projects.all()
        return list(map(
            lambda project: [
                project[0],
                str(timedelta(seconds=project[1])),
                project[2]
            ],
            closed_projects)
        )


charity_project_crud = CRUDCharityProject(CharityProject)
