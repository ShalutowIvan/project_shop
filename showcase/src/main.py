from fastapi import FastAPI, status, Response, Path, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



# from models.models import *
from typing import List, Union
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse


# from regusers.router import router as router_regusers
# from showcase.router import router as router_showcase





# from fastapi.exceptions import RequestValidationError#это декоратор для отображения ошибки на стороне сервера для пользователей. Возможно полезно для отладки. 
# from fastapi import FastAPI, Request, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

app = FastAPI(title="Склад интернет магазина", debug=True)#debug=True это для того чтобы в документации выводилсь ошибки как в консоли. 


app.mount("/static", StaticFiles(directory="static"), name="static")


#общая папка с шаблонами. Потом в функциях рендерах обращаться к ним по пути имени приложения например "showcase/test.html"
templates = Jinja2Templates(directory="templates")

#так подключается роутер
# app.include_router(router_pages)



# КОМАНДА ЗАПУСКА ВЕБ СЕРВЕРА: uvicorn main:app --reload
#uvicorn это команда запуска сервера, main - это название файла входа, app - это название объекта приложения. --reload это автоматический перезапуск приложения

#pip install fastapi[all] - это установка фастапи


#пример контекстного оператора типа рендера в джанго
@app.get("/", response_class=HTMLResponse)
async def start(request: Request):
    context = {
    "request": request,
    }
    return templates.TemplateResponse("showcase/start.html", context)







# @app.get("/")
# def home():
# 	return "Склад товаров"


# @app.get("/goods")
# def read_goods():
#     html_content = "<h1>Hello World</h1>"
#     return HTMLResponse(content=html_content)




# @app.post("/goods")
# def add_goods(goods: List[Goods]):#фукнция для добавления нового словаря по типу модели из файла models. То есть добавляем новый словарь в список. Данные также валидируются в соответствии с типами которые указали в модели. Параметров почему то нет в документации. Передается все через словарь
# 	fake_goods.extend(goods)
# 	return {"status": 200, "data": fake_goods}



# @app.get('/goods/{goods_id}', response_model=List[Goods])
# async def get_good(goods_id: int):
# 	return [g for g in fake_goods if g.get("id") == goods_id ]




@app.get("/old")
def old():
    return RedirectResponse("/new")

 
@app.get("/new")
def new():
    return PlainTextResponse("Новая страница")









if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True, workers=3)


