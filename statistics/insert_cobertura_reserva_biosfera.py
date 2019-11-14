import os
import pandas as pd
import psycopg2
import psycopg2.extras
from pprint import pprint
import json
import config
from functools import reduce


def get_all_geojsons_paths(path_folder):
    geojsons_paths = []
    for root, dirs, files in os.walk(path_folder):
        geojsons_paths = geojsons_paths + [
            os.path.join(root, file) for file in files if file.endswith(".geojson")
        ]
    return geojsons_paths


def filter_geojsons_by_cobertura(list_geojsons_path):
    result = []
    for json_path in list_geojsons_path:
        result.append(json_path)
    return result


def get_data(path_json):

    data = json.load(open(path_json))
    data = map(lambda item: item["properties"], data["features"])
    result = []
    for item in data:
        info = {}
        info["year"] = int(item["ANO"])
        info["featureid"] = int(item["featureid"])
        info["themeid"] = int(item["themeid"])
        for v, area in item["data"]:
            if area > 0:
                info[str(v)] = area
        result.append(info)
    df = pd.DataFrame(result)

    df.fillna(0.0, inplace=True)

    return df


def format_data(data, col_territorio="featureid", idprefix=0):
    classes = [str(i) for i in range(0, 34)]

    data = (
        data.groupby([col_territorio, "year"]).sum().reset_index().T.to_dict().values()
    )

    data_result = []
    for item in data:

        area_total = reduce(
            lambda a, b: a + item.get(b, 0.0), classes[1:], item.get("0", 0.0)
        )

        territorio = int(item[col_territorio])

        ano = int(item["year"])
        for value in classes:

            area = item.get(value, 0.0)

            if area <= 0.0:
                continue

            value = "27" if value == "0" else value

            data_result.append(
                {
                    "classe": int(value),
                    "area": area,
                    "ano": str(ano),
                    "territorio": territorio + idprefix,
                    "percentagem": round((area / area_total) * 100, 4),
                }
            )

    return data_result


def insert_postgres(data_postgres):

    conn = psycopg2.connect(
        dbname=config.postgres_db,
        user=config.postgres_user,
        host=config.postgres_host,
        port=config.postgres_port,
        password=config.postgres_password,
    )

    cur = conn.cursor()

    sqlinsert = """INSERT INTO 	estatisticas (territorio, classe, ano, area, percentagem)
                VALUES %s"""

    datainsert = [
        (a["territorio"], a["classe"], a["ano"], a["area"], a["percentagem"])
        for a in data_postgres
    ]

    psycopg2.extras.execute_values(
        cur, sqlinsert, datainsert, template=None, page_size=500
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # path = "/home/dyeden/data/stats_biosfera/RESERVA_BIOSFERA/COBERTURAV1/collection-4.0-cobertura-reserva.biosfera-5-1991-1-.geojson"
    path_folder = "/home/dyeden/data/stats_biosfera/COBERTURAV1"

    paths = get_all_geojsons_paths(path_folder)

    paths = filter_geojsons_by_cobertura(paths)

    for path in paths:
        print(path)
        data = get_data(path)
        data_formatted = format_data(data, col_territorio="themeid", idprefix=80000000)
        insert_postgres(data_formatted)

        # print(len(paths))

        # data = get_data(path)
        # data_formatted = format_data(data, col_territorio="themeid", idprefix=80000000)
        # print(data_formatted)
        # pass
