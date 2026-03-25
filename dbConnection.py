from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:root@cluster0.uaqpqn8.mongodb.net/?appName=Cluster0")

db = client["assignment1"]
dbCollection = db["products"]