import pandas as pd
import os
import osgeo.ogr
import config
import psycopg2
import psycopg2.extras


def get_infra_levels_info(path_csv):
    df = pd.read_csv(path_csv, sep=",")
    return df


def get_geojsons(path_folder):
    paths = []
    for path, subdirs, files in os.walk(path_folder):
        for name in files:
            if name[-8:] == ".geojson":
                paths.append(os.path.join(path, name))


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

