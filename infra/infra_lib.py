import pandas as pd
import os
import osgeo.ogr
import config
import psycopg2
import psycopg2.extras


import json
import os
import pandas as pd
import psycopg2
import psycopg2.extras
from pprint import pprint
import json
import config
from functools import reduce



def get_data_municipios(data_frame):

    data_pandas = data_frame.drop(
        ['UF', 'PAIS'], axis=1)

    data_pandas = data_frame.T.to_dict().values()

    return data_pandas


def get_data_estados(data_frame):

    data_pandas = data_frame.drop(
        ['featureid', 'PAIS'], axis=1).groupby(['UF', 'year','infraid']).sum().reset_index()

    data_pandas = data_pandas.T.to_dict().values()

    return data_pandas


def get_data_pais(data_frame):

    data_pandas = data_frame.drop(
        ['featureid', 'UF'], axis=1).groupby(['PAIS', 'year', 'infraid']).sum().reset_index()

    data_pandas = data_pandas.T.to_dict().values()

    return data_pandas


def format_data(data_pandas, col_territorio='featureid'):
    classes = [str(i) for i in range(0, 34)]

    data_result = []
    for item in data_pandas:

        area_total = reduce(lambda a, b: a + item.get(b, 0.0), classes[1:], item.get('0', 0.0))

        territorio = int(item[col_territorio])

        ano = int(item['year'])
        infraid = int(item['infraid'])
        for value in classes:
            

            area = item.get(value, 0.0)

            if area <= 0.0:
                continue

            
            value = '27' if value == '0' else value


            data_result.append(
                {
                    'classe': int(value),
                    'area': area,
                    'ano': str(ano),
                    'territorio': territorio,
                    'percentagem': round((area/area_total)*100, 4),
                    'infraid':infraid

                })

    return data_result


def insert_postgres(data_postgres):

    conn = psycopg2.connect(dbname=config.postgres_db, user=config.postgres_user, host=config.postgres_host, port=config.postgres_port, password=config.postgres_password)


    cur = conn.cursor()

    sqlinsert = """INSERT INTO 	estatistica_cobertura_infrabuffer (infrabuffer, territorio, classe, ano, area, percentagem)
                VALUES %s"""

    datainsert = [(a['infraid'], a['territorio'], a['classe'], a['ano'], a['area'], a['percentagem'])
                  for a in data_postgres]

    psycopg2.extras.execute_values(

        cur, sqlinsert, datainsert, template=None, page_size=100

    )

    conn.commit()
    conn.close()


def get_data(path_json):
    
    data = json.load(open(path_json))
    data = map(lambda item: item['properties'], data['features'])
    result = []
    for item in data:

        info = {}
        info['year'] = int(item['ANO'])
        info['featureid'] = int(item['featureid'])  
        info['infraid'] = int(item['infraid'])
        if info['featureid'] == 0:
            continue
        for v, area in item['data']:
            if area > 0:
                info[str(v)] = area
        result.append(info)
    df = pd.DataFrame(result)
    df['UF'] = df['featureid'].astype(str).str[0:2].astype(int)
    df['PAIS'] = 10
    df.fillna(0.0, inplace=True)
    return df

def get_info_project(project_name):
    if project_name == 'chaco':
        data = json.load(open('info_chaco.json'))
    if project_name == 'brasil':
        data = json.load(open('info_brasil.json'))
    else:
        raise Exception('this project name doesnt exist')
    return data


def get_infra_levels_info(path_csv):
    df = pd.read_csv(path_csv, sep=",")
    return df


def get_geojsons(path_folder):
    paths = []
    for path, subdirs, files in os.walk(path_folder):
        for name in files:
            if name[-8:] == ".geojson":
                paths.append(os.path.join(path, name))
                
    return paths


def get_shapefiles(path_folder):
    paths = []
    for path, subdirs, files in os.walk(path_folder):
        for name in files:
            if name[-4:] == ".shp":
                paths.append(os.path.join(path, name))
    return paths


