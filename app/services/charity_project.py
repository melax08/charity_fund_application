from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.crud.donation import donation_crud
from app.services.utils import close_obj


async def new_project_investment(
        project: CharityProject,
        session: AsyncSession
) -> CharityProject:
    """Invests existing donations into a new project."""

    not_closed_donations = await donation_crud.get_not_closed(session)
    needed_funds = project.full_amount

    for donate in not_closed_donations:
        available_funds = donate.full_amount - donate.invested_amount
        needed_funds = needed_funds - available_funds
        if needed_funds <= 0:
            available_funds = abs(needed_funds)
            if not needed_funds:
                close_obj(donate)
            else:
                donate.invested_amount = donate.full_amount - available_funds
            close_obj(project)
            return project
        else:
            close_obj(donate)

    project.invested_amount = project.full_amount - needed_funds

    return project
