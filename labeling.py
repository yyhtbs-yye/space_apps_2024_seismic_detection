import os.path as osp
import pandas as pd
import matplotlib.pyplot as plt

from utils import onehot_labeling

# Define the root path, planet, dataset type, metadata filename, and auxiliary data folder
root = 'data'
planet = 'lunar'
dstype = 'training'
meta_filename = 'apollo12_catalog_GradeA_final'
subaux = 'S12_GradeA'

out_folder = "raw_signals_and_labels"


# Construct the path to the metadata CSV file
path = osp.join(root, planet, dstype, 'catalogs', meta_filename) + ".csv"

# Read the metadata CSV file
df = pd.read_csv(path)

# Iterate through each row in the metadata DataFrame
for i, row in df.iterrows():
    filename = row['filename']
    filepath = osp.join(root, planet, dstype, 'data', subaux, filename) + ".csv"

    # Check if the file exists before proceeding
    if osp.exists(filepath):
        # Read the seismic data file
        sdf = pd.read_csv(filepath)

        # Get the time relative from the metadata row
        time_rel = row['time_rel(sec)']

        sdf = onehot_labeling(sdf, 'time_rel(sec)', [time_rel], 'label')

        # Save sdf['time_rel(sec)'] and sdf['label'] as x and y in a new DataFrame
        new_sdf = pd.DataFrame()
        new_sdf["t"] = sdf['time_rel(sec)']
        new_sdf["x"] = sdf['velocity(m/s)']
        new_sdf["y"] = sdf['label']

        # Save the new DataFrame to a CSV file
        new_sdf.to_csv(osp.join(out_folder, filename) + ".csv", index=False)
