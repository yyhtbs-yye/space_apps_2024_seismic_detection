import os.path as osp
import os
import pandas as pd
import numpy as np
from scipy.signal import resample

from dsp import apply_bandpass_filter

from utils import onehot_labeling

from tqdm import tqdm

in_folder = "raw_signals_and_labels"
out_folder = "downsampled_signals_and_sampels"

for filename in tqdm(os.listdir(in_folder)):

    df = pd.read_csv(osp.join(in_folder, filename))

    # Define the filter parameters
    minfreq = 0.5  # Minimum frequency (Hz)
    maxfreq = 1.0  # Maximum frequency (Hz)
    sampling_rate = 10  # Original sample rate (Assumed 10 Hz, adjust accordingly)
    nyquist_rate = sampling_rate / 2  # Nyquist rate

    # Apply bandpass filter to x and y data
    x_filtered = apply_bandpass_filter(df['velocity(m/s)'], minfreq, maxfreq, sampling_rate)

    # Resampling to 2Hz (based on Shannon theory)
    new_sampling_rate = 2  # New sampling rate (at least 2x the highest frequency)

    num_samples = int(len(df) * (new_sampling_rate / sampling_rate))

    # Resample the data
    df_resampled = pd.DataFrame()

    df_resampled['time_rel(sec)'] = np.linspace(df['time_rel(sec)'].min(), df['time_rel(sec)'].max(), num_samples)

    df_resampled['velocity(m/s)'] = resample(x_filtered, num_samples)

    time_value = df['time_rel(sec)'][df.index[df['label']==1]]

    df_resampled = onehot_labeling(df_resampled, 'time_rel(sec)', time_value, 'label')

    # Display the resampled data
    df_resampled.to_csv(osp.join(out_folder, filename), index=False)
