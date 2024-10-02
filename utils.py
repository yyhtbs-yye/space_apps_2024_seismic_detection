import pandas as pd

def onehot_labeling(df, col_name, values, label_name):

    if label_name not in df.columns:
        df[label_name] = 0

    series = df[col_name]

    for value in values:
        # Find the index of the closest time_rel in the seismic data
        closest_idx = (series - value).abs().idxmin()

        # Get the time_rel value of the closest row
        closest_val = df.loc[closest_idx][col_name]

        # Set the label for the closest time
        if value >= closest_val:
            df.loc[closest_idx, label_name] = 1
        else:
            df.loc[closest_idx - 1, label_name] = 1

    return df