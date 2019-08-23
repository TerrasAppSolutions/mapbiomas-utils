import infra_lib

def start():
    path_csv = "./infrastructure_levels.csv"
    df_levels = infra_lib.get_infra_levels_info(path_csv)
    print(df_levels.head())

start()