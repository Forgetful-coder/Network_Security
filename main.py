from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging 
from NetworkSecurity.entity.config_entity import (DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig)
import sys


if __name__=='__main__':
    try:
        logging.info('Data Ingestion Initiated')
        training_pipleine_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipleine_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_arti = data_ingestion.intiate_data_ingestion_config()
        print(data_ingestion_arti)
        logging.info('Data Ingestion Successful')
        logging.info('Data Validation Initiated ')
        data_validation_config = DataValidationConfig(training_pipleine_config)
        data_validation = DataValidation(data_ingestion_arti,data_validation_config)
        data_validation_arti = data_validation.initiate_data_validation()
        print(data_validation_arti)
        logging.info('Data Validation Successful')




    except Exception as e:
        raise NetworksecurityException(e,sys)