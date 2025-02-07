from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
# from regusers.schemas import *
from .models import State_order


#есть такая штука как перечисления Enum. Это набор значений который можно использовать при валидации как в схемах pydentic так и в функциях или роутерах указывая аннотация на класс с перечислениями. Более подробно как работать с перечислениями можно почитать в документации фастапи раздел path-параметры

class GroupShema(BaseModel):
    id: int
    name_group: str = Field(max_length=255)
    slug: str = Field(max_length=255)

    class Config:
        from_attributes = True


class GoodsShema(BaseModel):
    id: int
    # id: Optional[int] = Field(default=1)
    name_product: str = Field(max_length=255)
    vendor_code: str = Field(max_length=20)
    stock: float	
    price: float = Field(ge=0)
    slug: str = Field(max_length=255)
    photo: str
    availability: bool
    # group: Optional[list[Group]] = []
    group_id: int
    # time_create: datetime

    class Config:
        from_attributes = True


    # def __eq__(self, other):
    #     if not isinstance(other, type(self)):
    #         return False
    #     for attr in ["title", "state", "owner"]:
    #         if getattr(self, attr) != getattr(other, attr):
    #             return False
    #     return True


    # def to_dict_wo_id(self) -> dict:
    #     return self.model_dump(exclude={"id"})


class BasketShema(BaseModel):    
    id: int
    user_id: int
    # product: list[GoodsShema] = []
    product: GoodsShema
    product_id: int
    quantity: float
    created_timestamp: datetime


class OrganizationShema(BaseModel):
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


class Order_counterShema(BaseModel):
    id: int
    user_id: int
    time_create: datetime


class Order_list_form_Shema(BaseModel):
    fio: str
    phone: str
    delivery_address: str
    pay: str



class Order_list_boughtShema(BaseModel):    
    id: int
    fio: str
    delivery_address: str
    phone: str    
    product: GoodsShema
    product_id: int  
    quantity: float
    order_number: int
    user_id: int
    state_order: State_order
    state: bool

    class Config:
        from_attributes = True


class PaymentShema(BaseModel):  
    id: int
    pay: str


class ContactsShema(BaseModel):
    id: int
    user: int#это форинкей из таблицы юзеров, потом переделалать и везде юзера переделать потом
    fio: str
    phone: int
    delivery_address: str
    pay: list[PaymentShema] = []



