from fastapi import APIRouter

from app.api.endpoints import (
    user_router,
    project_router,
    donation_router,
    google_api_router
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    project_router, prefix='/charity_project', tags=['Projects']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)
main_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)
