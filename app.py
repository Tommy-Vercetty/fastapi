import re
import requests
from typing import Union
from fastapi import Query
from fastapi import FastAPI
from pydantic import BaseModel
from dbConnection import dbCollection

class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to Tommy's FAST Api!"}

@app.get("/getSingleProduct")
def getSingleProduct(productID: int):
    product = dbCollection.find_one({"ProductID": productID})

    print("Result:", product)

    if product:
        product["_id"] = str(product["_id"])
        return product
    else:
        return {"error" : "No product with that id Monsieur!"}
    
@app.get("/getAll")
def getAllProducts():
    products = list(dbCollection.find())

    print("Result:", products)

    for product in products:
        product["_id"] = str(product["_id"])
    
    return products
    
@app.post("/addNew")
def addNewProduct(product: Product):
    product_dict = product.dict()

    result = dbCollection.insert_one(product_dict)
    return { "message": "Product added!", "newlyInsertedProductID": str(result.inserted_id) }

@app.get("/deleteOne")
def deleteProduct(productID: int):
    product = dbCollection.find_one({"ProductID": productID})

    if not product:
        return {"error": "Product doesn't exist!"}
    
    result = dbCollection.delete_one({"ProductID": productID})
    print("message:", "Product deleted!")
    return { "message": f"Product {productID} deleted!", "numberOfDeletedProducts": result.deleted_count }

@app.get("/startsWith")
def filteringProducts(userEnteredLetter: str = Query(..., description = "Enter a letter to filter products.")):
    letterPattern = f"^{re.escape(userEnteredLetter)}"

    products = list(dbCollection.find({ "Name": {"$regex": letterPattern, "$options": "i"}}))

    print("Filtered Products:", products)

    for product in products:
        product["_id"] = str(product["_id"])

    if not products:
        return { "message": f"Sorry, there are no products starting with the etter '{userEnteredLetter}'"}
    
    return products

@app.get("/paginate")
def filterProductsViaRange(startOfRangeID: int = Query(..., description = "Enter the Product ID you want to start from."),
                           endOfRangeID: int = Query (..., description = "Enter the Product ID you want to end at.")):
    
    products = list(dbCollection.find({ "ProductID": {"$gte": startOfRangeID, "$lte": endOfRangeID}}
                                      ).sort("ProductID", 1).limit(10))
    
    print("Filtered Products in the selected range:", products)

    for product in products:
        product["_id"] = str(product["_id"])

    if not products:
        return {"message": f"There are no products between ProductID {startOfRangeID} and {endOfRangeID}"}
    
    return products

@app.get("/convert")
def convertDollarToEuro(productID: int):
    product = dbCollection.find_one({"ProductID": productID})

    if not product:
        return {"error": "The entered product doesn't exist!"}
    
    
    response = requests.get("https://open.er-api.com/v6/latest/USD")
    response.raise_for_status()
    rate = response.json()["rates"]["EUR"]

    USDToEUR = round(product["UnitPrice"] * rate, 2)

    product["_id"] = str(product["_id"])

    productPriceInEUR = product.copy()
    productPriceInEUR["UnitPriceEUR"] = USDToEUR

    return productPriceInEUR


