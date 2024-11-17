'''
import os
import sys
import json
    
from dotenv import load_dotenv
load_dotenv()

import urllib.parse

# URL-encode the username and password
username = "mpskkspm"
password = "Jatt@123"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Use the encoded username and password in the connection URI
MONGO_DB_URL = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.t7woo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

##MONGO_DB_URL=os.getenv("MONGO_DB_URL")  
print(MONGO_DB_URL) 
import certifi
ca=certifi.where()
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def csv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="Manpreet"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
'''

import os
import sys
import json
import urllib.parse
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables from .env file
load_dotenv()

# URL-encode the username and password
username = "mpskkspm"
password = "Jatt@123"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Use the encoded username and password in the connection URI
MONGO_DB_URL = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.t7woo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Optionally, you can load the URL from the .env file:
# MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            # Read the CSV file into a DataFrame
            data = pd.read_csv(file_path)
            # Reset the index and convert DataFrame to a list of dictionaries
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records  # Make sure to return the records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            if not isinstance(records, list) or not records:
                raise ValueError("The records parameter must be a non-empty list of dictionaries.")
            
            self.database = database
            self.collection = collection
            self.records = records

            # Establish MongoDB connection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            # Insert the records into MongoDB
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    # Define the file path, database, and collection name
    FILE_PATH = r"Network_Data\phisingData.csv"  # Use raw string to avoid escape sequences
    DATABASE = "Manpreet"
    Collection = "NetworkData"

    networkobj = NetworkDataExtract()

    # Convert CSV to JSON format
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)

    # Print the records to ensure they are loaded correctly
    print(f"Loaded records: {records}")

    # Insert data into MongoDB
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(f"Inserted {no_of_records} records.")
