from typing import Optional
from pydantic import BaseModel

class Model(BaseModel):
    product_type: str
    price: float
    is_purchased: bool