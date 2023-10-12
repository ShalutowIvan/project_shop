from pydantic import BaseModel, Field, EmailStr, validator, UUID4
from typing import Optional
from datetime import datetime

# import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    time_create_user: datetime
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    id: int
    name: str
    time_create_user: datetime
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


#пока без обновления. Этот класс для обновления пользователя
# class UserUpdate(schemas.BaseUserUpdate):
#     pass


