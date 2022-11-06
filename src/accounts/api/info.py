# pylint: disable=missing-module-docstring
from fastapi import APIRouter
from ..settings import settings


router = APIRouter(
    prefix='/info',
    tags=['info'],
)


@router.get("/")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "github_link": settings.github_link,
    }
