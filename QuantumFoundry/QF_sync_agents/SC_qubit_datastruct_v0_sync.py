from etiket_client.sync.base.sync_source_abstract import SyncSourceFileBase
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item, FileType

from QF_sync_agents.SC_qubit_datastruct_v0_config import SCSyncAgenetDataStructV0Config

import pathlib, os, datetime, xarray, logging, re

logger = logging.getLogger(__name__)

QF_SC_qubits_naming_scheme = re.compile(r"^(.+) (\d{4})[\\\/](\d{2})[\\\/](\d{2})[\\\/](.+).(\d{6}).*$")

class SCSyncAgenetDataStructV0Agent(SyncSourceFileBase):
    SyncAgentName = "SC_sync_agent_data_struct_v0"
    ConfigDataClass = SCSyncAgenetDataStructV0Config
    MapToASingleScope = True
    LiveSyncImplemented = False
    level = 4
    
    @staticmethod
    def rootPath(configData: SCSyncAgenetDataStructV0Config) -> pathlib.Path:
        return pathlib.Path(configData.data_storage_location)

    @staticmethod
    def checkLiveDataset(configData: SCSyncAgenetDataStructV0Config, syncIdentifier: sync_item, isNewest: bool) -> bool:
        # to keep things simple, we assume here files are only written when they are completed (i.e. at the end of a measurement)
        return False
    
    @staticmethod
    def syncDatasetNormal(configData: SCSyncAgenetDataStructV0Config, syncIdentifier: sync_item):
        create_dataset(configData, syncIdentifier)

        dataset_path = pathlib.Path(os.path.join(configData.data_storage_location, syncIdentifier.dataIdentifier))
        for root, dirs, files in os.walk(dataset_path):
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
                    fileType = f_type)

                sync_utilities.upload_file(file_path, syncIdentifier, f_info)
                        
                if (file.endswith(".hdf5") or file.endswith(".h5") or file.endswith(".nc")):
                    # make a 2nd version that converts netcdf3 to netcdf4
                    xr_ds = convert_netcdf3_to_netcdf4_compat_xarray(file_path)
                    
                    # TODO : collect keywords
                    f_info = file_info(name = file_path.name, fileName = file,
                        created = datetime.datetime.fromtimestamp(file_path.stat().st_mtime),
                        fileType = FileType.HDF5_NETCDF, file_generator = "")
                    
                    sync_utilities.upload_xarray(xr_ds, syncIdentifier, f_info)

    @staticmethod
    def syncDatasetLive(configData: SCSyncAgenetDataStructV0Config, syncIdentifier: sync_item):
        raise NotImplementedError

def create_dataset(configData: SCSyncAgenetDataStructV0Config, syncIdentifier: sync_item):    
    match = QF_SC_qubits_naming_scheme.match(syncIdentifier.dataIdentifier)
    
    if match:
        creator = match.group(1)
        day, month, year, hhmmss = match.group(4), match.group(3), match.group(2), match.group(6)
        dataset_name = match.group(5).replace("_", " ")
    else:
        raise ValueError(f"Could not parse dataset identifier {syncIdentifier.dataIdentifier}")  
    
    logger.info(f"Creating dataset {dataset_name}")

    keywords = []
    attributes = {"set_up": configData.set_up, "sample_name": configData.sample_name}
    
    created = datetime.datetime(int(year), int(month), int(day), int(hhmmss[:2]), int(hhmmss[2:4]), int(hhmmss[4:6]))
    
    ds_info = dataset_info(name = dataset_name, datasetUUID = syncIdentifier.datasetUUID,
            alt_uid = syncIdentifier.dataIdentifier, scopeUUID = syncIdentifier.scopeUUID,
            created = created, keywords = list(keywords), creator=creator,
            attributes = attributes)
    
    sync_utilities.create_ds(False, syncIdentifier, ds_info)
    
def convert_netcdf3_to_netcdf4_compat_xarray(path):
    ds_old = xarray.open_dataset(path)
    
    dim_coords = {}
    
    for dim in ds_old.dims:
        coords = {}
        
        first_coord = None
        for coord in ds_old.coords[dim].coords:
            if first_coord is None:
                first_coord = coord
                coords[coord] = ds_old.coords[dim][coord].values
            else:
                coords[coord] = (first_coord, ds_old.coords[dim][coord].values)
        
        if not coords:
            coords[dim] = ds_old.coords[dim].values
        
        dim_coords[dim] = coords
    
    variables = {}
    for var in ds_old.data_vars:
        coords = []
        for dim in ds_old[var].dims:
            coords.append(next(iter(dim_coords[dim])))
        
        variables[var] = (coords, ds_old[var].values)
    
    ds_new = xarray.Dataset(variables, coords={k : v for coords in dim_coords.values() for k, v in coords.items()})
    
    # assign attributes
    ds_new.attrs = ds_old.attrs
    for var in list(ds_old.data_vars) + list(ds_old.coords):
        ds_new[var].attrs = ds_old[var].attrs
    
    # check for the presence of standard deviation variables
    data_vars = list(ds_new)
    for var_name in data_vars:
        if var_name.endswith("__error") and var_name[:-7] in data_vars:
            ds_new[var_name[:-7]].attrs['__std'] = var_name
            ds_new[var_name].attrs['__is_std'] = 1

    return ds_new