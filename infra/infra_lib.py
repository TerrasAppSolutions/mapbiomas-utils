import pandas  as pd
import os

def get_infra_levels_info(path_csv):
    df = pd.read_csv(path_csv, sep=",")
    return df


def get_geojsons(path_folder):
    paths = []
    for path, subdirs, files in os.walk(path_folder):
        for name in files:
            if name[-8:] == ".geojson":
                paths.append(os.path.join(path, name))
                
    