from fastapi import FastAPI
from models import *
from typing import List



# from fastapi.exceptions import RequestValidationError#это декоратор для отображения ошибки на стороне сервера для пользователей. Возможно полезно для отладки. 
# from fastapi import FastAPI, Request, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse

app = FastAPI(title="Склад интернет магазина", debug=True)#debug=True это для того чтобы в документации выводилсь ошибки как в консоли. 


# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error". Это не работает. Я не разобрался...
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()}),
#     )




@app.get("/")
def home():
	return "Склад товаров"


fake_trades = [
{"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
{"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 321, "amount": 2.12}
]



@app.get("/trades")#trades это эндпоинт, точка конца
def get_trades(limit: int = 1, offset: int = 0):#limit колво получаемых сделок, offset это сдвиг по списку сделок. Можно задавать формальные параметры чтобы был один и тот же запрос
    return fake_trades[offset:][:limit]



fake_goods = [
{"id": 1, "name_product": 'килька', "vendor_code": "12345", "stock": 55, "price": 111, "slug": "fish", "photo": "image", "availability": True, "group": [{"name_group": "Рыба", "slug": "fish"}]}, 
{"id": 2, "name_product": "Торт", "vendor_code": "12341", "stock": 51, "price": 222, "slug": "cake", "photo": "image2", "availability": True, "group": [{"name_group": "Хлеб", "slug": "bread"}]},
{"id": 3, "name_product": "Унитаз", "vendor_code": "12342", "stock": 15, "price": 11111, "slug": "wasserclosed", "photo": "image", "availability": True }

]


# @app.post("/goods")
# def add_goods(goods: List[Goods]):#фукнция для добавления нового словаря по типу модели из файла models. То есть добавляем новый словарь в список. Данные также валидируются в соответствии с типами которые указали в модели. Параметров почему то нет в документации. Передается все через словарь
# 	fake_goods.extend(goods)
# 	return {"status": 200, "data": fake_goods}



@app.get('/goods/{goods_id}', response_model=List[Goods])
async def get_good(goods_id: int):
	return [g for g in fake_goods if g.get("id") == goods_id ]








if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True, workers=3)


