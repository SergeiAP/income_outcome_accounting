# pylint: disable=missing-module-docstring
from fastapi import FastAPI
from .api import router


app = FastAPI()
app.include_router(router)
