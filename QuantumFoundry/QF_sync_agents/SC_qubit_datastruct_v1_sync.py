from etiket_client.sync.base.sync_source_abstract import SyncSourceFileBase
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item, FileType

from QF_sync_agents.SC_qubit_datastruct_v1_config import SCSyncAgenetDataStructV1Config

import pathlib, os, datetime, xarray, logging, re, tempfile, shutil, json

logger = logging.getLogger(__name__)

# job_id not included atm
# stand deviation saved in the attributes?


QF_SC_qubits_naming_scheme = re.compile(r"^(.+)[\/\\](.+)[\/\\](.+)[\/\\](.+)[\/\\](.+)[\/\\](.+)[\/\\](.+)[\/\\](.+)_(\d{6}).*$")

class SCSyncAgenetDataStructV1Agent(SyncSourceFileBase):
    SyncAgentName = "SC_sync_agent_data_struct_v1"
    ConfigDataClass = SCSyncAgenetDataStructV1Config
    MapToASingleScope = True
    LiveSyncImplemented = False
    level = 8
    
    @staticmethod
    def rootPath(configData: SCSyncAgenetDataStructV1Config) -> pathlib.Path:
        return pathlib.Path(configData.data_storage_location)

    @staticmethod
    def checkLiveDataset(configData: SCSyncAgenetDataStructV1Config, syncIdentifier: sync_item, isNewest: bool) -> bool:
        # to keep things simple, we assume here files are only written when they are completed (i.e. at the end of a measurement)
        return False
    
    @staticmethod
    def syncDatasetNormal(configData: SCSyncAgenetDataStructV1Config, syncIdentifier: sync_item):
        create_dataset(configData, syncIdentifier)

        dataset_path = pathlib.Path(os.path.join(configData.data_storage_location, syncIdentifier.dataIdentifier))
        for root, dirs, files in os.walk(dataset_path):
            if not root.endswith(".zarr") and not os.path.dirname(root).endswith(".zarr"):
                for file in files:
                    file_path = pathlib.Path(os.path.join(root, file))
                    
                    if file_path.is_dir():
                        continue
                    
                    f_type = FileType.UNKNOWN
                    if file.endswith(".hdf5") or file.endswith(".h5") or file.endswith(".nc"):
                        f_type = FileType.HDF5
                    if file.endswith(".json"):
                        f_type = FileType.JSON
                    if file.endswith(".txt"):
                        f_type = FileType.TEXT
                    
                    f_info = file_info(name = file_path.name, fileName = file,
                        created = datetime.datetime.fromtimestamp(file_path.stat().st_mtime),
                        fileType = f_type, file_generator = "")

                    sync_utilities.upload_file(file_path, syncIdentifier, f_info)
            elif root.endswith(".zarr"):
                #  compress the zarr file in temp folder
                folder_name =  os.path.basename(root)
                # foldername without .zarr
                file_name = folder_name[:-5]
                with tempfile.TemporaryDirectory() as temp_dir:
                    shutil.make_archive(os.path.join(temp_dir, f'{folder_name}'), 'zip', root)
                    # upload the zip file
                    f_info = file_info(name = f"{folder_name}.zip", fileName = f"{folder_name}.zip",
                        created = datetime.datetime.fromtimestamp(pathlib.Path(root).stat().st_mtime),
                        fileType = FileType.UNKNOWN, file_generator = "")
                    sync_utilities.upload_file(os.path.join(temp_dir, f"{folder_name}.zip"),
                                               syncIdentifier, f_info)
                
                try:   
                    xr_ds = xarray.open_zarr(root)
                    
                    f_info = file_info(name = file_name, fileName = f"{file_name}.hdf5",
                        created = datetime.datetime.fromtimestamp(pathlib.Path(root).stat().st_mtime),
                        fileType = FileType.HDF5_NETCDF, file_generator = "")
                    
                    sync_utilities.upload_xarray(xr_ds, syncIdentifier, f_info)
                except:
                    logger.exception(f"Could not open zarr file {root}")

    @staticmethod
    def syncDatasetLive(configData: SCSyncAgenetDataStructV1Config, syncIdentifier: sync_item):
        raise NotImplementedError

def create_dataset(configData: SCSyncAgenetDataStructV1Config, syncIdentifier: sync_item):    
    match = QF_SC_qubits_naming_scheme.match(syncIdentifier.dataIdentifier)
    
    creator = None
    device_name = None
    if match:
        creator = match.group(3)
        day, month, year, hhmmss = match.group(7), match.group(6), match.group(5), match.group(9)
        dataset_name = match.group(8).replace("_", " ")
        device_name = f"{match.group(1)}/{match.group(2)}"
    else:
        raise ValueError(f"Could not parse dataset identifier {syncIdentifier.dataIdentifier}")  
    
    logger.info(f"Creating dataset {dataset_name}")

    keywords = []
    attributes = {}
    if device_name:
        attributes["device_name"] = device_name
    
    try:
        json_file = os.path.join(configData.data_storage_location, syncIdentifier.dataIdentifier, "state/information.json")
        json_data = json.load(open(json_file))
        if "information" in json_data.keys():
            info = json_data["information"]
            if "user_name" in info.keys():
                creator = info["user_name"]
            if "fridge_name" in info.keys():
                attributes["fridge_name"] = info["fridge_name"]
            if "device_name" in info.keys():
                attributes["device_name"] = info["device_name"]
    except:
        print(f"Could not parse dataset information {syncIdentifier.dataIdentifier}")
    
    # try to assign subject_id
    try:
        json_file = os.path.join(configData.data_storage_location, "name_ID_mapping.json")
        json_data = json.load(open(json_file))
        device_name = attributes.get("device_name", None)
        if device_name in json_data.keys():
            attributes["subject_id"] = json_data[device_name]
    except:
        pass
    
    created = datetime.datetime(int(year), int(month), int(day), int(hhmmss[:2]), int(hhmmss[2:4]), int(hhmmss[4:6]))
    
    ds_info = dataset_info(name = dataset_name, datasetUUID = syncIdentifier.datasetUUID,
            alt_uid = syncIdentifier.dataIdentifier, scopeUUID = syncIdentifier.scopeUUID,
            created = created, keywords = list(keywords), creator=creator,
            attributes = attributes)
    
    sync_utilities.create_ds(False, syncIdentifier, ds_info)