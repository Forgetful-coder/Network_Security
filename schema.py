from NetworkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import os
import pandas as pd
import yaml

def generate_scehema_file(file_path, output_yaml_file=SCHEMA_FILE_PATH):
    df = pd.read_csv(file_path)
    schema={'columns':[]}
    for col in df.columns:
        col_dtype = str(df[col].dtype)

        schema['columns'].append({
            col:col_dtype
        })
    dir_path = os.path.dirname(output_yaml_file)
    os.makedirs(dir_path,exist_ok=True)
    
    with open(output_yaml_file,'w') as yaml_file:
        yaml.dump(schema,yaml_file,default_flow_style=False)
if __name__ == '__main__':
    generate_scehema_file('/Users/aayushaggarwal/Desktop/mlops_tute/Network_security/NetworkData/phisingData.csv')