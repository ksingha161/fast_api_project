from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from app.contract import Model
import psycopg2
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def get_home_page():
    return {"message": "welcome to products API"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return {"items": products}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def register_products(product: Model, db: Session = Depends(get_db)):
    new_product = models.Product(product_type= product.product_type, price=product.price, 
    is_purchased=product.is_purchased)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"new_item": product}

@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"item with id {id} does not exist")
    return {"item": product}

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/products/{id}")
def update_product(id: int, updated_product: Model, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()
    return {'data': product_query.first()}
