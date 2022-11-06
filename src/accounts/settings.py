# pylint: disable=missing-module-docstring
from pydantic import BaseSettings


# TODO: add '/info'
# it is also possible to use env vars and .env
class Settings(BaseSettings):
    """Typical settings based on Pydantic"""
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = 'sqlite:///./src/database.sqlite3'

    jwt_secret: str = 'pass'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # in seconds

    class Config:
        """Config to set .env file uploading"""
        env_file = './src/app/.env'
        env_file_encoding='utf-8'


settings = Settings()
