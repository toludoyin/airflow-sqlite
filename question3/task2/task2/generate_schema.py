import os
import json
import jsonschema
from jsonschema import validate
from pathlib import Path

def infer_schema(data):
    def get_type(value):
        if isinstance(value, str):
            return "STRING"
        elif isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, list):
            if all(isinstance(i, str) for i in value):
                return "ENUM ARRAY"
            elif all(isinstance(i, dict) for i in value):
                return "ARRAY"
            else:
                return "ARRAY"
        elif isinstance(value, dict):
            return "OBJECT"
        return "UNKNOWN"

    def build_schema(d):
        schema = {}
        for key, value in d.items():
            schema[key] = {
                "type": get_type(value),
                "tag": "",
                "description": "",
                "required": False
            }
            if isinstance(value, dict):
                schema[key].update(build_schema(value))
        return schema
    
    return build_schema(data)

def main():
    # reads JSON files from the data folder
    data_folder = Path('./data/')
    schema_folder = Path('./schema/')
    schema_folder.mkdir(parents=True, exist_ok=True)
    
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.json'):
            file_path = data_folder / file_name
            with open(file_path, 'r') as f:
                json_data = json.load(f)
            
            if 'message' in json_data:
                schema = infer_schema(json_data['message'])
                
                #schema to file
                schema_file_name = file_name.replace('.json', '_schema.json')
                schema_file_path = schema_folder / schema_file_name
                with open(schema_file_path, 'w') as f:
                    json.dump(schema, f, indent=4)
                
                print(f"Schema for {file_name} has been written to {schema_file_path}")

if __name__ == "__main__":
    main()
