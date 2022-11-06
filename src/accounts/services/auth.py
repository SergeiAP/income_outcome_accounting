# pylint: disable=missing-module-docstring
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..tables import User as TablesUser
from ..models.auth import User as ModelsUser, Token, UserCreate
from ..settings import settings
from ..database import get_session


# '/auth/sign-in/' - redirect url if no token provided
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth_scheme)) -> ModelsUser:
    """Check token in the url, return user if ok. If no token - redicrect to 
    `/auth/sign-in/`

    Args:
        token (str, optional): token itself. Defaults to Depends(oauth_scheme).

    Returns:
        models.auth.user: user data
    """
    return AuthService.validate_token(token)


class AuthService:
    """Class to handle authentification processes"""
    @classmethod
    def verify_password(cls, plain_pwd: str, hashed_pwd: str) -> bool:
        """Check password by it's hash in database

        Args:
            plain_pwd (str): raw password
            hashed_pwd (str): hashed transformed password

        Returns:
            bool: verify or not
        """
        return bcrypt.verify(plain_pwd, hashed_pwd)

    @classmethod
    def hash_password(cls, pwd: str) -> str:
        """Hash password

        Args:
            pwd (str): raw password

        Returns:
            str: hashed password
        """
        return bcrypt.hash(pwd)

    @classmethod
    def validate_token(cls, token: str) -> ModelsUser:
        """Method to check token in request

        Args:
            token (str): token to validate

        Raises:
            exeption: if token is incorrect

        Returns:
            models.auth.User: user data
        """
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError as e:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = ModelsUser.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: TablesUser) -> Token:
        """Create token based on system jwt fields and user data

        Args:
            user (tables.User): user data

        Returns:
            Token: generated token
        """
        user_data = ModelsUser.from_orm(user)

        now = datetime.utcnow()
        payload = {
            # Token created time
            'iat': now,
            # Token working start date
            'nbf': now,
            # Token expiration date
            'exp': (now + timedelta(seconds=settings.jwt_expiration)),
            # All info related to the user
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        """Register new user and return hist token

        Args:
            user_data (models.auth.UserCreate): user info

        Returns:
            Token: token with specific expiration datetime
        """
        user = TablesUser(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password)
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authentificate_user(self, username: str, password: str) -> Token:
        """Generate time limited token

        Args:
            username (str): username in database
            password (str): password

        Raises:
            exception: incorrect username or password

        Returns:
            Token: generated token
        """
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        user = (
            self.session
            .query(TablesUser)
            .filter(TablesUser.username == username)
            .first()
        )

        if not user:
            raise exception from None

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
