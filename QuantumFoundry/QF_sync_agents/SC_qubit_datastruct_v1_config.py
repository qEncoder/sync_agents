import pathlib
import dataclasses

@dataclasses.dataclass
class SCSyncAgenetDataStructV1Config:
    data_storage_location: pathlib.Path
