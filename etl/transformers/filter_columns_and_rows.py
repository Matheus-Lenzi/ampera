import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

rules = [
    {
        "target": "yaw",
        "max_value": 180,
        "min_value": -180
    },
    {
        "target": "pitch",
        "max_value": 180,
        "min_value": -180
    },
    {
        "target": "roll",
        "max_value": 180,
        "min_value": -180
    },
    {
        "target": "position_x",
        "max_value": 6400000,
        "min_value": -6400000
    },
    {
        "target": "position_y",
        "max_value": 6400000,
        "min_value": -6400000
    },
    {
        "target": "position_z",
        "max_value": 6400000,
        "min_value": -6400000
    },
    {
        "target": "velocity_x",
        "max_value": 30,
        "min_value": -30
    },
    {
        "target": "velocity_y",
        "max_value": 30,
        "min_value": -30
    },
    {
        "target": "velocity_z",
        "max_value": 30,
        "min_value": -30
    },
    {
        "target": "accel_x",
        "max_value": 30,
        "min_value": -30
    },
    {
        "target": "accel_y",
        "max_value": 30,
        "min_value": -30
    },
    {
        "target": "accel_z",
        "max_value": 30,
        "min_value": -30
    },
    {
        "target": "angular_rate_x",
        "max_value": 3,
        "min_value": -3
    },
    {
        "target": "angular_rate_y",
        "max_value": 3,
        "min_value": -3
    }
]

def clean_out_of_range(dataframe, target, min_value, max_value):
    
    dataframe = dataframe[dataframe[target] > min_value]
    dataframe = dataframe[dataframe[target] < max_value]
    
    return dataframe


@transformer
def transform(data, *args, **kwargs):

    for column in rules:
        data = clean_out_of_range(data, column.get("target"), column.get("min_value"), column.get("max_value"))

    data = data.dropna(axis=1, how='all')

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
