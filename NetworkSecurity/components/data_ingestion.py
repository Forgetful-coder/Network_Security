import numpy as  np
import pandas  as pd
from typing import List
from sklearn.model_selection import train_test_split
import pymongo
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging 
from dotenv import load_dotenv
import sys
import os

load_dotenv()

os.environ['MONGODB_URI'] = os.getenv('MONGODB_URI')

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    
    def export_data_collection(self):

        """
        Read the data from mongo_DB
        """
        try:
            datbase_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(os.environ['MONGODB_URI'])
            records = self.mongo_client[datbase_name][collection_name]

            df = pd.DataFrame(list(records.find()))
            if '_id' in df.columns.to_list():
                df = df.drop(columns=['_id'],axis=1)
            
            df.replace({'na':np.nan},inplace=True)
            return df

        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def export_data_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            ## Creating the folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,header=True,index=False)
            return dataframe

        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def train_test_gen(self,dataframe:pd.DataFrame):

        """
        Train and Test Split Of Data
        """
        try:
            logging.info('Initiating train_test_split')
            train_set,test_set = train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info('Done')

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info('Exporting data to respective train and test file paths')
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
            )
            logging.info('Exported train and test data successfully')
            
        except Exception as e:
            raise NetworksecurityException(e,sys)

    
    def intiate_data_ingestion_config(self):
        """
        Initate data ingestion step
        """
        try:
            dataframe = self.export_data_collection()
            dataframe = self.export_data_feature_store(dataframe)
            self.train_test_gen(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            return (data_ingestion_artifact)



        
        except Exception as e:
            raise NetworksecurityException(e,sys)

