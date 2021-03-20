from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse

import publishing_platform.auth.service as auth_service
from publishing_platform.auth.dto import Token
from publishing_platform.users.dto import UserFAPI
from publishing_platform.app import templates

auth_router = APIRouter()


__all__ = [
    "auth_router",
]


@auth_router.post("/sign_in", response_model=Token, response_class=HTMLResponse)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    return templates.TemplateResponse('login.html', {'form_data': form_data, 'title': 'авторизация', 'request': request})


@auth_router.get("/get_me", response_model=UserFAPI)
async def get_me(current_user: UserFAPI = Depends(auth_service.get_current_active_user)):
    return current_user
