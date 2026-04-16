#This is our API file. In this API, we provide several endpoints we can access.
# The technologies we are using are the following:
# - Fast API: Used for building the web version of our API that we can test
# - MongoDB: Schema-less database for storing our products CSV data
# - Pydantic: Used for ensuring some forms of data validation
# - Requests: Since we needed to call an external API for the currency exchange
# - REGEX: For filtering specific product names

#Starting off with our imports, we have the following:
# 're' library: Allows us to use regex patterns for filtering product names. 
# Regex patterns are simple character-level patterns typically used for input handling/ validation.
import re
# 'requests' library: Allows us to make HyperText Transfer Protocol requests to external API's.
#  This is used for our currency exchange endpoint.
import requests
# 'Query' library: Since we are going to have to pass parameters in our POST or GET requests,
#   we need to be able to validate and document them. 
from fastapi import Query
# 'FastAPI' library: Creates our API application.
from fastapi import FastAPI
# 'BaseModel' library: Since we need to define different data models and validate them.
from pydantic import BaseModel
# 'dbConnection' file: This is our small seperate file that transfers the content of
#  our CSV into a specific collection within our database.
from dbConnection import dbCollection

#Even though we are using a schema-less database, we want to ensure that any NEW product
# added to the database follows a specific structure. In our 3rd API endpoint, we are pushing
#  a new product into the database. Using this Pydantic model, we can automatically validate it.
#   NOTE: All of the attributes below, are the same ones as all products already present in our database.
class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str

#We now start off by creating our FastAPI application.
# We create an object called 'app' of type FastAPI.
#  This object will be used to define all other endpoints we have below.
#   To access and test our API endpoints manually, we have SwaggerUI
app = FastAPI()

#API Endpoint 0 - Root Endpoint (GET)
# The purpose of this endpoint is to provide a simple welcome message.
#  We return a 'message' in the form of a JSON response.
@app.get("/")
def read_root():
    return {"message": "Welcome to Tommy's FAST Api!"}

#API Endpoint 1 - Retrieving a single product (GET)
# We start off by accepting a productID as an 'int' parameter.
#  MongoDB then searches for a matching product that has the user entered ID using the 'findOne' function.
#   We then create a local variable called 'product' that is going to store the product
#   the user is looking for.
#    If the product exists, we convert the ID of the product from its Mongo Object ID,
#    to a string ID for JSON serialization.
#     Lastly, we return the product. If the product does not exist, we return an error message.
@app.get("/getSingleProduct")
def getSingleProduct(productID: int):
    product = dbCollection.find_one({"ProductID": productID})

    print("Result:", product)

    if product:
        product["_id"] = str(product["_id"])
        return product
    else:
        return {"error" : "No product with that id Monsieur!"}

#API Endpoint 2 - Retrieve all products (GET) 
# We start off by retrieving all of the documents (AKA products) from our Mongo collection
# using the 'find()' function.
#  Next, to display all the products we loop into the products list, and convert each product ID
#  into a String.
#   Lastly, we return the full list of products.
@app.get("/getAll")
def getAllProducts():
    productList = list(dbCollection.find())
    print("All Products List:", productList)
    for product in productList:
        product["_id"] = str(product["_id"])
    
    return productList

#API Endpoint 3 - Adding a new product (POST)
# We start off by accepting a JSON body accepted by the Product model we declared above
#  First off, we want to convert the model for any new product we created above, and convert
#   it into a Python dictionary. We do this so that we can then convert the dictionary into JSON
#    format. We then insert the new product in the database, and return the ID of the newly inserted product
@app.post("/addNew")
def addNewProduct(product: Product):
    productDictionary = product.dict()
    newlyInsertedProduct = dbCollection.insert_one(productDictionary)
    return {"message": "Your product has been added Monsieur!", "newlyInsertedProductID": str(newlyInsertedProduct.inserted_id)}

#API Endpoint 4 - Deleting an existing product (GET)
# We start off by checking if the product exists in the database using the 'find_one()' method.
#  This function will filter the database and search by the Product ID
#   If the product is not present, we let the user know by sending them a message.
#    If the product is found, we delete it from the collection using the 'delete_one()' function.
#     Lastly, we send a message to the user, and return the ID of the deleted product, and the number
#      of deleted documents.
#      NOTE: We could have use the DELETE method instead of the GET method
@app.get("/deleteOne")
def deleteProduct(productID: int):
    product = dbCollection.find_one({"ProductID": productID})
    if not product:
        return {"error": "Product doesn't exist Monsieur!"}
    
    result = dbCollection.delete_one({"ProductID": productID})
    print("message:", "Product deleted Monsieur!")
    return {"message": f"Product with {productID} has been successfully deleted!", "numberOfDeletedProducts": result.deleted_count}

