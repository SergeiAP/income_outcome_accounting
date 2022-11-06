# pylint: disable=missing-module-docstring
from fastapi import FastAPI
from .api import router


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Authentification and Registration',
    },
    {
        'name': 'operations',
        'description': 'Handle financial operations',
    },
    {
        'name': 'reports',
        'description': 'Upload/download .csv operations reports',
    }
]


app = FastAPI(
    title="Income outcome accounting",
    description="Service to accounting for personal income and expenses in FastAPI",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.include_router(router)
