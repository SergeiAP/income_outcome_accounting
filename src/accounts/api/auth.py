# pylint: disable=missing-module-docstring
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..services.auth import AuthService, get_current_user

from ..models.auth import (
    User,
    UserCreate,
    Token,
)


router = APIRouter(
    prefix='/auth'
)


@router.post('/sign-up', response_model=Token)
def sign_up(user_data: UserCreate, service: AuthService = Depends(),) -> Token:
    """Registry process"""
    return service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(),
            service: AuthService = Depends(),
            ) -> Token:
    """Signing in"""
    return service.authentificate_user(
        form_data.username,
        form_data.password,
    )


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)) -> User:
    'Method to check user'
    return user
