import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, validator

from publishing_platform.comments.dto import CommentFAPI
from publishing_platform.repo.base_validators import datetime_validator

__all__ = [
    "ArticleFAPI",
    "AddArticleFAPI",
    "ArticleTreeFAPI",
    "RichArticleFAPI",
]


class ArticleFAPI(BaseModel):

    id: UUID
    author_id: UUID
    title: str
    text: str
    created_at: datetime.datetime
    rating: int

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, var):  # noqa
        return datetime_validator(var)


class AddArticleFAPI(BaseModel):

    author_id: UUID
    title: str
    text: str


class ArticleTreeFAPI(BaseModel):
    article: ArticleFAPI
    comments: List[CommentFAPI]


class RichArticleFAPI(ArticleFAPI):
    number_of_comments: int
    author_name: str
