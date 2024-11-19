Automatic Folder Generator
==========================

This script creates arbitrary folder structures that can be synchronized with the [synchronization tool](https://docs.dataqruiser.com/setting_up_synchronisation.html#setting-up-a-synchronization-for-a-filebase-source).

The configuration for the synchronization can be specified in the folder_config.yaml file. After setting up the configuration, run the script:

```bash
python folder_maker.py
```

**Note**: The [qDrive](https://docs.dataqruiser.com/installation.html) package must be installed for this script to work.


The folder_config.yaml file 
---------------------------

An example configuration file:

```yaml
root_folder: N:/SCI-NBI-Cleanroom/NQCP/SC-platform
attributes:
  - Initials: DSDK
  - SubjectID: A001B001
keywords: []  # Optional
skip: []      # Optional
folders:
  - "1_Resonators/$SubjectID/0_Design/"
  - "1_Resonators/$SubjectID/1_Exposure/"
  - "1_Resonators/$SubjectID/2_OpticalImages/0_Cleaning/"
  - "1_Resonators/$SubjectID/2_OpticalImages/1_Development/"
  - "1_Resonators/$SubjectID/2_OpticalImages/2_Etch/1_PostEtch/"
  - "1_Resonators/$SubjectID/2_OpticalImages/2_Etch/2_PostStrip/"
```

Fields:

- root_folder : Specifies the directory where the folders should be created.
- attributes : Defines attributes to be added.
- keywords : Optional list of keywords to add.
- skip : Optional list of patterns to skip during upload (e.g., "*.json" to skip all JSON files).
- folders : List of folder paths. Variables (e.g., $SubjectID) will be replaced with values from the attributes section. An error will be raised if the attribute is not present.

The folder_maker.py file
------------------------

This file contains the Python code that creates the folder structures.

To update an existing folder structure, the script can be rerun. Existing configuration files (_QH_dataset_info.yaml) will be updated with the new attributes and keywords. The synchronization tool will reflect these changes in the database.