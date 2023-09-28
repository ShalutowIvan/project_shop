from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse

from sqlalchemy import insert, select

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from config import templates
from .models import *
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

@router.get("/registration")
async def registration_get(request: Request):
    return templates.TemplateResponse("regusers/test.html", {"request": request})

# username: str = Form(...), password: str = Form(...)

@router.post("/registration")
async def registration_post(request: Request, session: AsyncSession = Depends(get_async_session), name: str = Form(), email: str = Form(), password: str = Form()):
    # stmt = await session.execute(select(users))
    stmt = insert(users).values(email=email, name=name, password=password)
    # user = stmt.users(email=email, name=name, password=password)
    await session.execute(stmt)
    await session.commit()


    return RedirectResponse("/auth/registration", status_code=303)


@router.get("/")
async def url_reg(request: Request):
    return RedirectResponse("/auth/registration", status_code=303)


