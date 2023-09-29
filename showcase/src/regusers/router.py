from fastapi import Form, APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse

from sqlalchemy import insert, select

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from config import templates
from .models import *
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
# OAuth2PasswordRequestForm - это форма для авторизации из фастапи



from pydantic import BaseModel





router = APIRouter(
    prefix="",
    tags=["Regusers"]
)



#получение инфы об авторизованном пользователе

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # @router.get("/")
# # async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
# #     return {"token": token}

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# def fake_decode_token(token):    
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user


# @router.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     print(current_user)
#     return current_user


############################################################################
#авторизация!!!!!!!! третья часть доки про авторизацию

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}







def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# OAuth2PasswordRequestForm
# OAuth2PasswordRequestFormStrict
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user




#конец третьей части
############################################################################





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





################################################################################
#просто ссылки для перехода на страницу тестовой авторизации. Потом удалить.
@router.get("/")
async def url_reg(request: Request):
    return RedirectResponse("/auth/registration", status_code=303)


@router.get("/")
async def url_auth(request: Request):
    return RedirectResponse("/auth/users/me", status_code=303)
################################################################################
