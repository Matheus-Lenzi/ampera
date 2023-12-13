import pandas as pd
from datetime import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    diff_values = data['timestamp'].diff()
    mask = (diff_values == 0) 
    data.loc[mask, 'timestamp'] = None
    data['timestamp'] = data['timestamp'].interpolate(method='linear')

    data['date_hour'] = data['timestamp'].apply(lambda x: pd.NaT if pd.isna(x) else (pd.Timestamp(datetime.fromtimestamp(x)) if pd.notna(x) else x)) # Convert seconds Timestamp to datetime
    data['date'] = data['date_hour'].dt.strftime('%d/%m/%Y')
    data['hour'] = data['date_hour'].dt.strftime('%H:%M:%S:%f')

    data['timestamp'] = data['timestamp'] * 1000000
    data['timestamp'] = data['timestamp'].round()

    return data[['date_hour', 'date', 'hour', 'timestamp']]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
