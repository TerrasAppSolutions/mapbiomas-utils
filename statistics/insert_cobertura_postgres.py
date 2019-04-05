import os
import pprint
import json
import psycopg2
import psycopg2.extras
import config
from functools import reduce

def get_data(path_json):

    data = json.load(open(path_json))
    data = map(lambda item: item['properties'], data['features'])
    result = []
    for item in data:
        if int(item['featureid']) == 0:
            continue
        info = {}
        info['year'] = int(item['ANO'])
        info['featureid'] = int(item['featureid'])
        for v, area in item['data']:
            if area >= 0:
                info[str(v)] = area
        result.append(info)
    return result

def get_json_metadata(json_name):
    
    return {
    "collection_version":json_name.split('-')[1],
    "collection_type":json_name.split('-')[2],
    "layer_name":json_name.split('-')[3],
    "year":json_name.split('-')[4],
    "version":json_name.split('-')[5]
    }

def get_all_geojsons_paths(path_folder):
    geojsons_paths = []
    for root, dirs, files in os.walk(path_folder):
        geojsons_paths = geojsons_paths + [os.path.join(root,file) for file in files if file.endswith(".geojson")]
    return geojsons_paths

def get_cobertura_meta(path_folder, filter_layer=None, year = None):
    result = []
    for json_path in get_all_geojsons_paths(path_folder):
        json_name = json_path.split('/')[-1]
        meta = get_json_metadata(json_name)
        if meta["collection_type"] != 'cobertura':
            continue
        meta['json_path'] = json_path
        meta['json_name'] = json_name
        result.append(meta)

    result = [meta for meta in result if meta["collection_type"] == "cobertura"]

    if filter_layer:
        result = [meta for meta in result if meta["layer_name"] == filter_layer]

    if year:
        result = [meta for meta in result if meta["year"] == year]

    return result


def format_data(data, idprefix=0):
    
    classes = [str(i) for i in range(0, 34)]

    data_result = []
    for item in data:

        area_total = reduce(lambda a, b: a + item.get(b, 0.0), classes[1:], item.get('0', 0.0))

        territorio = int(item['featureid'])

        ano = int(item['year'])
        for value in classes:

            area = item.get(value, 0.0)

            if area <= 0.0: 
                continue

            value = '27' if value == '0' else value


            data_result.append(
                {
                'classe':int(value),
                'area':area,
                'ano':str(ano),   
                'territorio':territorio + idprefix,
                'percentagem':round((area/area_total)*100, 4)      

                })

    return data_result

def insert_postgres(data_postgres):

    conn = psycopg2.connect(dbname=config.postgres_db, user=config.postgres_user, host=config.postgres_host, port=config.postgres_port, password=config.postgres_password)

    cur = conn.cursor()

    sqlinsert = """INSERT INTO 	estatisticas (territorio, classe, ano, area, percentagem)
                VALUES %s"""

    datainsert = [(a['territorio'], a['classe'], a['ano'], a['area'], a['percentagem'])
                    for a in data_postgres] 


    psycopg2.extras.execute_values (

        cur, sqlinsert, datainsert, template=None, page_size=100
    
    )

    conn.commit()
    conn.close()


