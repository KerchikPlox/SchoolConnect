import datetime
from typing import Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext

from publishing_platform.auth.dto import *
from publishing_platform.auth.exceptions import validation_exception, incorrect_auth_data_exception
from publishing_platform.constants import JWT_ALGORITHM, JWT_SECRET
from publishing_platform.users.dto import *
from publishing_platform.users.models import *

__all__ = [
    "get_password_hash",
    "create_access_token",
    "provide_auth",
    "validate_token_dependency",
    "get_current_user",
    "get_current_active_user",
]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign_in")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ##### #####
# ======================================== Crypto functions ========================================


def verify_password(plain_password, password_hash) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> bytes:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt


# ##### #####
# ======================================== Dependency ========================================


async def validate_token_dependency(token: str = Depends(oauth2_scheme)) -> None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise validation_exception
    except PyJWTError:
        raise validation_exception


# ##### #####
# ======================================== Service ========================================


async def provide_auth(username: str, password: str) -> dict:
    user = await authenticate_user(username, password)

    if user is None:
        raise incorrect_auth_data_exception

    access_token = create_access_token(data={"sub": user.login},)

    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate_user(username: str, password: str) -> Optional[UserFAPI]:

    user: Optional[UserIdentity] = (await UserIdentity.query.where(UserIdentity.login == username).gino.first())

    if user is None:
        return None

    if verify_password(password, user.password_hash) is False:
        return None

    user: UserFAPI = UserFAPI(**(await User.query.where(User.login == username).gino.first()).to_dict())
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserFAPI:

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise validation_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise validation_exception

    user = await User.query.where(User.login == token_data.username).gino.first()

    if user is None:
        raise validation_exception

    user = UserFAPI(**user.to_dict())
    return user


async def get_current_active_user(current_user: UserFAPI = Depends(get_current_user)) -> UserFAPI:
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
