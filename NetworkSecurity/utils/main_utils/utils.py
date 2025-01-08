import yaml
import os
import numpy as np
from NetworkSecurity.Exceptions.exceptions import NetworksecurityException
from NetworkSecurity.logging.logger import logging
import pickle
import dill
import sys

def read_yaml_file(file_path: str) -> dict:
    try:
        logging.info('Reading yaml file')
        with open(file_path, 'r') as file:
            content =  yaml.safe_load(file)
        logging.info('Content fetched successfully')
        return content
        
    except Exception as e:
        logging.info('Error occured')
        raise NetworksecurityException(e,sys)

def write_yaml_file(file_path: str, content: object, replace: bool =False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,'w') as file:
            yaml.dump(content,file,default_flow_style=False)

    except Exception as e:
        raise NetworksecurityException(e,sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworksecurityException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworksecurityException(e, sys) from e
    
        


