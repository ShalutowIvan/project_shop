from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse

from sqlalchemy import insert, select

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from regusers.models import *
from config import templates
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer



router = APIRouter(
    prefix="/auth",
    tags=["Regusers"]
)


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# @router.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}



# @router.post("/login")
# async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
#     return {"username": username}

@router.get("/")
async def read_items(request: Request):
    return templates.TemplateResponse("regusers/test.html", {"request": request})


@router.post("/my_form")
async def login(username: str = Form(...), password: str = Form(...)):
	
    return RedirectResponse("/", status_code=303)