#API Endpoint 5 - Searching for a product with a user-determined letter (GET)
# First off, we ask the user to enter a letter, that is then stored as a string.
#  Then, we use a regex expression called 'regexExpression' to match product namers that start
#  with a specific letter. We use the '^' symbol to make sure that we match the user's entered letter
#  with the first letter of the products in our database.
#   NOTE: We use the 're.escape()' function as a cool extra measure to prevent any Regex injection, which is
#   simply when an attacker wants to enter malicious patterns.
#    Moving on, we then want to make sure that the search is case-insensitive. This means if the user enters
#    the letter 'C' or 'c' for example, they are treated the same way. This is because all our products in the database
#    start with capital letters. 
@app.get("/startsWith")
def filteringProducts(userEnteredLetter: str = Query(..., description = "Enter a letter to filter our products!")):
    regexExpression = f"^{re.escape(userEnteredLetter)}"
    productsList = list(dbCollection.find({"Name": {"$regex": regexExpression, "$options": "i"}}))
    print("Filtered Products:", productsList)
    for product in productsList:
        product["_id"] = str(product["_id"])
    if not productsList:
        return { "message": f"Sorry, there are no products starting with the letter '{userEnteredLetter}' Monsieur!"}
    
    return productsList

#API Endpoint 6 - Return products from within a given range (GET)
# We start off by asking the user to enter an 'int' for the start of the rangfe and another 'int' for the end of the range.
#  Since we use the Query, we are making these parameters required, before any data is returned.
#   Next, we search for products in our database collection using the 'find()' function.
#   NOTE: '$gte' = greater than or equal, >=
#   NOTE: 'lte' = less than or equal <=
#    Penultimetaly, we limit the number of documents that are returned independant of the range with a limit of 10 products
#    and sort them in ascending order using the 'sort()' function.
#     Lastly, we return them, and if products within that range don't exist, we let the user know by sending them a message
@app.get("/paginate")
def filterProductsViaRange(startOfRangeID: int = Query(..., description = "Enter the Product ID you want to start from."),
                           endOfRangeID: int = Query (..., description = "Enter the Product ID you want to end at.")):
    
    products = list(dbCollection.find({ "ProductID": {"$gte": startOfRangeID, "$lte": endOfRangeID}}).sort("ProductID", 1).limit(10))
    print("Filtered Products in the selected range:", products)
    for product in products:
        product["_id"] = str(product["_id"])
    if not products:
        return {"message": f"There are no products between ProductID {startOfRangeID} and {endOfRangeID}"}
    
    return products

#API Endpoint 7 - Converting the 'UnitPrice' attribute from the stock currency to EUR (GET)
# We simply start off by retrieving the product we want to update from our collection, using
# the 'find_one()' function as we have already seen. 
#  If the product does not exist, we let the user know.
#   We then want to make sure that the updated price in EUR is up-to-date and not manually inserted
#    Therefore, we make a call to an external API to retrieve the exchange rate.
#     Subsequently, we need to calculate the converted price and store it in the 'USDToEUR' variable
#      We then convert the ID from its Mongo form to a string as we have done previously.
#       We then make a copy of the product whose unit price we are tring to change. This is because, we want to add
#       the price in EUR as a new field, rather than replacing the default USD one.
#        Once we have it copied and stored in 'productPriceinEUR' variable, we can then add a new attribute called
#        'UnitPriceEUR' and assign it the EURO converted price of the product
#          NOTE: We could have use the UPDATE method instead of the GET method
@app.get("/convert")
def convertDollarToEuro(productID: int):
    product = dbCollection.find_one({"ProductID": productID})
    if not product:
        return {"error": "The entered product doesn't exist!"}

    response = requests.get("https://open.er-api.com/v6/latest/USD")
    response.raise_for_status()
    exchangeRate = response.json()["rates"]["EUR"]
    USDToEUR = round(product["UnitPrice"] * exchangeRate, 2)
    product["_id"] = str(product["_id"])
    productPriceInEUR = product.copy()
    productPriceInEUR["UnitPriceEUR"] = USDToEUR

    return productPriceInEUR


