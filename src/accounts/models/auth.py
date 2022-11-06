# pylint: disable=missing-module-docstring
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class BaseUser(BaseModel):
    """Base user class for other User models"""
    email: str
    username: str


class UserCreate(BaseUser):
    """Schema of user creation"""
    password: str


class User(BaseUser):
    """Schema of user in database"""
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    """Schema for tokens, obligatory fields according to Oauth2"""
    access_token: str           # for gwt token
    token_type: str = 'bearer'  # type of token as in Oauth2
