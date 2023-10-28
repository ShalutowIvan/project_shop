from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse

from sqlalchemy import insert, select

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


from .models import *
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# OAuth2PasswordRequestForm - это форма для авторизации из фастапи

from .schemas import *



#мой роутер
router_reg = APIRouter(
    prefix="",
    tags=["Regusers"]
)






#роутеры для реги


@router_reg.get("/registration")
async def registration_get(request: Request):
    return templates.TemplateResponse("regusers/test.html", {"request": request})

# username: str = Form(...), password: str = Form(...)

#функция из видоса. 
# def reg(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
# ост 22 мин.


@router_reg.post("/registration", response_model=UserCreate, status_code=201)
async def registration_post(request: Request, session: AsyncSession = Depends(get_async_session), name: str = Form(), email: str = Form(), password: str = Form()):
    # stmt = await session.execute(select(users))
    stmt = insert(users).values(email=email, name=name, password=password)
    # user = stmt.users(email=email, name=name, password=password)
    await session.execute(stmt)
    await session.commit()


    return RedirectResponse("/registration", status_code=303)

# сделать перезапись пароля в захешированный пароль. То есть берем пароль из формы и юзера создаем, потом хешируем и перезаписываем пароль в базу захешированным. 
#аннотейтед это такие аннотации со типом данных и значениями. В доке по фастапи есть инфа в питоне 3,8 как в метанит, а в питон 3,9 появились Annotated 




async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)



################################################################################
#просто ссылки для перехода на страницу тестовой авторизации. Потом удалить.
@router_reg.get("/auth")
async def url_reg(request: Request):
    return RedirectResponse("/auth", status_code=303)


@router_reg.get("/auth/jwt")
async def url_auth(request: Request):
    return RedirectResponse("auth/jwt", status_code=303)
################################################################################
