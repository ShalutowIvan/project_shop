# from pydantic import BaseModel, Field
# from typing import List, Optional

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, JSON
from datetime import datetime
# from ..regusers.models import User

from database import Base

# metadata = MetaData()


# group = Table(
#     "group",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name_group", String, nullable=False),
#     Column("slug", String, nullable=False),
# )

class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True),
    name_group = Column(String, nullable=False),
    slug = Column(String, nullable=False),


# goods = Table(
#     "goods",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name_product", String, nullable=False),
#     Column("vendor_code", String, nullable=False),
#     Column("stock", Float, nullable=True),
#     Column("slug", String, nullable=False),
#     Column("photo", String, nullable=False),
#     Column("availability", Boolean, nullable=False),
#     Column("time_create", TIMESTAMP, default=datetime.utcnow),#utcnow для разных часовых поясов в случае расположения бд и пользователя в разных часовых поясах, это универсальный часовой пояс. При создании будет автоматом записываться текущее время создания поля.
#     Column("name_group", Integer, ForeignKey("group.id")),#ссылаемся на таблицу group и на ее элемент id
# )

class Goods(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True)
    name_product = Column(String, nullable=False)
    vendor_code = Column(String, nullable=False)
    stock = Column(Float, nullable=True)
    slug = Column(String, nullable=False)
    photo = Column(String, nullable=False)
    availability = Column(Boolean, nullable=False)
    time_create = Column(TIMESTAMP, default=datetime.utcnow)#utcnow для разных часовых поясов в случае расположения бд и пользователя в разных часовых поясах, это универсальный часовой пояс. При создании будет автоматом записываться текущее время создания поля.
    name_group = Column(Integer, ForeignKey("group.id"))#ссылаемся на таблицу group и на ее элемент id




# basket = Table(
#     "basket",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     # Column("user", Integer, ForeignKey(".id")),
#     Column("product", Integer, ForeignKey("goods.id")),
#     Column("quantity", Integer, default=0),
#     Column("created_timestamp", TIMESTAMP, default=datetime.utcnow),
# )

class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True)
    #user = Column("user", Integer, ForeignKey(".id"))
    product = Column(Integer, ForeignKey("goods.id"))
    quantity = Column(Integer, default=0)
    created_timestamp = Column(TIMESTAMP, default=datetime.utcnow)





# organization = Table(
#     "organization",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name_org", String, nullable=False),
#     Column("inn", Integer, default=0),
#     Column("kpp", Integer, default=0),
#     Column("ogrn", Integer, default=0),
#     Column("working_mode", String, default="_"),
#     Column("about", Text, default="_"),
#     Column("adres", String, default="_"),
#     Column("phone", Integer, default=0),
#     Column("email_name", String, nullable=False),
#     Column("telegram", String, default="_"),
#     Column("whatsApp", String, default="_"),
# )

class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name_org = Column(String, nullable=False)
    inn = Column(Integer, default=0)
    kpp = Column(Integer, default=0)
    ogrn = Column(Integer, default=0)
    working_mode = Column(String, default="_")
    about = Column(Text, default="_")
    adres = Column(String, default="_")
    phone = Column(Integer, default=0)
    email_name = Column(String, nullable=False)
    telegram = Column(String, default="_")
    whatsApp = Column(String, default="_")




# order_list_bought = Table(
#     "order_list",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name_product", Integer, ForeignKey("goods.id")),
#     Column("quantity", Float, nullable=False),
#     Column("order_number", Integer, nullable=False),
#     Column("time_create", TIMESTAMP, default=datetime.utcnow),
#     # Column("user", Integer, ForeignKey(".id")),
# )

class Order_list(Base):
    __tablename__ = "order_list"
    id = Column(Integer, primary_key=True)
    name_product = Column(Integer, ForeignKey("goods.id"))
    quantity = Column(Float, nullable=False)
    order_number = Column(Integer, nullable=False)
    time_create = Column(TIMESTAMP, default=datetime.utcnow)
    # user = Column(Integer, ForeignKey(".id"))



# payment = Table(
#     "payment",
#     metadata,
#     Column("id", Integer, unique=True, primary_key=True),
#     Column("pay", String, nullable=False),
# )

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, unique=True, primary_key=True)
    pay = Column(String, nullable=False)



# contacts = Table(
#     "contacts",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     # Column("user", Integer, ForeignKey(".id")),
#     Column("fio", String, nullable=False),
#     Column("phone", Integer, default=0),
#     Column("delivery_address", Text, default="_"),
#     Column("pay", Integer, ForeignKey("payment.id")),
# )

class Contacts(Base):
    __tablename__ = "contacts"
    id = Column( Integer, primary_key=True)
    # user = Column(Integer, ForeignKey(".id"))
    fio = Column( String, nullable=False)
    phone = Column( Integer, default=0)
    delivery_address = Column( Text, default="_")
    pay = Column( Integer, ForeignKey("payment.id"))








# памятка для миграций БД
#команда для создания ревизиии миграции БД
# alembic revision --autogenerate -m "Database creation"
#команда для запуска миграции:
# alembic upgrade hash
# alembic upgrade head
#hash брать из файла миграции
#head - это значит до самой последней миграции




