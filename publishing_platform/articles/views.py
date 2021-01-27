from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Request

import publishing_platform.articles.service as articles_service
from publishing_platform.articles.dto import *
from publishing_platform.auth.service import validate_token_dependency
from publishing_platform.repo.common.common_dto import UpdateRatingFAPI

articles_router = APIRouter()


__all__ = [
    "articles_router",
]


@articles_router.post("", response_model=ArticleFAPI)
async def create_article(add_article_info: AddArticleFAPI, _=Depends(validate_token_dependency)) -> ArticleFAPI:
    return await articles_service.create_article(add_article_info)


@articles_router.get("", response_model=List[ArticleFAPI])  # noqa
async def get_articles_all():
    return await articles_service.get_articles_all()


@articles_router.get("/rich", response_model=List[RichArticleFAPI])  # noqa
async def get_articles_all_rich(request: Request):
    return await articles_service.get_articles_all_rich(request)


@articles_router.put("/rating")
async def update_article_rating(rating: UpdateRatingFAPI, _=Depends(validate_token_dependency)):
    await articles_service.update_article_rating(rating)


@articles_router.delete("/{article_id}")
async def delete_article(article_id: UUID, _=Depends(validate_token_dependency)):
    await articles_service.delete_article(article_id)


@articles_router.get("/{article_id}", response_model=ArticleFAPI)
async def get_article_by_id(article_id: UUID):
    return await articles_service.get_article_by_id(article_id)


@articles_router.get("/{article_id}/read", response_model=ArticleTreeFAPI)
async def read_article(article_id: UUID) -> ArticleTreeFAPI:
    return await articles_service.read_article(article_id)
