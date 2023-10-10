from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.core.constants import MIN_INVESTED_AMOUNT


async def check_name_duplicate(name: str, session: AsyncSession) -> None:
    """Checks if a project with the specified name already exists."""
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        project_id: int, session: AsyncSession
) -> Optional[CharityProject]:
    """Checks if the specified project exists."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_before_delete(
        project_id: int, session: AsyncSession
) -> Optional[CharityProject]:
    """Checks if the specified project exists
    and whether there were investments in it."""
    project = await check_project_exists(project_id, session)

    if project.invested_amount > MIN_INVESTED_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_project_before_update(
        project_id: int, full_amount: Optional[int], session: AsyncSession
) -> Optional[CharityProject]:
    """Check if the specified project exists,
    is it closed and correct full amount set."""
    project = await check_project_exists(project_id, session)

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!"
        )

    if full_amount is not None and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=("Вы не можете установить общую сумму проекта меньше чем "
                    "уже внесенные средства.")
        )
    return project
