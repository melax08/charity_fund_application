from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charity_project import ProjectCreate, ProjectDB, ProjectUpdate
from app.core.user import current_superuser
from app.api.validators import (check_name_duplicate,
                                check_project_before_delete,
                                check_project_before_update)
from app.crud.charity_project import charity_project_crud
from app.services.charity_project import new_project_investment

router = APIRouter()


@router.post(
    '/',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_project(
        project: ProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.

    Create charity project.
    """
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project,
        session,
        investment_func=new_project_investment
    )
    return new_project


@router.get(
    '/', response_model=List[ProjectDB], response_model_exclude_none=True
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Get the list of all charity projects."""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)

):
    """
    Only for superusers.
    - You can't delete projects with invested_amount > 0.
    """
    project = await check_project_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        obj_in: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Only for superusers.
    - You can't modify closed project.
    - You can't set full amount lower than already invested amount.
    """
    project = await check_project_before_update(
        project_id,
        obj_in.full_amount,
        session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(project, obj_in, session)
    return project
