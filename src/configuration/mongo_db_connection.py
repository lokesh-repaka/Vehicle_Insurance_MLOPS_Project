import os
import sys
import pymongo
import certifi
from dotenv import load_dotenv

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load environment variables from .env file
load_dotenv()


ca =  certifi.where()

class MongoDBClient():
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database

    Attribites:
    -----------
    client: MongoClient
        A shared MongoClient instance for the class
    database :Database
        The specific database instance that MonogDBclient connects to


    Methods:
    ---------
    __init__(database_name:str)--> None
        Intializes the MongoDB connection using the given database name
    """

    client = None

    def __init__(self,database_name:str=DATABASE_NAME)->None:
        """
        Initializes a connection th the mongoDB database if no existing connction is founc it establishes a new one

        parameters:
        database_name: str, optional
            Name of the MongoDB database to connect to defualt is set by DATABASE_NAME constant

        Raises:
        -------
        MyException
            If there is an issue connecting t  MongoDb or if the  environment variable for the MongoDb URL is not set
        """

        try:
            if MongoDBClient.client is None:
                mongo_db_url =  os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY} is not set")
                
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("mongodb connection succesful")


        except Exception as e:
            raise MyException(e, sys)