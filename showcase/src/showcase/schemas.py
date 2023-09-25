from pydantic import BaseModel, Field
from typing import Optional



class Group(BaseModel):
	id: int
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
	group: Optional[list[Group]] = []