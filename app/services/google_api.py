from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Create spreadsheets on Google service account."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Set read-write role to user gmail account on specified spreadsheet."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        closed_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Update specified spreadsheet with information from database."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in closed_projects:
        new_row = [
            project['name'],
            str(timedelta(seconds=project['diff_seconds'])),
            project['description']
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
