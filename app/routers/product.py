from typing import List
from fastapi import status, HTTPException, APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session

from app import oauth2
from ..schemas import PostProduct, ProductResponse
import psycopg2
from .. import models, utils
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def register_products(product: PostProduct, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_product = models.Product(product_type= product.product_type, price=product.price, 
    is_purchased=product.is_purchased)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"item with id {id} does not exist")
    return product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: int, updated_product: PostProduct, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()