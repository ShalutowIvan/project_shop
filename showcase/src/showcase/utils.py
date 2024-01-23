
from src.regusers.secure import update_tokens







#функция для формирования контекста страницы
async def base_requisites(db, request, check=[False, None]):#db - сессия, check - результат дешифровки аксес токена, request - Request
    org = await db.execute(select(Organization))    
    group = await db.execute(select(Group))
    # good = await db.execute(select(Goods))

    if check[1] != None and check[1] != False:       
        query = select(User).where(User.id == int(check[1]))    
        user = await db.scalars(query)                
        user_name = user.all()[0].name
    else:
        user_name = ""

    context = {
    "request": request,    
    "org": org.scalars().first(),
    "group": group.scalars(),
    # "good": good.scalars(),
    "check": check[0],
    "user_name": user_name,
    }

    return context