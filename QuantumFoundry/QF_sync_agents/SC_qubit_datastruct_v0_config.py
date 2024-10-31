import pathlib
import dataclasses

@dataclasses.dataclass
class SCSyncAgenetDataStructV0Config:
    data_storage_location: pathlib.Path
    set_up: str
    sample_name : str