import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, data_2, data_3, *args, **kwargs):

    data = pd.concat([data, data_2, data_3], axis=1)
    filepath = './data/output/output.csv'
    data.to_csv(filepath)
