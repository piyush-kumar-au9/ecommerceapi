# models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    name: str
    price: float
    available_quantity: int

class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

class OrderItem(BaseModel):
    product_id: str
    bought_quantity: int
    total_amount: float

class Order(BaseModel):
    order_id:str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem]
    user_address: UserAddress
