import datetime
from typing import List
from uuid import uuid4, UUID

from fastapi import Request
from gino import GinoConnection
from sqlalchemy.engine.result import RowProxy

from publishing_platform.articles.dto import *
from publishing_platform.articles.models import *
from publishing_platform.comments.dto import CommentFAPI
from publishing_platform.comments.models import Comment
from publishing_platform.repo.common.common_dto import UpdateRatingFAPI
from publishing_platform.repo.common.common_service import update_rating
from publishing_platform.users.models import User

__all__ = [
    "create_article",
    "get_article_by_id",
    "update_article_rating",
    "delete_article",
    "get_articles_all",
    "read_article",
]


async def create_article(add_article_info: AddArticleFAPI) -> ArticleFAPI:

    article = await Article.create(
        id=uuid4(),
        author_id=add_article_info.author_id,
        title=add_article_info.title,
        text=add_article_info.text,
        created_at=datetime.datetime.utcnow(),
        rating=0,
    )

    return ArticleFAPI(**article.to_dict())


async def get_article_by_id(article_id: UUID) -> ArticleFAPI:
    article = await Article.query.where(Article.id == article_id).gino.first_or_404()
    return ArticleFAPI(**article.to_dict())


async def update_article_rating(rating: UpdateRatingFAPI):
    await update_rating(rating, Article)

    article: Article = await Article.query.where(Article.id == rating.entity_id).gino.first()

    await update_rating(UpdateRatingFAPI(entity_id=article.author_id, value=rating.value), User)


async def delete_article(article_id: UUID) -> None:
    article = await Article.query.where(Article.id == article_id).gino.first_or_404()
    await article.delete()


async def get_articles_all() -> List[ArticleFAPI]:
    return [ArticleFAPI(**u.to_dict()) for u in await Article.query.gino.all()]


async def get_articles_all_rich(request: Request) -> List[RichArticleFAPI]:
    connection: GinoConnection = request["connection"]  # noqa

    async with connection.transaction():

        # language=PostgreSQL
        articles_joined: List[RowProxy] = await connection.all(
            """
            SELECT a.id, a.author_id, u.author_name, a.title, a.text, a.created_at, a.rating, count(c) as number_of_comments
            FROM articles a 
            JOIN users u on a.author_id = u.id
            JOIN comments c on a.id = c.article_id
            GROUP BY a.id, a.author_id, u.author_name, a.title, a.text, a.created_at, a.rating
        """
        )

    return [RichArticleFAPI(**a) for a in articles_joined]


async def read_article(article_id: UUID) -> ArticleTreeFAPI:
    article = await get_article_by_id(article_id)
    comments = await Comment.query.where(Comment.article_id == article_id).gino.all()

    return ArticleTreeFAPI(article=article, comments=[CommentFAPI(**c.to_dict()) for c in comments])
