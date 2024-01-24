from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from regusers.schemas import *

#есть такая штука как перечисления Enum. Это набор значений который можно использовать при валидации как в схемах pydentic так и в функциях или роутерах указывая аннотация на класс с перечислениями. Более подробно как работать с перечислениями можно почитать в документации фастапи раздел path-параметры

class Group(BaseModel):
	id: int
	name_group: str = Field(max_length=255)
	slug: str = Field(max_length=255)


class Goods(BaseModel):
	id: int
	name_product: str = Field(max_length=255)
	vendor_code: str = Field(max_length=20)
	stock: float	
	price: float = Field(ge=0)
	slug: str = Field(max_length=255)
	photo: str
	availability: bool
	group: Optional[list[Group]] = []


class Basket(BaseModel):    
    id: int
    user: int
    product: list[Goods] = []
    quantity: float
    created_timestamp: datetime


class Organization(BaseModel):
    id: int
    name_org: str
    inn: int
    kpp: int
    ogrn: int
    working_mode: str
    about: str
    adres: str
    phone: int
    email_name: str
    telegram: str
    whatsApp: str


class Order_list_bought(BaseModel):    
    id: int
    # name_product: list[Goods] = []
    name_product: int
    quantity: float
    order_number: int
    time_create datetime
    user: int


class Payment(BaseModel):  
    id: int
    pay: str


class Contacts(BaseModel):
    id: int
    user: int#это форинкей из таблицы юзеров, потом переделалать и везде юзера переделать потом
    fio: str
    phone: int
    delivery_address: str
    pay: list[Payment] = []



