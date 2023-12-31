from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(100))
    time_create_user = mapped_column(TIMESTAMP, default=datetime.utcnow)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

# mapped_column - это более расширенный класс для колонок в sqlalchemy. То есть тоже самое но лучше

# class User(SQLAlchemyBaseUserTableUUID, Base):
#     email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
#     hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#     is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)





# tokens = Table(
#     "tokens",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column(
#         "token",
#         UUID(as_uuid=False),
#         server_default=sqlalchemy.text("uuid_generate_v4()"),
#         unique=True,
#         nullable=False,
#         index=True,
#     ),
#     Column("expires", DateTime()),
#     Column("user_id", ForeignKey("users.id")),
# )




# https://habr.com/ru/articles/513328/
#это ссылка с инфой по фаст апи по реге