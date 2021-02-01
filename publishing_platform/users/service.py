import datetime
from typing import List
from uuid import uuid4, UUID

from fastapi import HTTPException, status, Path

from publishing_platform.auth.dto import Token
from publishing_platform.auth.service import get_password_hash, create_access_token
from publishing_platform.repo.common.common_dto import UpdateRatingFAPI
from publishing_platform.repo.common.common_service import update_rating
from publishing_platform.users.dto import *
from publishing_platform.users.models import *

__all__ = [
    "create_user",
    "get_user_by_id",
    "update_user",
    "delete_user",
    "get_users_all",
]


async def create_user(add_user_info: AddUserFAPI) -> UserAndTokenFAPI:

    if await UserIdentity.query.where(UserIdentity.login == add_user_info.login).gino.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"ERROR! User with login {add_user_info.login} is already exists!",
        )

    await UserIdentity.create(
        id=uuid4(), login=add_user_info.login, password_hash=get_password_hash(add_user_info.password),
        role=add_user_info.role
    )

    user = await User.create(
        id=uuid4(),
        login=add_user_info.login,
        author_name=add_user_info.author_name,
        created_at=datetime.datetime.utcnow(),
        role=add_user_info.role,
    )

    access_token = create_access_token(data={"sub": user.login},)

    return UserAndTokenFAPI(
        user=UserFAPI(**user.to_dict()), token=Token(**{"access_token": access_token, "token_type": "bearer"})
    )


async def get_user_by_id(user_id: UUID) -> UserFAPI:
    user = await User.query.where(User.id == user_id).gino.first_or_404()
    return UserFAPI(**user.to_dict())


async def update_user(update_info: UpdateUserFAPI, user_id: UUID = Path(...)):
    await User.update.values(**update_info.dict(exclude_unset=True)).where(User.id == user_id).gino.status()


async def delete_user(user_id: UUID) -> None:
    user = await User.query.where(User.id == user_id).gino.first_or_404()
    user_identity = await UserIdentity.query.where(UserIdentity.login == user.login).gino.first_or_404()

    await user.delete()
    await user_identity.delete()


async def get_users_all() -> List[UserFAPI]:
    return [UserFAPI(**u.to_dict()) for u in await User.query.gino.all()]
