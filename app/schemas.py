from pydantic import BaseModel, EmailStr
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

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True