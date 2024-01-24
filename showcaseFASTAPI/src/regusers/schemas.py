from pydantic import BaseModel, Field, EmailStr, validator, UUID4
from typing import Optional
from datetime import datetime





class UserAuth(BaseModel):
    # id: UUID4
    # id: int
    # name: str
    # time_create_user: datetime
    email: EmailStr
    password: str
    # is_active: bool = True
    

class UserCreate(BaseModel):
    id: int
    name: str
    # time_create_user: datetime
    email: EmailStr
    password: str
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
    


class MailBody(BaseModel):
    to: list[str]
    subject: str
    body: str
