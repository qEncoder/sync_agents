from datetime import datetime, timedelta
import random

# Updated sample input data with dates in October 2024
projects_data = [
    {
        "project_name": "Project_A",
        "subjects": [
            {
                "subject_id": "SUB123",
                "measurements": [
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type2",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type3",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                ]
            },
            {
                "subject_id": "SUB124",
                "measurements": [
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type2",
                    },
                ]
            },
        ]
    },
    {
        "project_name": "Project_B",
        "subjects": [
            {
                "subject_id": "SUB200",
                "measurements": [
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type2",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type3",
                    },
                ]
            },
            {
                "subject_id": "SUB201",
                "measurements": [
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type2",
                    },
                ]
            },
        ]
    },
    {
        "project_name": "Project_C",
        "subjects": [
            {
                "subject_id": "SUB300",
                "measurements": [
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type3",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type2",
                    },
                ]
            },
            {
                "subject_id": "SUB301",
                "measurements": [
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime.now() + timedelta(seconds=random.randint(0, 60)),
                        "measurement_type": "Type3",
                    },
                ]
            },
        ]
    },
]
