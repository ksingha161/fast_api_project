from typing import Optional
from pydantic import BaseModel

class Model(BaseModel):
    product: str
    price: int
    review: Optional[int]
    purchased: bool = True