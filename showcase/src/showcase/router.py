from fastapi import APIRouter, Depends, HTTPException, Request, Response

from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import insert, select

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


from .models import *
from config import templates

router = APIRouter(
    prefix="/home",
    tags=["Showcase"]
)



##################################################################################
#памятка как делать sql запрос с асинхронным подключением к сессии БД!!!!!!!!!!!!
#этот код нужно писать в асинхронной функции
# org = select(organization)#создали запрос на таблицу организаций. organization это модель БД, которую мы ранее сами сделали. select это функция из sql алхимии. 
# res = await session.execute(org)#запросили ее из сессии, всю таблицу. session - это параметр функции вьюшки, execute это метод для подключения. В скобках пишем переменную которую написали выше.
# print(f"Название {res.all()[0]}")#тут мы сделали sql запрос всей таблицы, возвращается список кортежей по каждой строке в таблице, 1 строка 1 кортеж. Тут к предыдущей переменной можно юзать функции из sql алхимии. 
##################################################################################




@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_async_session)):    
    
    org = await session.execute(select(organization))
    gr = await session.execute(select(group))
    gd = await session.execute(select(goods))

    context = {
    "request": request,    
    "org": org.all()[0],
    "group": gr.all(),
    "gd": gd.all(),

    }

    return templates.TemplateResponse("showcase/start.html", context)


@router.get("/basket", response_class=HTMLResponse)
async def basket_view(request: Request, session: AsyncSession = Depends(get_async_session)):
    
    basket = await session.execute(select(basket))

    context = {
    "request": request,
    "basket": basket.all(),

    }

    return templates.TemplateResponse("showcase/basket.html", context)



@router.get("/checkout_list", response_class=HTMLResponse)
async def checkout_list(request: Request, session: AsyncSession = Depends(get_async_session)):
    order_list = await session.execute(select(order_list_bought))
    kont = await session.execute(select(contacts))

    context = {
    "request": request,
    "order_list": order_list.all(),
    "contacts": kont.all()
    }

    return templates.TemplateResponse("showcase/basket.html", context)






# <!-- пагинация начало -->
# {% if page_obj.has_other_pages %}
# <nav class="list-pages">
#     <ul>
# {% if page_obj.has_previous %}
# <li class="page-num">
# <a href="?page={{ page_obj.previous_page_number }}">&lt;</a>
# </li>
# {% endif %}

# {% for i in paginator.page_range %}

# {% if page_obj.number == i %}
# <li class="page_selected">{{ i }}</li>

# {% elif i >= page_obj.number|add:-2 and i <= page_obj.number|add:2  %}


# <li class="page-num">
#     <a href="?page={{ i }}">{{ i }}</a>
# </li>
# {% endif %}

# {% endfor %}


# {% if page_obj.has_next %}
# <li class="page-num">
# <a href="?page={{ page_obj.next_page_number }}">&gt;</a>
# </li>
# {% endif %}
# </ul>
# </nav>
# {% endif %}

# <!-- пагинация конец -->


# <!--Форма для поиска товара -->
# <form action="{% url 'start' %}" method="get">

#     <input type="search" type="text" name='q' placeholder="Введите название товара">

#     <button type="submit">Найти</button>
# </form>
# <!--конец Форма для поиска товара -->



# <!--    {% # if request.user.is_authenticated %}   -->

# <!--  {% # else %}  -->

# <!--                {% # endif %} -->



# <!--форма для добавления корзины -->
#     {% if request.user.is_authenticated %}
# <a href="{% url 'add_in_basket' j.id %}"><button class="add_basket">Добавить в корзину</button></a>

#     <br><br>


#     {% endif %}
# <!--конец форма -->




