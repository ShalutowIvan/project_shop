# from pydantic import BaseModel, Field
# from typing import List, Optional

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, JSON
from datetime import datetime
# from reguers import


metadata = MetaData()


group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_group", String, nullable=False),    
    Column("slug", String, nullable=False),
)

goods = Table(
    "goods",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_product", String, nullable=False),
    Column("vendor_code", String, nullable=False),
    Column("stock", Float, nullable=True),#пароли нужно хранить в захешированном виде всегда, это для безопасности. Без ключа в захеришрованном виде нельзя его расшифровать
    Column("slug", String, nullable=False),
    Column("photo", String, nullable=False),
    Column("availability", Boolean, nullable=False),
    Column("time_create", TIMESTAMP, default=datetime.utcnow),#utcnow для разных часовых поясов в случае расположения бд и пользователя в разных часовых поясах, это универсальный часовой пояс. При создании будет автоматом записываться текущее время создания поля. 
    Column("name_group", Integer, ForeignKey("group.id")),#ссылаемся на таблицу group и на ее элемент id
)


basket = Table(
    "basket",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user", String, nullable=False),
    Column("product", Integer, ForeignKey("goods.id")),
    Column("quantity", Integer, default=0),
    Column("created_timestamp", TIMESTAMP, default=datetime.utcnow),
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


order_list_bought = Table(
    "order_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_product", String, nullable=False),
    Column("quantity", Float, nullable=False),
    Column("order_number", Integer, nullable=False),
    Column("time_create", TIMESTAMP, default=datetime.utcnow),
    # Column("user", String, ForeignKey("")),
)

contacts = Table(
    "contacts",
    metadata,
    Column("id", Integer, primary_key=True),
    # Column("user", Integer, ForeignKey(".id")),
    Column("fio", String, nullable=False),
    Column("phone", Integer, default=0),
    Column("delivery_address", Text, default="_"),
    # Column("pay", Integer, ForeignKey(".id")),
)


payment = Table(
    "payment",
    metadata,
    Column("id", Integer, nullable=False),
    Column("pay", String, nullable=False),
)




# https://www.youtube.com/watch?v=1Ag3RoOjNI0&list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS&index=7&ab_channel=%D0%90%D1%80%D1%82%D1%91%D0%BC%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE
# ост 13 мин



# памятка для миграций БД
#команда для создания ревизиии миграции БД
# alembic revision --autogenerate -m "Database creation"
#команда для запуска миграции:
# alembic upgrade hash
# alembic upgrade head
#hash брать из файла миграции
#head - это значит до самой последней миграции




