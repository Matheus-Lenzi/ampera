import numpy as np
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def calculate_acceleration(velocity_xyz, accel_xyz):
    
    dot_product = np.dot(velocity_xyz, accel_xyz)
    norm_accel_xyz_square = np.linalg.norm(accel_xyz) ** 2
    acceleration_xyz = (dot_product / norm_accel_xyz_square) * accel_xyz
    acceleration = np.linalg.norm(acceleration_xyz)

    cos_theta = dot_product / (np.linalg.norm(velocity_xyz) * np.linalg.norm(accel_xyz))
    theta = np.arccos(cos_theta)
    
    if theta > np.pi / 2:
        acceleration = -acceleration
    
    return acceleration

@transformer
def transform(data, *args, **kwargs):

    data['speed'] = (data['velocity_x'] ** 2 + data['velocity_y'] ** 2 + data['velocity_z'] ** 2) ** (1/2)

    data['acceleration'] = data.apply(lambda row: calculate_acceleration(
        np.array([row['velocity_x'], row['velocity_y'], row['velocity_z']]),
        np.array([row['accel_x'], row['accel_y'], row['accel_z']])
    ), axis=1)

    data[['speed', 'acceleration']] = data[['speed', 'acceleration']] * 3.6

    return data[['speed', 'acceleration']]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
