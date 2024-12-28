# теория в видео
# https://www.youtube.com/watch?v=GrQR4VhRsNA&t=1712s
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from src.regusers.models import User
from src.settings import templates
from src.regusers.secure import test_token_expire, access_token_decode

from jose.exceptions import ExpiredSignatureError

import requests



router_showcase_chat = APIRouter(
    prefix="",
    tags=["Showcase_chat"]
)



# Логика: при написании одним человеком будет видно всем людям в чате












