from pymap3d import ecef2geodetic

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def transform_ecef_to_lla(x, y, z):

    latitude, longitude, altitude = ecef2geodetic(x, y, z)

    return latitude, longitude, altitude


@transformer
def transform(data, *args, **kwargs):

    for index, row in data.iterrows():
        x = float(row['position_x'])
        y = float(row['position_y'])
        z = float(row['position_z'])

        latitude, longitude, altitude = transform_ecef_to_lla(x, y, z)

        data.at[index, 'latitude'] = latitude
        data.at[index, 'longitude'] = longitude
        data.at[index, 'altitude'] = altitude

    return data[['position_x', 'position_y', 'position_z', 'latitude', 'longitude', 'altitude']]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
