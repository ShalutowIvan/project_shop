from pydantic import BaseModel, Field
from typing import List, Optional

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, JSON
from datetime import datetime

metadata = MetaData()


group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_group", String, nullable=False),    
)

goods = Table(
    "goods",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_product", String, nullable=False),
    Column("vendor_code", String, nullable=False),
    Column("stock", Float, nullable=True),#пароли нужно хранить в захешированном виде всегда, это для безопасности. Без ключа в захеришрованном виде нельзя его расшифровать
    # Column("slug", String, nullable=False),
    Column("photo", String, nullable=False),
    Column("availability", Boolean, nullable=False),
    Column("time_create", TIMESTAMP, default=datetime.utcnow),#utcnow для разных часовых поясов в случае расположения бд и пользователя в разных часовых поясах, это универсальный часовой пояс. При создании будет автоматом записываться текущее время создания поля. 
    Column("name_group", Integer, ForeignKey("group.id")),#ссылаемся на таблицу group и на ее элемент id
)


organization = Table(
    "organization",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_org", String, nullable=False),
    Column("inn", Integer, default=0),
    Column("kpp", Integer, default=0),
    Column("ogrn", Integer, default=0),#пароли нужно хранить в захешированном виде всегда, это для безопасности. Без ключа в захеришрованном виде нельзя его расшифровать
    Column("working_mode", String, default="_"),
    Column("about", Text, default="_"),
    Column("adres", String, default="_"),
    Column("phone", Integer, default=0),#utcnow для разных часовых поясов в случае расположения бд и пользователя в разных часовых поясах, это универсальный часовой пояс. При создании будет автоматом записываться текущее время создания поля. 
    Column("email_name", String, nullable=False),
    Column("telegram", String, default="_"),
    Column("whatsApp", String, default="_"),
)



order_list = Table(
    "order_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("buyer", Text, nullable=False),#тут данные о покупателе, фио, адрес доставки, телефон и тд
    Column("name_product", String, nullable=False),    
    Column("quantity", Float, nullable=False),    
    Column("order_number", Integer, nullable=False),    
    Column("time_create", TIMESTAMP, default=datetime.utcnow),    
    # Column("user", String, nullable=False),    
)


#способ оплаты. Пока не пригодился
# payment = Table(
#     "payment",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("pay", String, nullable=False),    
# )



# class Group(BaseModel):
# 	name_group: str = Field(max_length=255)
# 	slug: str = Field(max_length=255)



# class Goods(BaseModel):
# 	id: int
# 	name_product: str = Field(max_length=255)
# 	vendor_code: str = Field(max_length=20)
# 	stock: float	
# 	price: float = Field(ge=0)
# 	slug: str = Field(max_length=255)
# 	photo: str
# 	availability: bool
# 	group: Optional[list[Group]] = [] #это поле опциональное. То есть его может и не быть. В новых версяих питона можно юзать просто list, а не List


    
# class Organization(BaseModel):
# 	id: int
# 	name_org: str = Field(max_length=255)
# 	inn_kpp: str = Field(max_length=255)
# 	ogrn: int
# 	working_mode: str = Field(max_length=255)
# 	about: str = Field(max_length=255)
# 	adres: str = Field(max_length=255)
# 	phone: int
# 	email_name: str = Field(max_length=255)
# 	telegram: str = Field(max_length=255)
# 	whatsApp: str = Field(max_length=255)





