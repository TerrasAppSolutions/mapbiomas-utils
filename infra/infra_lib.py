import pandas  as pd

def get_infra_levels_info(path_csv):
    df = pd.read_csv(path_csv, sep=",")
    return df