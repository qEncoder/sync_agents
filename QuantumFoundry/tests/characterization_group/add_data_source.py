from QF_sync_agents.characterization.sync_characterization import CharcterizationSyncCSV
from QF_sync_agents.characterization.sync_characterization_config import CharacterizationConfigCSV

from etiket_client.sync.backends.sources import add_sync_source#, remove_sync_source
from etiket_client.python_api.scopes import get_scope_by_name

import pathlib 

# path the the measurement data of the calibration measurements
# data_path = pathlib.Path(__file__).parent / 'data'
data_path = pathlib.Path(r'C:\Users\atosato\Downloads\test_sync')
print(data_path)

if not data_path.exists():
    raise ValueError(f"Data path {data_path} does not exist. Please correct the path.")

# scope to which the data will be uploaded
scope4upload = get_scope_by_name('Test_scope')

# sample name and set up will be added to every dataset that is uploaded from this location
config = CharacterizationConfigCSV(
  data_storage_location = data_path,
)

# # give a name to the sync agent (should be locally unique)
add_sync_source('characterization_sync_2', CharcterizationSyncCSV, config, scope4upload)