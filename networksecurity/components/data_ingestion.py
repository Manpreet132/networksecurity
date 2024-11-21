import os
import sys
import numpy as np
import pandas as pd
import pymongo
import urllib.parse
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

load_dotenv()

# MongoDB credentials
username = "mpskkspm"
password = "Jatt@123"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# MongoDB connection URL
MONGO_DB_URL = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.t7woo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read data from MongoDB
        """
        try:
            # Get database and collection names from config
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            logging.info(f"Connecting to MongoDB: Database={database_name}, Collection={collection_name}")

            # MongoDB client connection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            # Fetching data from the collection
            documents = list(collection.find())
            if not documents:
                logging.warning(f"No documents found in collection {collection_name}. Please check the database.")
                return pd.DataFrame()  # Return empty DataFrame if no data found

            # Convert data to DataFrame
            df = pd.DataFrame(documents)
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)

            # Replace 'na' with NaN
            df.replace({"na": np.nan}, inplace=True)

            # Log dataframe shape after import
            logging.info(f"Data loaded successfully from MongoDB. Shape of dataframe: {df.shape}")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Creating folder if not exists
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Data exported to feature store at: {feature_store_file_path}")
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            if dataframe.empty:
                raise NetworkSecurityException("Dataframe is empty, cannot perform train/test split.", sys)

            # Perform train/test split
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train/test split successfully.")

            # Create directories if not exist
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

            # Export train and test datasets to CSV
            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)

            logging.info(f"Train and test data saved to: {train_file_path} and {test_file_path}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            # Step 1: Export data from MongoDB
            dataframe = self.export_collection_as_dataframe()

            # Check if DataFrame is empty after exporting
            if dataframe.empty:
                raise NetworkSecurityException("Dataframe is empty after exporting from MongoDB", sys)

            # Step 2: Export to feature store
            self.export_data_into_feature_store(dataframe)

            # Step 3: Perform train/test split
            self.split_data_as_train_test(dataframe)

            # Step 4: Create and return artifact for data ingestion
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
