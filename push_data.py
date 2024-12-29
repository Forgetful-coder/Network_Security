from dotenv import load_dotenv
import pymongo
import certifi
import pandas as pd
import numpy as np
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging
import os
import sys
import json

load_dotenv()

os.environ['MONGODB_URI'] = os.getenv('MONGODB_URI')

ca = certifi.where()


class NetworkDataExtract:
    
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())

            return records
        
        except Exception as e:
            NetworksecurityException(e,sys)
    

    def insert_data_to_mongodb(self,database,collections,records):
        try:
            self.database = database
            self.collection = collections
            self.records = records

            self.mongodb_client = pymongo.MongoClient(os.environ['MONGODB_URI'])
            self.database = self.mongodb_client[self.database]

            self.collection =  self.database[self.collection]
            self.collection.insert_many(self.records)

            return(len(self.records))

        except Exception as e:
            NetworksecurityException(e,sys)

if __name__=='__main__':
    ns_obj = NetworkDataExtract()
    FILE_PATH = '/Users/aayushaggarwal/Desktop/mlops_tute/Network_security/NetworkData/phisingData.csv'
    DATABASE = 'Network_data'
    COLLECTION  = 'Phishing_data'
    records = ns_obj.csv_to_json(FILE_PATH)
    #print(records)
    no_of_records = ns_obj.insert_data_to_mongodb(DATABASE,COLLECTION,records)
    print(no_of_records)
