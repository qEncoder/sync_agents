import pathlib
import os
import json
import datetime
import xarray
import pandas as pd
import logging
import xarray as xr
import re

from etiket_client.sync.base.sync_source_abstract import SyncSourceFileBase
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities, dataset_info, sync_item, FileType
from QF_sync_agents.characterization.sync_characterization_config import CharacterizationConfigCSV


logger = logging.getLogger(__name__)

class CharcterizationSyncCSV(SyncSourceFileBase):
    SyncAgentName = "CharcterizationSyncCSV"
    ConfigDataClass = CharacterizationConfigCSV
    MapToASingleScope = True
    LiveSyncImplemented = False
    level = 3  # {project_name}/{subject_id}/{measurement_folder}
    
    @staticmethod
    def rootPath(configData: CharacterizationConfigCSV) -> pathlib.Path:
        return pathlib.Path(configData.data_storage_location)

    @staticmethod
    def checkLiveDataset(configData: CharacterizationConfigCSV, syncIdentifier: sync_item, isNewest: bool) -> bool:
        # We assume measurements are only written when they are completed
        return False

    @staticmethod
    def syncDatasetNormal(configData: CharacterizationConfigCSV, syncIdentifier: sync_item):
        dataset_path = pathlib.Path(configData.data_storage_location) / syncIdentifier.dataIdentifier
        print(dataset_path)

        # Implement the synchronization of a dataset
        create_dataset(configData, syncIdentifier)
        
        # Upload info.json
        info_json_path = dataset_path / "info.json"
        upload_file_if_exists(info_json_path, "info.json", FileType.JSON, syncIdentifier)
        
        # Upload metadata.json
        metadata_json_path = dataset_path / "metadata.json"
        upload_file_if_exists(metadata_json_path, "metadata.json", FileType.JSON, syncIdentifier)

        data_csv_path = dataset_path / "measurement.csv"

        # upload all other files

        for file in dataset_path.rglob("*"):
            if file.is_file():
                # Apply exclusion only in the root directory (first level)
                if file.parent == dataset_path and file in {info_json_path, metadata_json_path, data_csv_path}:
                    continue
                upload_file_if_exists(file, file.name, file_type_from_extension(file), syncIdentifier)
        # for file in dataset_path.iterdir():
        #     if file.is_file() and file not in {info_json_path, metadata_json_path, data_csv_path}:
        #         upload_file_if_exists(file, file.name, file_type_from_extension(file), syncIdentifier)

        
        # Upload data.csv and convert to xarray
        if data_csv_path.exists():
            upload_file_if_exists(data_csv_path, "measurement.csv", FileType.UNKNOWN, syncIdentifier)
            # Convert CSV to xarray and upload
            try:
                df = pd.read_csv(data_csv_path)
                df.set_index(guess_index_columns(df), inplace=True)
                ds = xarray.Dataset.from_dataframe(df)
                ds = process_xarray_units(ds)
                f_info = file_info(
                    name="measurement",
                    fileName="measurement.hdf5",
                    created=datetime.datetime.fromtimestamp(data_csv_path.stat().st_mtime),
                    fileType=FileType.HDF5_NETCDF,
                    file_generator=""
                )
                sync_utilities.upload_xarray(ds, syncIdentifier, f_info)
            except Exception:
                logger.exception(f"Error converting {data_csv_path} to xarray dataset.")

    @staticmethod
    def syncDatasetLive(configData: CharacterizationConfigCSV, syncIdentifier: sync_item):
        raise NotImplementedError

# Helper functions

def upload_file_if_exists(file_path: pathlib.Path, file_name: str, file_type: FileType, syncIdentifier: sync_item):
    if file_path.exists():
        f_info = file_info(
            name=file_name,
            fileName=file_path.name,
            created=datetime.datetime.fromtimestamp(file_path.stat().st_mtime),
            fileType=file_type,
            file_generator="ProjectDataSync"
        )
        sync_utilities.upload_file(str(file_path), syncIdentifier, f_info)

