from etiket_client.sync.backends.filebase.converters.base import FileConverter

import pathlib, pandas as pd, xarray, re

class ZarrToZipConverter(FileConverter):
    input_type = 'csv' # Specify the input file type
    output_type = 'hdf5' # Specify the output file type

    def convert(self) -> pathlib.Path:
        df = pd.read_csv(self.file_path)
        df.set_index(guess_index_columns(df), inplace=True)
        ds = xarray.Dataset.from_dataframe(df)
        ds = process_xarray_units(ds)
        output_path = self.temp_dir.name / f"{self.file_path.stem}.hdf5"
        ds.to_netcdf(output_path, engine='h5netcdf', invalid_netcdf=True)
        return output_path
        
def guess_index_columns(df : pd.DataFrame) -> list:
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
def extract_name_and_units(label) -> tuple:
    match = re.match(r"(.*?)(?:\s*\((.*?)\))?$", label)
    name = match.group(1).strip() if match else label
    units = match.group(2).strip() if match and match.group(2) else None
    return name, units


def process_xarray_units(ds : xarray.Dataset) -> xarray.Dataset:
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