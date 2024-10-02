import os.path as osp
import pandas as pd
import matplotlib.pyplot as plt

class SeismicDataSet():
    def __init__(self, root, planet, dstype, meta_filename, aux) -> None:

        path = osp.join(root, planet, dstype, 'catalogs', meta_filename) + ".csv"

        df = pd.read_csv(path)

        for i, row in df.iterrows():
            filename = row['filename']
            filepath = osp.join(root, planet, dstype, 'data', aux, filename) + ".csv"

            if osp.exists(filepath):

                sdf = pd.read_csv(filepath)

                time_rel = row['time_rel(sec)']

                sdf['label'] = 0

                closest_idx = (sdf['time_rel(sec)'] - time_rel).abs().idxmin()

                closest_time_rel = sdf.loc[closest_idx]['time_rel(sec)']

                if time_rel >= closest_time_rel:
                    sdf.loc[closest_idx, 'label'] = 1
                else:
                    sdf.loc[closest_idx - 1, 'label'] = 1

                # save sdf['time_rel(sec)'] and sdf['label'] as x, y

                new_sdf = pd.DataFrame()
                new_sdf["t"] = sdf['time_rel(sec)']
                new_sdf["x"] = sdf['velocity(m/s)']
                new_sdf["y"] = sdf['label']
                new_sdf.to_csv(filename + ".csv", index=False)

ds = SeismicDataSet('data', 'lunar', 'training', 'apollo12_catalog_GradeA_final', 'S12_GradeA')