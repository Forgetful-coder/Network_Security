import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from NetworkSecurity.constants.training_pipeline import TARGET_COLUMN
from NetworkSecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from NetworkSecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifacts
)

from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException 
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_valdiation_artifact:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig):
        self.data_validation_artifact = data_valdiation_artifact
        self.data_transformation_config = data_transformation_config
    


    

    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe

        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def get_transformer_object(cls)->Pipeline:
        try:
            """
            Computes nan values using KNN Imputer

            Args: DATA_TRANSFORMATION_IMPUTER_PARAMS

            Output: Pipeline
            """
            logging.info('Inputing Nan Values Process inititated')
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline([('imputer',imputer)])
            save_object("final_model/preprocessor.pkl",processor)

            logging.info('Process completed Successfully')
            return processor
            
        except Exception as e:
            raise NetworksecurityException(e,sys)



    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            train_valid_file_path = self.data_validation_artifact.valid_train_file_path
            test_valid_file_path = self.data_validation_artifact.valid_test_file_path
            print(train_valid_file_path)
            print(test_valid_file_path)

            #Reading the valid train and test files
            train_df = DataTransformation.read_data(train_valid_file_path)
            test_df = DataTransformation.read_data(test_valid_file_path)

            #Seprating the train input and output and features
            input_train_features = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_feature = train_df[TARGET_COLUMN]

            #Seprating the train input and output and features
            input_test_features = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_feature = test_df[TARGET_COLUMN]

            #Transforming the target Feature from -1 to 0

            target_train_feature = target_train_feature.replace(-1,0)
            target_test_feature = target_test_feature.replace(-1,0)

            #Imputing nan values using KNN Imputer
            preprocessor = self.get_transformer_object()
            processed_train_input_features = preprocessor.fit_transform(input_train_features)
            processed_test_input_features = preprocessor.transform(input_test_features)

            #Creating train and test final numpy array
            train_arr = np.c_[processed_train_input_features,np.array(target_train_feature)]
            test_arr = np.c_[processed_test_input_features,np.array(target_test_feature)]


            #Saving the files to their respective Format
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,obj=preprocessor)

            #Creating Data Transformation Artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path)
            
            return data_transformation_artifact
        
        except Exception as e:
            raise NetworksecurityException(e,sys)


