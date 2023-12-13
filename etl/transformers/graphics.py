import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, data_3, *args, **kwargs):

    data = pd.concat([data, data_2, data_3], axis=1)

    data['speed_variation'] = data['speed'].diff() / data['date_hour'].diff().dt.total_seconds()

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
