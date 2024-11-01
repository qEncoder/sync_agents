import os
from pathlib import Path
from datetime import datetime
import shutil
import json

project_name = "project_name"
subject_id = "subject_id"

info_data = {
    "Version": "1.0",
    "SubjectID_chip": "subject_id",
    "SubjectID_Device": f"subject_id_Device",
    "NickName": f"NickName",
    "Cooldown": "Cooldown_time",
    "Setup_fridge": "FridgeX",
    "UserID": "User123",
    "Platform": "PlatformY",
    "Component": "ComponentZ",
    "Step": "Initial",
    "SubStep": "SubInitial",
    "ProtocolName": "Protocol1",
    "WentNotAsExpected": False,
}



def organize_files_by_timestamp(old_data_path: Path, new_data_path: Path):
    # Ensure the given path is a directory
    if not old_data_path.is_dir():
        raise ValueError("The provided path is not a directory")
    new_data_path.mkdir(parents=True, exist_ok=True)

    # Loop through each file in the directory
    for file_path in old_data_path.iterdir():
        if file_path.is_file():  # Process only files
            # Get the file's creation time as a timestamp
            created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
            timestamp_str = created_time.strftime("%Y%m%d_%H%M%S")
            
            # Create the folder name as timestamp_file_name
            folder_name = f"{timestamp_str}_{file_path.stem}"
            target_folder = new_data_path / f"{project_name}/{subject_id}/{folder_name}"
            target_folder.mkdir(parents=True, exist_ok=True)

            # Define the target path for the file within the new folder
            if file_path.suffix == '.csv':
                target_file_path = target_folder / "measurement.csv"
            else:
                target_file_path = target_folder / file_path.name

            # Move and rename the file
            shutil.copy(str(file_path), str(target_file_path))
            print(f"copied {file_path.name} to {target_folder}")

            # Add info.json file
            with open(target_folder / "info.json", "w") as f:
                json.dump(info_data, f)


# Usage example
old_data_path = Path("/Users/atosato/Downloads/bluewhale1728488315392/2024-08-26 W4_Al_resonators4_B002019D02/2024-08-26 W4_Al_resonators4_B002019D02-run1-oldprotocol")
new_data_path = Path("/Users/atosato/Downloads/NQCP_data_char_reformatted")
organize_files_by_timestamp(old_data_path, new_data_path)
