from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation
from app.crud.charity_project import charity_project_crud
from app.services.utils import close_obj


async def new_donate_investment(
        donate: Donation,
        session: AsyncSession
) -> Donation:
    """Invests a new donation in already open projects."""

    not_closed_projects = await charity_project_crud.get_not_closed(session)
    available_funds = donate.full_amount

    for project in not_closed_projects:
        needed_funds = project.full_amount - project.invested_amount
        if needed_funds == available_funds:
            close_obj(project)
            close_obj(donate)
            return donate
        elif needed_funds > available_funds:
            project.invested_amount += available_funds
            close_obj(donate)
            return donate
        else:
            close_obj(project)
            available_funds -= needed_funds

    donate.invested_amount = donate.full_amount - available_funds
    return donate
