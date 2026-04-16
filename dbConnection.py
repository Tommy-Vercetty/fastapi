#This is our file to connect to the database. We put this in a seperate file
# so that all the API code and database related code were seperate.
from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:root@cluster0.uaqpqn8.mongodb.net/?appName=Cluster0")

#We store the name of our database in a variable called 'db'
db = client["assignment1"]
#We store the name of the collection our products reside in, in a variable called 'dbConnection'
dbCollection = db["products"]