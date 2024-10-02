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
    output_filepath = osp.join(out_folder, filename) + ".csv"

    # Check if the file exists before proceeding
    if osp.exists(filepath):

        # Check if the output file already exists
        if osp.exists(output_filepath):
            # If the output file exists, load the existing dataframe
            sdf = pd.read_csv(output_filepath)
        else: # Read the seismic data file
            sdf = pd.read_csv(filepath)
            sdf = sdf[['time_rel(sec)', 'velocity(m/s)']]
            sdf['label'] = 0

        # Get the time relative from the metadata row
        time_rel = row['time_rel(sec)']

        sdf = onehot_labeling(sdf, 'time_rel(sec)', [time_rel], 'label')

        # Save the new DataFrame to a CSV file
        sdf.to_csv(output_filepath, index=False)
