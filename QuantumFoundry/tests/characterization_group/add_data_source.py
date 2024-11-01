from QF_sync_agents.SC_qubit_datastruct_v1_sync import SCSyncAgenetDataStructV1Agent
from QF_sync_agents.SC_qubit_datastruct_v1_config import SCSyncAgenetDataStructV1Config

from etiket_client.sync.backends.sources import add_sync_source#, remove_sync_source
from etiket_client.python_api.scopes import get_scope_by_name

import pathlib 

# path the the measurement data of the calibration measurements
data_path = pathlib.Path(__file__).parent / 'data'
print(data_path)

if not data_path.exists():
    raise ValueError(f"Data path {data_path} does not exist. Please correct the path.")

# scope to which the data will be uploaded
scope4upload = get_scope_by_name('test_data_characterization')

# sample name and set up will be added to every dataset that is uploaded from this location
config = SCSyncAgenetDataStructV1Config(
  data_storage_location = data_path,
)

# # give a name to the sync agent (should be locally unique)
add_sync_source('characterization_sync', SCSyncAgenetDataStructV1Agent, config, scope4upload)