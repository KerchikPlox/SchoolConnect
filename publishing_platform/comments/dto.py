import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from publishing_platform.repo.base_validators import datetime_validator

__all__ = [
    "CommentFAPI",
    "AddCommentFAPI",
]


class CommentFAPI(BaseModel):

    id: UUID
    author_id: Optional[UUID]
    author_name: Optional[str]
    article_id: UUID
    reply_to: Optional[UUID]
    text: str
    created_at: datetime.datetime
    rating: int
    anonymous: bool

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, var):  # noqa
        return datetime_validator(var)


class AddCommentFAPI(BaseModel):

    author_id: Optional[UUID]
    article_id: UUID
    reply_to: Optional[UUID]
    text: str
    anonymous: bool
