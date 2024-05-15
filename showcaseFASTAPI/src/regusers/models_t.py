from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Text, Table, Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db_t import Base


class User(Base):
    __tablename__ = "user"    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256))
    time_create_user: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)    
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)

    #связи
    tokens: Mapped["Token"] = relationship(back_populates="user")
    basket: Mapped["Basket"] = relationship(back_populates="user")
    order_list: Mapped["Order_list"] = relationship(back_populates="user")
    # order_counter: Mapped["Order_counter"] = relationship(back_populates="user")


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    refresh_token = mapped_column(String(length=320), unique=True, index=True, nullable=False)    

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    
    user: Mapped["User"] = relationship(back_populates="tokens")


