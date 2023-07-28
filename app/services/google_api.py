from typing import List
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT

TABLE_VALUES: List[list] = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

LIST_ROW_COUNT: int = 100
LIST_COLUMN_COUNT: int = 11
BODY_TEMPLATE: dict = dict(
    properties=dict(title='Отчет на ', locale='ru_RU'),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=LIST_ROW_COUNT,
            columnCount=LIST_COLUMN_COUNT
        )
    ))]
)
PERMISSION_BODY: dict = dict(
    type='user',
    role='writer',
    emailAddress=settings.email
)


def get_spreadsheet_body() -> dict:
    """Create spreadsheet body with current time."""
    spreadsheet_body = BODY_TEMPLATE.copy()
    spreadsheet_body['properties']['title'] += datetime.now().strftime(FORMAT)
    return spreadsheet_body


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Create spreadsheets on Google service account."""
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = get_spreadsheet_body()

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Set read-write role to user gmail account on specified spreadsheet."""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSION_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        closed_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Update specified spreadsheet with information from database."""
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = TABLE_VALUES.copy()
    table_values[0].append(datetime.now().strftime(FORMAT))
    table_values.extend(closed_projects)

    if len(table_values) > LIST_ROW_COUNT:
        raise RuntimeError(
            f'Количество строк в отчете больше допустимого лимита: '
            f'{LIST_ROW_COUNT}'
        )

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:E{LIST_ROW_COUNT}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
