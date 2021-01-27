from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import publishing_platform.comments.service as comments_service
from publishing_platform.auth.service import validate_token_dependency
from publishing_platform.comments.dto import CommentFAPI, AddCommentFAPI
from publishing_platform.repo.common.common_dto import UpdateRatingFAPI

comments_router = APIRouter()


__all__ = [
    "comments_router",
]


@comments_router.post("", response_model=CommentFAPI)
async def create_comment(add_comment_info: AddCommentFAPI) -> CommentFAPI:
    return await comments_service.create_comment(add_comment_info)


@comments_router.get("", response_model=List[CommentFAPI])  # noqa
async def get_comments_all():
    return await comments_service.get_comments_all()


@comments_router.put("/rating")
async def update_comment_rating(rating: UpdateRatingFAPI, _=Depends(validate_token_dependency)):
    await comments_service.update_comment_rating(rating)


@comments_router.delete("/{comment_id}")
async def delete_comment(comment_id: UUID, _=Depends(validate_token_dependency)):
    await comments_service.delete_comment(comment_id)


@comments_router.get("/{comment_id}", response_model=CommentFAPI)
async def get_comment_by_id(comment_id: UUID):
    return await comments_service.get_comment_by_id(comment_id)
