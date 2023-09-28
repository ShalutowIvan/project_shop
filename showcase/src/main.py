from fastapi import FastAPI, status, Response, Path, Request

from fastapi.staticfiles import StaticFiles



# from models.models import *
from typing import List, Union
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse


from regusers.router import router as router_regusers
from showcase.router import router as router_showcase




# from fastapi import FastAPI, Request, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

# from config import Settings
# setting = Settings()
# openapi_url=setting.openapi_url,


app = FastAPI(title="Склад интернет магазина", debug=True)#debug=True это для того чтобы в документации выводилсь ошибки как в консоли. 


app.mount("/static", StaticFiles(directory="static"), name="static")



#тут подключается роутер
app.include_router(router_showcase)
app.include_router(router_regusers)


# КОМАНДА ЗАПУСКА ВЕБ СЕРВЕРА: uvicorn main:app --reload
#uvicorn это команда запуска сервера, main - это название файла входа, app - это название объекта приложения. --reload это автоматический перезапуск приложения

#pip install fastapi[all] - это установка фастапи








if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)