def buffer_distance(shp_path):
    shapefile = osgeo.ogr.Open(shp_path)
    layer = shapefile.GetLayer(0)

    field_names = [field.name for field in layer.schema]

    bufdist = None

    if "bufdist" in field_names:
        feature = layer.GetFeature(0)
        bufdist = feature.GetField("bufdist")

    shapefile.Destroy()

    return bufdist


def get_infra_level(shp_path):
    shapefile = osgeo.ogr.Open(shp_path)
    layer = shapefile.GetLayer(0)

    feature = layer.GetFeature(0)
    infra_level = feature.GetField("infra_id")

    shapefile.Destroy()

    return infra_level

def get_wkts(path_shp):
    shapefile = osgeo.ogr.Open(path_shp)    
    layer = shapefile.GetLayer(0)  
    list_wkts = []  
    for i in range(layer.GetFeatureCount()):  
        feature = layer.GetFeature(i)  
        wkt = feature.GetGeometryRef().ExportToWkt()  
        list_wkts.append(wkt)
    shapefile.Destroy()
    return list_wkts


def data_infra_postgres(info):
    data = []
    for item in info:
        path_shp = item['path']
        list_wkts = get_wkts(path_shp) 
        for wkt in list_wkts:
            data.append([item['infra_level'], wkt])
    return data


def data_infra_buffer_postgres(info):
    data = []
    for item in info:
        path_shp = item['path']
        list_wkts = get_wkts(path_shp) 
        for wkt in list_wkts:
            data.append([item['id'], item['buffer_distance'], item['infra_level'], wkt])
    return data


def insert_postgres(datainsert):
    conn = psycopg2.connect(
        dbname=config.postgres_db,
        user=config.postgres_user,
        host=config.postgres_host,
        port=config.postgres_port,
        password=config.postgres_password,
    )

    cur = conn.cursor()

    sqlinsert = """INSERT INTO 	territorios_infra (infra_level, the_geom)
            VALUES %s"""

    template = "(%s, ST_Force2D(ST_GeometryFromText(%s, 4326)))"

    psycopg2.extras.execute_values(
        cur, sqlinsert, datainsert, template=template, page_size=500
    )

    conn.commit()
    conn.close()


def delete_infra_postgres(list_infra_levels):
    conn = psycopg2.connect(
        dbname=config.postgres_db,
        user=config.postgres_user,
        host=config.postgres_host,
        port=config.postgres_port,
        password=config.postgres_password,
    )

    cur = conn.cursor()

    for infra_level in list_infra_levels:

        cur.execute(
            "DELETE FROM territorios_infra WHERE infra_level = %s", (infra_level,)
        )

    conn.commit()
    conn.close()


def delete_infra_buffer_postgres(list_ids):
    conn = psycopg2.connect(
        dbname=config.postgres_db,
        user=config.postgres_user,
        host=config.postgres_host,
        port=config.postgres_port,
        password=config.postgres_password,
    )

    cur = conn.cursor()

    for _id in list_ids:
        cur.execute("DELETE FROM territorios_infrabuffer WHERE id = %s", (_id,))

    conn.commit()
    conn.close()


def insert_postgres_buffer(datainsert):
    conn = psycopg2.connect(
        dbname=config.postgres_db,
        user=config.postgres_user,
        host=config.postgres_host,
        port=config.postgres_port,
        password=config.postgres_password,
    )

    cur = conn.cursor()

    sqlinsert = """INSERT INTO 	territorios_infrabuffer (id, bufdist, infra_level, the_geom)
            VALUES %s"""

    template = "(%s, %s, %s, ST_Force2D(ST_GeometryFromText(%s, 4326)))"

    psycopg2.extras.execute_values(
        cur, sqlinsert, datainsert, template=template, page_size=500
    )

    conn.commit()
    conn.close()

