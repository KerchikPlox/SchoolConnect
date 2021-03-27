from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from pip._vendor.requests import Response

import publishing_platform.auth.service as auth_service
from publishing_platform.auth.dto import Token
from publishing_platform.users.dto import UserFAPI
from publishing_platform.app import templates

auth_router = APIRouter()


__all__ = [
    "auth_router",
]


@auth_router.post("/sign_in", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.provide_auth(form_data.username, form_data.password)
    # return templates.TemplateResponse('login_form.html', {'form_data': form_data, 'title': 'авторизация',
    # 'request': request})


@auth_router.get("/get_me", response_model=UserFAPI)
async def get_me(current_user: UserFAPI = Depends(auth_service.get_current_active_user)):
    return current_user
