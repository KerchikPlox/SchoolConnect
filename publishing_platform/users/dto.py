import datetime
from uuid import UUID

from pydantic import BaseModel, validator

from typing import Optional

from publishing_platform.auth.dto import Token
from publishing_platform.repo.base_validators import datetime_validator
from publishing_platform.users.enums import *

__all__ = [
    "UserFAPI",
    "AddUserFAPI",
    "UserAndTokenFAPI",
    "UpdateUserFAPI"
]


class UserFAPI(BaseModel):

    id: UUID
    login: str
    author_name: str
    created_at: datetime.datetime
    role: Roles

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, var):  # noqa
        return datetime_validator(var)


class AddUserFAPI(BaseModel):
    login: str
    password: str
    author_name: str
    role: Roles


class UpdateUserFAPI(BaseModel):
    login: Optional[str] = None
    author_name: str
    role: Optional[Roles] = None


class UserAndTokenFAPI(BaseModel):
    user: UserFAPI
    token: Token
