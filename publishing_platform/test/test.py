from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse

from publishing_platform.auth.service import get_current_user
from publishing_platform.auth.dto import Token
from publishing_platform.users.dto import UserFAPI
from publishing_platform.app import templates


auth_router = APIRouter()


@auth_router.post("/lk", response_model=Token, response_class=HTMLResponse)
async def lk(request: Request, user: get_current_user()):
    return templates.TemplateResponse('user_profile.html', {'user': user, 'title': 'авторизация', 'request': request})