def create_dataset(configData: CharacterizationConfigCSV, syncIdentifier: sync_item):
    dataset_path = pathlib.Path(configData.data_storage_location) / syncIdentifier.dataIdentifier
    dataset_name = extract_dataset_name(dataset_path)
    keywords = []
    attributes = {}
    
    # Parse info.json for dataset name and attributes
    info_json_path = dataset_path / "info.json"
    if info_json_path.exists():
        try:
            with info_json_path.open("r") as f:
                info_data = json.load(f)
                # dataset_name = f"{info_data.get('ProtocolName', '')}"
                info_data = {str(k): str(v) for k, v in info_data.items()}
                attributes.update(info_data)
        except Exception:
            logger.exception(f"Error reading {info_json_path}")
    
    # Add keywords from metadata.json
    metadata_json_path = dataset_path / "metadata.json"
    if metadata_json_path.exists():
        try:
            with metadata_json_path.open("r") as f:
                metadata_data = json.load(f)
                # Assuming we can use the keys of metadata as keywords
                keywords.extend(metadata_data.keys())
        except Exception:
            logger.exception(f"Error reading {metadata_json_path}")
    
    # When the folder was created, we take as the creation time of the dataset
    created = datetime.datetime.fromtimestamp(dataset_path.stat().st_mtime)
    
    ds_info = dataset_info(
        name=dataset_name,
        datasetUUID=syncIdentifier.datasetUUID,
        alt_uid=syncIdentifier.dataIdentifier,
        scopeUUID=syncIdentifier.scopeUUID,
        created=created,
        keywords=list(set(keywords)), 
        attributes=attributes
    )
    sync_utilities.create_ds(False, syncIdentifier, ds_info)


def extract_dataset_name(dataset_path: pathlib.Path) -> str:
    parts = dataset_path.name.split("_")
    return "_".join(parts[1:]) if len(parts) > 1 else "Dataset"

def file_type_from_extension(file: pathlib.Path) -> FileType:
    f_type = FileType.UNKNOWN
    if file.suffix.lower()==".hdf5" or file.suffix.lower()==".h5" or file.suffix.lower()==".nc":
        f_type = FileType.HDF5
    if file.suffix.lower()==".json":
        f_type = FileType.JSON
    if file.suffix.lower()==".txt":
        f_type = FileType.TEXT
    return f_type

def guess_index_columns(df):
    """
    Guesses the index columns of a pandas DataFrame. 
    This is not ideal but it's what can be done if it's not specified what the axis are.
    """
    columns = df.columns.tolist()
    total_rows = len(df)
    index_columns = [columns[0]]

    for col in columns[1:]:
        num_unique_values = df[col].nunique()
        
        if num_unique_values <= total_rows / 2:
            index_columns.append(col)
        else:
            break  # Stop adding columns when more than half the values are unique

    return index_columns


# Define the function to extract name and units
def extract_name_and_units(label):
    match = re.match(r"(.*?)(?:\s*\((.*?)\))?$", label)
    name = match.group(1).strip() if match else label
    units = match.group(2).strip() if match and match.group(2) else None
    return name, units


def process_xarray_units(ds):
    '''Rename variables and coordinates in the existing dataset and add units as attributes.'''
    # Rename data variables
    data_var_renames = {}
    for name, dataarray in ds.data_vars.items():
        new_name, units = extract_name_and_units(name)
        data_var_renames[name] = new_name
        if units:
            ds[name].attrs['units'] = units
    
    ds = ds.rename_vars(data_var_renames)
    
    # Rename coordinates
    coord_renames = {}
    for name, dataarray in ds.coords.items():
        new_name, units = extract_name_and_units(name)
        coord_renames[name] = new_name
        if units:
            ds[name].attrs['units'] = units
    
    ds = ds.rename(coord_renames)

    return ds