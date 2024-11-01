from datetime import datetime

# Updated sample input data with dates in October 2024
projects_data = [
    {
        "project_name": "Project_A",
        "subjects": [
            {
                "subject_id": "SUB123",
                "measurements": [
                    {
                        "datetime": datetime(2023, 10, 31, 15, 30),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime(2023, 11, 1, 9, 45),
                        "measurement_type": "Type2",
                    },
                    {
                        "datetime": datetime(2024, 10, 1, 10, 15),
                        "measurement_type": "Type3",
                    },
                    {
                        "datetime": datetime(2024, 10, 15, 14, 0),
                        "measurement_type": "Type1",
                    },
                ]
            },
            {
                "subject_id": "SUB124",
                "measurements": [
                    {
                        "datetime": datetime(2023, 10, 31, 16, 0),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime(2024, 10, 10, 11, 30),
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
                        "datetime": datetime(2024, 10, 5, 8, 45),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime(2024, 10, 20, 13, 15),
                        "measurement_type": "Type2",
                    },
                    {
                        "datetime": datetime(2024, 10, 25, 15, 30),
                        "measurement_type": "Type3",
                    },
                ]
            },
            {
                "subject_id": "SUB201",
                "measurements": [
                    {
                        "datetime": datetime(2024, 10, 3, 9, 0),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime(2024, 10, 12, 10, 45),
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
                        "datetime": datetime(2024, 10, 7, 16, 0),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime(2024, 10, 15, 9, 30),
                        "measurement_type": "Type3",
                    },
                    {
                        "datetime": datetime(2024, 10, 31, 17, 45),
                        "measurement_type": "Type2",
                    },
                ]
            },
            {
                "subject_id": "SUB301",
                "measurements": [
                    {
                        "datetime": datetime(2024, 10, 18, 11, 15),
                        "measurement_type": "Type1",
                    },
                    {
                        "datetime": datetime(2024, 10, 24, 14, 0),
                        "measurement_type": "Type3",
                    },
                ]
            },
        ]
    },
]
