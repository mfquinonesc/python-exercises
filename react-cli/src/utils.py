import re 

def to_kebab_case(text:str):
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    return text.lower()


# This function formats the file path, depending on whether it is 
# a component or not, formats the last folder name
def format_path(file_path:str, is_component = False):
    
    folders = file_path.split('/')     

    formatted_folders = []
    for folder in folders:
        formatted_folders.append(to_kebab_case(folder))

    if is_component:
        component_name = folders.pop()
        formatted_folders.pop()
        formatted_folders.append(component_name)      

    return '/'.join(formatted_folders)