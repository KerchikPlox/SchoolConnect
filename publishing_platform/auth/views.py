from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

import publishing_platform.auth.service as auth_service
from publishing_platform.auth.dto import Token
from publishing_platform.users.dto import UserFAPI

auth_router = APIRouter()


__all__ = [
    "auth_router",
]


@auth_router.post("/sign_in", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.provide_auth(form_data.username, form_data.password)


@auth_router.get("", response_model=UserFAPI)
async def get_me(current_user: UserFAPI = Depends(auth_service.get_current_active_user)):
    return current_user
