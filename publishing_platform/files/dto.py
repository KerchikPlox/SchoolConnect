import datetime
from uuid import UUID

from pydantic import BaseModel, validator

from publishing_platform.repo.base_validators import datetime_validator
from publishing_platform.users.enums import *

__all__ = [
    "FileFAPI",
    "SendFileFAPI",
]


class FileFAPI(BaseModel):

    id: UUID
    user_id: UUID
    file: bytes
    role: Roles
    sent_at: datetime.datetime

    @validator("sent_at", pre=True, always=True)
    def set_sent_at(cls, var):  # noqa
        return datetime_validator(var)


class SendFileFAPI(BaseModel):
    user_id: UUID
