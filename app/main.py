from fastapi import FastAPI, status, HTTPException
from starlette.responses import Response
from app.contract import Model
from random import randrange

app = FastAPI()

stored_products = [{
        "id": 1,
        "product": "chair",
        "price": 600,
        "review": None,
        "purchased": False,
    },
    {
        "id": 2,
        "product": "table",
        "price": 750,
        "review": "pretty nice table",
        "purchased": True
    }]

def get_user_id(id):
    for i in stored_products:
        if i['id'] == id:
            return i

def get_index(id):
    for i, j in enumerate(stored_products):
        if j['id'] == id:
            return i

@app.get("/")
def get_home_page():
    return {"message": "hello"}

@app.get("/products")
def get_products():
    return {"items": stored_products}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def register_products(product: Model):
    product_dict = product.dict()
    rand_id = randrange(0, 100000)
    product_dict['id'] = rand_id
    stored_products.append(product_dict)
    print(stored_products)
    return {"new_item": product}

@app.get("/products/{id}")
def get_product(id: int):
    product = get_user_id(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"item with id {id} does not exist")
    return {"item": product}

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    index = get_index(id)
    stored_products.pop(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/products/{id}")
def update_product(id: int, product: Model):
    # find the index of product that user is request
    index = get_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # take all data and convert to python dictionary
    product_dict = product.dict() 
    product_dict['id'] = id
    stored_products[index] = product_dict
    return {'data': product_dict}
