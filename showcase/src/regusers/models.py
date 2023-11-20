from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class User(Base):
    __tablename__ = "user"
    # id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = mapped_column(Integer, primary_key=True, index=True)#пока так, если что потом заменить на uuid
    name = mapped_column(String(100))
    time_create_user = mapped_column(TIMESTAMP, default=datetime.utcnow)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    tokens = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = "token"

    id = mapped_column(Integer, primary_key=True, index=True)
    refresh_token = mapped_column(String(length=320), unique=True, index=True, nullable=False)    

    user_id = mapped_column(Integer, ForeignKey("user.id"))#это id пользователь которому будет принадлежать токен
    
    user = relationship("User", back_populates="token")



# class Item(Base):
#     __tablename__ = "item"

#     id = mapped_column(Integer, primary_key=True, index=True)
#     atom = mapped_column(String(length=320), unique=True, index=True, nullable=False)        




    

# ост 29 мин



