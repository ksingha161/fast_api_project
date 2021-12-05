from fastapi import FastAPI
import psycopg2
from . import models
from .database import engine, get_db
from .routers import product, user

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(
    product.router, 
    prefix="/products",
    tags=['Products']
    )

app.include_router(
    user.router, 
    prefix="/user",
    tags=['Users']
    )

@app.get("/")
def get_home_page():
    return {"message": "welcome to products API"}
