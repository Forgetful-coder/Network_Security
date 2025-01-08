import os
import sys
import numpy as np
import pandas as pd


"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = "/Users/aayushaggarwal/Desktop/mlops_tute/Network_security/data_schema/schema.yaml"

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"

""" 
DATA INGESTED RELATED CONSTANT
"""

DATA_INGESTION_COLLECTION_NAME: str = "Phishing_data"
DATA_INGESTION_DATABASE_NAME: str = "Network_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


"""
DATA VALIDATION CONSTANTS
"""

DATA_VALIDATION_DIR_NAME: str = 'Data_Validation'
DATA_VALIDATION_VALID_DIR: str = 'Valid_Data'
DATA_VALIDATION_INVALID_DIR: str = 'Invalid_Data'
DATA_VALDIATION_DRIFT_DIR: str = 'Data_Drift'
DATA_VALDIATION_DRIFT_REPORT: str = 'report.yaml'

"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "Data_Transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "Transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "Transformed_Object"

## knn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


