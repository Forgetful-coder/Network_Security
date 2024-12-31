from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging 
from NetworkSecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
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


    except Exception as e:
        raise NetworksecurityException(e,sys)