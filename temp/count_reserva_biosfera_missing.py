import os


def get_all_geojsons_paths(path_folder):
    geojsons_paths = []
    for root, dirs, files in os.walk(path_folder):
        geojsons_paths = geojsons_paths + [
            os.path.join(root, file) for file in files if file.endswith(".geojson")
        ]
    return geojsons_paths


if __name__ == "__main__":
    themes = ["1", "2", "3", "4", "5", "6", "7", "8"]

    years = range(1985, 2019)

    path_folder = "/home/dyeden/data/stats_biosfera/COBERTURAV1"

    paths = get_all_geojsons_paths(path_folder)

    print(len(paths))

    # theme_missing = {
    #     "1": [],
    #     "2": [],
    #     "3": [],
    #     "4": [],
    #     "5": [],
    #     "6": [],
    #     "7": [],
    #     "8": [],
    # }

    # ex = "/home/dyeden/data/stats_biosfera/RESERVA_BIOSFERA/COBERTURAV1/collection-4.0-cobertura-reserva.biosfera-{0}-{1}-1-.geojson"

    # for year in years:
    #     for theme_id in themes:
    #         # print(theme_id)
    #         path_geojson = ex.format(theme_id, year)
    #         path_filtered = [path for path in paths if path == path_geojson]
    #         if len(path_filtered) == 0:
    #             print(path_geojson)
    #     #     break
    #     # break
    # print(len(paths))
    # print(len(years))
    # print(paths)
