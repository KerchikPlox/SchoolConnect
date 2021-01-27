from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import publishing_platform.users.service as users_service
from publishing_platform.auth.service import validate_token_dependency
from publishing_platform.repo.common.common_dto import UpdateRatingFAPI
from publishing_platform.users.dto import *

users_router = APIRouter()


__all__ = [
    "users_router",
]


@users_router.get("", response_model=List[UserFAPI])  # noqa
async def get_users_all():
    return await users_service.get_users_all()


@users_router.post("", response_model=UserAndTokenFAPI)
async def create_user(add_user_info: AddUserFAPI) -> UserAndTokenFAPI:
    return await users_service.create_user(add_user_info)


@users_router.put("/rating")
async def update_user_rating(rating: UpdateRatingFAPI, _=Depends(validate_token_dependency)):
    await users_service.update_user_rating(rating)


@users_router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    await users_service.delete_user(user_id)


@users_router.get("/{user_id}", response_model=UserFAPI)
async def get_user_by_id(user_id: UUID):
    return await users_service.get_user_by_id(user_id)
