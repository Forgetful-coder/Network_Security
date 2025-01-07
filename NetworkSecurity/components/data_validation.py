from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifacts
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging
from scipy.stats import ks_2samp ## To check for drift in the data 
from NetworkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import pandas as pd
import os,sys



class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworksecurityException
    
    def validate_number_of_columns(self,dataframe: pd.DataFrame) -> bool:
        try:
            number_of_cols = len(self._schema_config['columns'])
            logging.info(f'DataFrame must have {number_of_cols} columns')
            logging.info(f'DataFrame actually has {len(dataframe.columns)}')

            if len(dataframe.columns)==number_of_cols:
                return True
            return False
            
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,thereshold: float=0.05) -> bool:
        try:
            report={}
            status = False
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                is_same_dist = ks_2samp(d1,d2)
                pvalue = float(is_same_dist.pvalue)
                if thereshold<=pvalue:
                        is_found=False

                else:
                    is_found=True
                    status=True
                report.update({column:{
                    'pvalue':pvalue,
                    'status':is_found
                }})
            drift_report_file_path = self.data_validation_config.data_drift_file_name
            #Creating directories
            os.makedirs(os.path.dirname(drift_report_file_path),exist_ok=True)
            #Writing to the file
            write_yaml_file(file_path=drift_report_file_path,content=report)

            return status
        
        except Exception as e:
            raise NetworksecurityException(e,sys)



    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## reading the data
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            # Validating the Columns:
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if status:
                logging.info('Train DataFrame does not miss any columns')
            else:
                logging.info('Train DataFrame has missing columns')
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if status:
                logging.info('Test DataFrame does not miss any columns')
            else:
                logging.info('Test DataFrame has missing columns')
            
            #Check for Data Drift
            status_drift = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            if not status_drift:
                logging.info('Saving files to Valid Data Directory')
                data_valid_dir = self.data_validation_config.valid_data_dir
                os.makedirs(data_valid_dir,exist_ok=True)
                train_dataframe.to_csv(self.data_validation_config.train_valid_file,header=True,index=False)
                test_dataframe.to_csv(self.data_validation_config.test_valid_file,header=True,index=False)

                #DataValidationArtifacts
                logging.info('Generating Data Validation Artifacts for no Data Drift')
                data_validation_artifacts = DataValidationArtifacts(
                    validation_status=status_drift,
                    valid_train_file_path=self.data_validation_config.train_valid_file,
                    valid_test_file_path=self.data_validation_config.test_valid_file,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.data_drift_file_name
                )
                return data_validation_artifacts

            else:
                logging.info('Saving files to Invalid Data Directory')
                data_invalid_dir = self.data_validation_config.invalid_data_dir
                os.makedirs(data_invalid_dir,exist_ok=True)
                train_dataframe.to_csv(self.data_validation_config.train_invalid_file,header=True,index=False)
                test_dataframe.to_csv(self.data_validation_config.test_invalid_file,header=True,index=False)

                #DataValidationArtifacts
                logging.info('Generating Data Validation Artifacts for Data Drift')
                data_validation_artifacts = DataValidationArtifacts(
                    validation_status=status_drift,
                    valid_train_file_path=None,
                    valid_test_file_path=None,
                    invalid_train_file_path=self.data_validation_config.train_invalid_file,
                    invalid_test_file_path=self.data_validation_config.test_invalid_file,
                    drift_report_file_path=self.data_validation_config.data_drift_file_name
                )
                return data_validation_artifacts
            
            




        except Exception as e:
            raise NetworksecurityException(e,sys)
        
            

        