from pydantic import BaseModel
from typing import List

class Menu(BaseModel):
    id: int
    named: str
    types: str
    cost: int

class OrderiDTO(BaseModel):
    order_products: List[Menu]
    total:str