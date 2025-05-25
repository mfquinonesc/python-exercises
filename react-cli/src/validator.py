import os 
import json
import re

def is_react_project(base_path:str = "."):

    package_json_path = os.path.join(base_path, 'package.json')

    if not os.path.exists(package_json_path):
        return False
    
    try: 
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            dependencies = package_data.get("dependencies", {})
            dev_dependencies = package_data.get("devDependencies", {})
            return 'react' in dependencies or 'react' in dev_dependencies
    
    except Exception as e:
        print(f"Error reading package.json: {e}")
        return False
    
    
def detect_typescript(base_path:str = "."):

    if os.path.exists(os.path.join(base_path, "tsconfig.json")):
        return True
    
    for root, _, files in os.walk(os.path.join(base_path, "src")):
        for file in files:
            if file.endswith(".ts") or file.endswith(".tsx"):
                return True
            
    return False


def check_working_directory(expected_folder_name:str):
    
    current_dir = os.path.basename(os.getcwd())    
    return bool(current_dir != expected_folder_name)
      

def check_required_files(files:list):
    
    for file in files:
        if not os.path.exists(file):
            return False
        
    return True


def check_file_path(file_path:str):

    pattern = r'^[a-zA-Z0-9/-]+$'

    if not bool(re.match(pattern, file_path)):        
        return False

    if file_path.startswith('/') or file_path.endswith('/'):       
        return False
    
    if file_path.startswith('-') or file_path.endswith('-'):       
        return False

    if "--" in file_path or "//" in file_path:
        return False    
   
    return True