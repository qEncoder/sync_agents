import re, yaml, pathlib, copy

valid_folder_name = re.compile(r'^[a-zA-Z0-9$][a-zA-Z0-9_\/\\$]+[\/\\]$')
variable_name_in_folder = re.compile(r'[$][a-zA-Z0-9_]+[\/\\]')

def create_folders():
    with open('folder_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    try :
        root_folder = pathlib.Path(config['root_folder'])
    except KeyError:
        raise ValueError("root_folder key not found in the YAML file.")
        
    if not root_folder.exists():
        raise ValueError(f"Data path {root_folder} does not exist. Please provide the correct path.")

    attributes = {k:v for attr in config['attributes'] for k,v in attr.items()}
    
    QH_dataset_info_base = {}
    QH_dataset_info_base['version'] = '0.1'
    QH_dataset_info_base['attributes'] = attributes
    QH_dataset_info_base['keywords'] = [] if 'keywords' not in config else config['keywords']
    folders = config['folders']
    
    folders_validated = []
    for folder in folders:
        if not valid_folder_name.match(folder):
            raise ValueError(f"Invalid folder name: {folder}. The folder should start with a letter or number and end with slash (/).")
        for match in variable_name_in_folder.findall(folder):
            variable = match[1:-1]
            if variable not in attributes:
                raise ValueError(f"Variable {variable} not found in the attributes. Please add it to the attributes in the YAML file.")
            folder = folder.replace(match[:-1], attributes[variable])
            folders_validated.append(folder)
    
    print("Starting folder creation :\n")
    
    print('Set attributes :')
    for key, value in attributes.items():
        print(f"\t{key} : {value}")
    
    print('\nProgress :')
    print("----------")
    # make the folders
    for folder in folders_validated:
        folder_path = root_folder / folder
        if folder_path.exists():
            print(f"Folder already exists: {folder}")
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"Folder created: {folder}")
        
        QH_dataset_info = copy.deepcopy(QH_dataset_info_base)
        QH_dataset_info['expected_path'] = str(folder_path)
        QH_dataset_info['keywords'] += extract_keywords_from_path(folder)
        
        yaml_file_path = folder_path / '_QH_dataset_info.yaml'
        exists = yaml_file_path.exists()
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(QH_dataset_info, yaml_file)
        if exists:
            print(f"\t _QH_dataset_info.yaml updated")
        else:
            print(f"\t _QH_dataset_info.yaml added")

def extract_keywords_from_path(folder : str):
    items = re.split(r'[_/]', folder)
    # if item is number or empty string, ignore it
    return [item for item in items if not item.isdecimal() and item != '']
    
create_folders()