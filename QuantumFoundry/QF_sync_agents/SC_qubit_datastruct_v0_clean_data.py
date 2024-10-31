import os
import re
import shutil, pathlib


# Define the regex pattern for matching the desired file structure
correct_name = re.compile(r'^(.+) (\d{4})[\\/](\d{2})[\\/](\d{2})[\\/](.+)_(\d{6})')
faulty_name = re.compile(r'^(.+) (\d{4})[\\/](\d{2})[\\/](\d{2})[\\/](.+)[\\/](.+)_(\d{6})')
expected_parent_of_parent = re.compile(r'^(.+) (\d{4})[\\/](\d{2})[\\/](\d{2})')

def organize_files(root_dir):
    root_dir = pathlib.Path(root_dir)
    
    if not root_dir.exists():
        raise ValueError(f"Data path {root_dir} does not exist. Please correct the path.")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        folder_name = os.path.basename(dirpath)
        parent_dir = os.path.dirname(dirpath)
        parent_of_parent_dir = os.path.dirname(os.path.dirname(dirpath))
        if faulty_name.match(dirpath) and expected_parent_of_parent.match(parent_of_parent_dir):
            if correct_name.match(os.path.join(parent_of_parent_dir, folder_name)):
                print(f"Moving {dirpath} to {os.path.join(parent_of_parent_dir, folder_name)}\n")
                shutil.move(os.path.join(dirpath), os.path.join(parent_of_parent_dir, folder_name))
                
            if not os.listdir(parent_dir):
                shutil.rmtree(parent_dir)
                print(f"Removed empty directory {parent_dir}\n")
