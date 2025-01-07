import yaml
import os
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
        


