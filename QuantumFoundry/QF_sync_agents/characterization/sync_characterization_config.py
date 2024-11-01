import pathlib
import dataclasses

@dataclasses.dataclass
class CharacterizationConfigCSV:
    data_storage_location: pathlib.Path
