from urllib.parse import quote_plus

from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://mpskkspm:Jatt@123@cluster0.t7woo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


'''
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient

# Your actual MongoDB username and password
username = "mpskkspm"
password = "Jatt@123"  # Example password, potentially containing special characters

# Escape username and password
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# Create the MongoDB URI with the escaped credentials
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.t7woo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

'''