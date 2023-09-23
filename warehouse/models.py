from pydantic import BaseModel, Field
from typing import List, Optional





class Group(BaseModel):
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
	group: Optional[list[Group]] = [] #это поле опциональное. То есть его может и не быть. В новых версяих питона можно юзать просто list, а не List


    
class Organization(BaseModel):
	id: int
	name_org: str = Field(max_length=255)
	inn_kpp: str = Field(max_length=255)
	ogrn: int
	working_mode: str = Field(max_length=255)
	about: str = Field(max_length=255)
	adres: str = Field(max_length=255)
	phone: int
	email_name: str = Field(max_length=255)
	telegram: str = Field(max_length=255)
	whatsApp: str = Field(max_length=255)





