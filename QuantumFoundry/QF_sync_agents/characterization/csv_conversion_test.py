import pandas as pd


import pandas as pd

def guess_index_columns(df):
    """
    Guesses the index columns of a pandas DataFrame by considering columns with
    unique values less than or equal to half the number of total rows.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to analyze.
        
    Returns:
        list: A list of column names that are likely to be index columns.
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





file = '/Users/atosato/Downloads/bluewhale1728488315392/2024-08-26 W4_Al_resonators4_B002019D02/2024-08-26 W4_Al_resonators4_B002019D02-run1-oldprotocol/HighPowerSweep_B002019D02_2.csv'
# file = 'QuantumFoundry/tests/characterization_group/data/Project_A/SUB123/1698762600.0_Type1/measurement.csv'
df = pd.read_csv(file)
# df.set_index(df.columns[0], inplace=True)
# print(df)


# df = pd.DataFrame({
#     # 'col1': [1, 2, 3, 4, 5, 3],
#     'col1': [1, 2, 3, 1,2,3],
#     'col2': [5, 5, 5, 6, 6, 6],
#     # 'col2': [5,6,7,8,9,10],
#     'col3': ['A', 'B', 'C', 'D', 'E', 'A']
# })

index_columns = guess_index_columns(df)
print("Guessed index columns:", index_columns)

print(df.duplicated(subset=df.columns[:1]))