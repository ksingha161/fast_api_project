from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    product_type: str
    price: float
    is_purchased: bool = False

class PostProduct(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config():
        orm_mode = True