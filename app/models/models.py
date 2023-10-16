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
class CoffeeShopStatus:
    def __init__(self):
        self.start = False
        self.flag = False
        self.lastAdminAssistantResponce = ""
        self.newProductType = ""
        self.newProductName = ""
        self.newProductCost = ""
        self.products = ""
        self.chatHistory = []
        self.newRandomProduct = []
        self.status = []
        self.startAdmin = True
        self.products = []

    def reset_variables(self):
        self.start = False
        self.flag = False
        self.lastAdminAssistantResponce = ""
        self.newProductType = ""
        self.newProductName = ""
        self.newProductCost = ""
        self.products = ""
        self.chatHistory = []
        self.newRandomProduct = []
        self.status = []
        self.startAdmin = True
        self.products = []