import os
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader


class EarthquakeDataset(Dataset):
    def __init__(self, csv_folder):
        """
        Args:
            csv_folder (string): Path to the folder with CSV files.
        """
        self.csv_folder = csv_folder
        self.csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    def __len__(self):
        return len(self.csv_files)

    def __getitem__(self, idx):
        # Load the csv file as a pandas dataframe
        csv_path = os.path.join(self.csv_folder, self.csv_files[idx])
        df = pd.read_csv(csv_path)
        
        # Get the velocity (x) and label (y) as tensors
        x = torch.tensor(df['velocity(m/s)'].values, dtype=torch.float32)  # x is velocity
        y = torch.tensor(df['label'].values, dtype=torch.float32)  # y is label
        
        return x, y

# Usage Example:
# Assuming all your CSV files are stored in the folder 'data/csv_files/'
csv_folder = 'downsampled_signals_and_sampels/'
dataset = EarthquakeDataset(csv_folder)

# Create a DataLoader to load the data in batches
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# Example of iterating through the dataset
for x, y in dataloader:
    print("Input (x):", x)
    print("Target (y):", y)
    break  # Remove break to see all batches
