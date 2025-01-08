from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging 
from NetworkSecurity.entity.config_entity import (DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,
                                                  DataTransformationConfig)
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
        logging.info('Data Transformation Initiated')
        data_transformation_config = DataTransformationConfig(training_pipleine_config)
        data_transformation = DataTransformation(data_validation_arti,data_transformation_config)
        data_transformation_arti = data_transformation.initiate_data_transformation()
        print(data_transformation_arti)
        logging.info('Data Transformation Successful')





    except Exception as e:
        raise NetworksecurityException(e,sys)