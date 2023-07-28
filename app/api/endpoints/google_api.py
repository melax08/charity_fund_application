from aiogoogle import Aiogoogle
from aiogoogle.excs import AiogoogleError
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value
)
from app.core.constants import SPREADSHEETS_URL

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """
    Only for superusers.
    Get a report on the fastest closed projects.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)
    try:
        spreadsheet_id = await spreadsheets_create(wrapper_services)
        await set_user_permissions(spreadsheet_id, wrapper_services)
        await spreadsheets_update_value(
            spreadsheet_id,
            projects,
            wrapper_services
        )
    except RuntimeError as error:
        return str(error)
    except AiogoogleError:
        return ('Возникла ошибка при генерации google-таблицы. '
                'Попробуйте создать отчет позже.')
    return SPREADSHEETS_URL + spreadsheet_id
