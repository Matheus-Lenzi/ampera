import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_file(*args, **kwargs):

    filepath = 'ecef.csv'
    
    dataframe = pd.read_csv(filepath, header=None)
    dataframe = dataframe.rename(columns={
        0: 'yaw',
        1: 'pitch',
        2: 'roll', 
        3: 'position_x', 
        4: 'position_y', 
        5: 'position_z', 
        6: 'velocity_x', 
        7: 'velocity_y', 
        8: 'velocity_z', 
        9: 'accel_x', 
        10: 'accel_y', 
        11: 'accel_z', 
        12: 'angular_rate_x', 
        13: 'angular_rate_y', 
        14: 'timestamp'
    })

    for column in dataframe.columns:
        dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')

    dataframe = dataframe.dropna(subset=[
        'yaw',
        'pitch',
        'roll', 
        'position_x', 
        'position_y', 
        'position_z', 
        'velocity_x', 
        'velocity_y', 
        'velocity_z', 
        'accel_x', 
        'accel_y', 
        'accel_z', 
        'angular_rate_x', 
        'angular_rate_y', 
        'timestamp'
    ])
    
    dataframe = dataframe.astype(float)

    return dataframe


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
