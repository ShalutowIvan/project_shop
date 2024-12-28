from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from sqlalchemy import insert, select, text
from sqlalchemy.orm import joinedload

from src.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .schemas import *
from src.regusers.models import User
from src.regusers.secure import test_token_expire, access_token_decode

from jose.exceptions import ExpiredSignatureError

import requests



router_showcase_api = APIRouter(
    prefix="/api",
    tags=["Showcase_api"]
)



async def base_requisites(db, request, check=[False, None, " "]):#db - сессия, check - результат дешифровки аксес токена, request - Request
    org = await db.execute(select(Organization))  
    group = await db.execute(select(Group))    

    if check[1] != None and check[1] != False:       
        # query = select(User).where(User.id == int(check[1]))   
        # user = await db.scalars(query)                
        # user_name = user.all()[0].name
        user_name = check[2]
    else:
        user_name = ""

    context = {
    "request": request,    
    "org": org.scalars().first(),
    "group": group.scalars(),    
    "check": check[0],
    "user_name": user_name,
    }

    return context



@router_showcase_api.get("/groups_all/", response_model=list[GroupShema])
async def groups_all(request: Request, session: AsyncSession = Depends(get_async_session)) -> GroupShema:
    query = select(Group)
    group = await session.scalars(query)
    
    # group = await session.execute(select(Group))
    
    # context = group.scalars()

    return group






#главное сделать response_model=list[GoodsShema] в декораторе, тогда ответ из дб будет конвертироваться в JSON и приниматься на фронте
@router_showcase_api.get("/goods_all/", response_model=list[GoodsShema])
async def goods_all(request: Request, session: AsyncSession = Depends(get_async_session)) -> GoodsShema:
	
	good = await session.execute(select(Goods))
	
	context = good.scalars()
	return context



@router_showcase_api.get("/goods_in_group/{slug}", response_model=list[GoodsShema])
async def goods_in_group(request: Request, slug: str, session: AsyncSession = Depends(get_async_session)) -> GoodsShema:	
    
    query = select(Goods).options(joinedload(Goods.group))
    good_gr = await session.scalars(query)
    if slug == "0":
        good_gr = list(good_gr)
    else:
        good_gr = list(filter(lambda x: x.group.slug == slug, good_gr))


    return good_gr




# ост тут, решил делать фронт для витрины









