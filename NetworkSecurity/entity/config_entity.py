from datetime import datetime
import os
from NetworkSecurity.constants import training_pipeline


print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)



class TrainingPipelineConfig:

    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime('"%m_%Y_%d_%H_%M_%S"')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp: str = timestamp
    

class DataIngestionConfig:
    """
    Setting up Data Ingestion Config
    """

    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
            )
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    """
    Setting up Data Validation Config
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir: str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.train_valid_file: str = os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.test_valid_file: str = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.train_invalid_file: str = os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.test_invalid_file: str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)

        self.data_drift_file_name = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALDIATION_DRIFT_DIR,
            training_pipeline.DATA_VALDIATION_DRIFT_REPORT
        )



class DataTransformationConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)