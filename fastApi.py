from typing import Union
from dbConnection import dbCollection
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"Welcome to Tommy's FAST Api!"}

@app.get("/products/{ProductID}")
def getSingleProduct(productId: int):
    product = dbCollection.find_one({"ProductID": productId})

    if product:
        product["_id"] = str(product["_id"])
        return product
    else:
        return {"error" : "No product found!"}
    
@app.get("/getAll")
def getAllProducts():
    return []

#@app.post("/addNew")

#@app.get("/deleteOne")

#@app.get("/startsWith")

#@app.get("/paginate")

#@app.get("/convert")


