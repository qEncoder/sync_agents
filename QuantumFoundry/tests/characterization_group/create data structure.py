import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np

from mock_data_structure import projects_data

# Function to generate folder structure and files
def create_folder_structure(projects):
    for project in projects:
        project_name = project["project_name"]
        
        for subject in project["subjects"]:
            subject_id = subject["subject_id"]
            
            for measurement in subject["measurements"]:
                datetime_str = measurement["datetime"].timestamp() #.strftime("%Y%m%d_%H%M%S")
                measurement_type = measurement["measurement_type"]
                
                # Define folder path
                base_dir = Path(__file__).parent
                print(base_dir)
                folder_path = base_dir / Path(f"data/{project_name}/{subject_id}/{datetime_str}_{measurement_type}")
                folder_path.mkdir(parents=True, exist_ok=True)
                
                # Create info.json
                info_data = {
                    "Version": "1.0",
                    "SubjectID_chip": subject_id,
                    "SubjectID_Device": f"{subject_id}_Device",
                    "NickName": f"{subject_id}_Nick",
                    "Cooldown": measurement["datetime"].isoformat(),
                    "Setup_fridge": "FridgeX",
                    "UserID": "User123",
                    "Platform": "PlatformY",
                    "Component": "ComponentZ",
                    "Step": "Initial",
                    "SubStep": "SubInitial",
                    "ProtocolName": "Protocol1",
                    "WentNotAsExpected": False,
                }
                info_path = folder_path / "info.json"
                with open(info_path, "w") as info_file:
                    json.dump(info_data, info_file, indent=4)
                
                # Create metadata.json with random content
                metadata_data = {
                    "description": "Sample metadata for testing",
                    "additional_info": "Additional metadata content",
                    "generated_on": datetime.now().isoformat()
                }
                metadata_path = folder_path / "metadata.json"
                with open(metadata_path, "w") as metadata_file:
                    json.dump(metadata_data, metadata_file, indent=4)
                
                # Generate CSV with x and y columns
                data_path = folder_path / "measurement.csv"
                data_df = pd.DataFrame({
                    "x": np.linspace(0, 10, 100),
                    "y": np.sin(np.linspace(0, 10, 100))
                })
                data_df.to_csv(data_path, index=False)
                
                print(f"Created structure for project {project_name}, subject {subject_id}, measurement {datetime_str}_{measurement_type}")

# Run the function
create_folder_structure(projects_data)
