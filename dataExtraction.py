#In this file, we want to first load and read our 'products.csv' file.
# We then want to convert the file into a JSON format
#  After that, we then will create a client that will allow us to connect to our cloud-based database
#   Next, we will choose the database and specific collection we want to send the product data to
#    Lastly, we will want to insert the loaded CSV data into the database.

import pandas as pd
from pymongo import MongoClient

#STEP 1: We start by loading the CSV file
csvFile = pd.read_csv("products.csv")

#STEP 2: Then, we convert the CSV file into JSON format
jsonFile = csvFile.to_dict(orient = "records")

#STEP 3: Next, we connect to our MongoDB Schema-Less Database
client = MongoClient("mongodb+srv://root:root@cluster0.uaqpqn8.mongodb.net/?appName=Cluster0")

#STEP 4: Subsequently, we select our newly created database and specific collection
db = client["assignment1"]
dbCollection = db["products"]

#STEP 5: Lastly, we insert our JSON data into the database
dbCollection.insert_many(jsonFile)
print("Data inserted successfully!")