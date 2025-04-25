from fastapi import FastAPI, status, Response, Path, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse


from src.regusers.router import router_reg
from src.showcase.router import router_showcase
from src.showcase.router_chat import router_showcase_chat
from src.showcase.router_api import router_showcase_api
from src.regusers.router_api import router_reg_api

#fastapi users - пока не юзаю
# from fastapi_users import FastAPIUsers#это иморт класса с роутерами для авторизации, регистрации и тд.
# from regusers.auth import auth_backend
# from regusers.manager import get_user_manager
# from regusers.models import User
# from regusers.schemas import UserRead, UserCreate

# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

# useEffect(() => {
#         synchro()
#       }, [])



app = FastAPI(title="Витрина интернет магазина", debug=True)#debug=True это для того чтобы в документации выводилсь ошибки как в консоли. 




app.mount("/static", StaticFiles(directory="src/static"), name="static")
#пояснения к статичным файлам
# ("папка из фаст апи вшитая", StaticFiles(directory="путь к папке со статичными файлами"), name="имя")

#тут подключается роутер
app.include_router(router_showcase)
app.include_router(router_showcase_chat)
app.include_router(router_reg)
app.include_router(router_showcase_api)
app.include_router(router_reg_api)

origins = [
    "http://localhost:5173",    
   ]
# "http://127.0.0.1:5173",




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#fastapi users - пока не юзаю
# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

#fastapi users - пока не юзаю
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )

# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )


# КОМАНДА ЗАПУСКА ВЕБ СЕРВЕРА: uvicorn main:app --reload
#uvicorn это команда запуска сервера, main - это название файла входа, app - это название объекта приложения. --reload это автоматический перезапуск приложения

#pip install fastapi[all] - это установка фастапи



# from typing import Annotated
# from fastapi.security import OAuth2PasswordBearer

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

#скачивание файла
# from fastapi.responses import FileResponse

# @app.get("/file/download")
# def download_file():
#   return FileResponse(path='data.xlsx', filename='Статистика покупок.xlsx', media_type='multipart/form-data')



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)

#без fast-api users
# https://www.youtube.com/watch?v=qKlq8TPrrbI&t=24s

#с fast-api users
# https://www.youtube.com/watch?v=nfueh3ei8HU&t=762s







# Если ты хочешь проект, как сейчас делают большие дяди, то гугли:
# 1. Что такое SPA и SSR
# 2. React/Vue
# 3. DRF
# 4. Как связать фронт с бэком через API.
















