from pydantic import BaseModel, Field, EmailStr, validator, UUID4
from typing import Optional
from datetime import datetime



class Users(BaseModel):   
    id: int
    email: str
    name: str
    password: str
    is_active: bool
    time_create_user: datetime



