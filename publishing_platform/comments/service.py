import datetime
from typing import List
from uuid import uuid4, UUID

from publishing_platform.comments.dto import *
from publishing_platform.comments.models import *
from publishing_platform.repo.common.common_dto import UpdateRatingFAPI
from publishing_platform.repo.common.common_service import update_rating
from publishing_platform.users.models import User

__all__ = [
    "create_comment",
    "get_comment_by_id",
    "update_comment_rating",
    "delete_comment",
    "get_comments_all",
]


async def create_comment(add_comment_info: AddCommentFAPI) -> CommentFAPI:

    author: User = await User.query.where(User.id == add_comment_info.author_id).gino.first()

    comment = await Comment.create(
        id=uuid4(),
        author_id=add_comment_info.author_id,
        author_name=author.author_name,
        article_id=add_comment_info.article_id,
        reply_to=add_comment_info.reply_to,
        text=add_comment_info.text,
        created_at=datetime.datetime.utcnow(),
        rating=0,
        anonymous=add_comment_info.anonymous,
    )

    return CommentFAPI(**comment.to_dict())


async def get_comment_by_id(comment_id: UUID) -> CommentFAPI:
    comment = await Comment.query.where(Comment.id == comment_id).gino.first_or_404()
    return CommentFAPI(**comment.to_dict())


async def update_comment_rating(rating: UpdateRatingFAPI):
    await update_rating(rating, Comment)

    comment: Comment = await Comment.query.where(Comment.id == rating.entity_id).gino.first()

    if comment.anonymous is False and comment.author_id is not None:
        await update_rating(UpdateRatingFAPI(entity_id=comment.author_id, value=rating.value), User)


async def delete_comment(comment_id: UUID) -> None:
    comment = await Comment.query.where(Comment.id == comment_id).gino.first_or_404()
    await comment.delete()


async def get_comments_all() -> List[CommentFAPI]:
    return [CommentFAPI(**u.to_dict()) for u in await Comment.query.gino.all()]
