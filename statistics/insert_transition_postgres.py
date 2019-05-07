import os
import pprint
import json
import psycopg2
import psycopg2.extras
import config
from functools import reduce


def get_data(path_json):

    data = json.load(open(path_json))["features"]
    data = [item['properties'] for item in data ]
    for item in data:
        item['year'] = item['ANO']

    return data

def get_arranjos():
    """
     get all mapbiomas classes combination in transition the actual rule is:
     IMAGE1*100 + IMAGE2B
    """
    arranjos = {}
    classes1 = range(35)
    classes2 = range(35)
    arranjos = {}
    for classe1 in classes1:
        for classe2 in classes2:
            arranjos[classe1 * 100 + classe2] = [classe1, classe2]
    return arranjos

def get_json_metadata(json_name):
    
    return {
    "collection_version":json_name.split('-')[1],
    "collection_type":json_name.split('-')[2],
    "layer_name":json_name.split('-')[3],
    "years_pair":json_name.split('-')[4],
    "version":json_name.split('-')[5]
    }

def get_all_geojsons_paths(path_folder):
    geojsons_paths = []
    for root, dirs, files in os.walk(path_folder):
        geojsons_paths = geojsons_paths + [os.path.join(root,file) for file in files if file.endswith(".geojson")]
    return geojsons_paths

def get_transitions_meta(path_folder, filter_layer=None, year1=None, year2=None):
    
    result = []
    for json_path in get_all_geojsons_paths(path_folder):
        json_name = json_path.split('/')[-1]
        meta = get_json_metadata(json_name)
        if meta["collection_type"] != 'transicao':
            continue
        meta['year1'] = meta['years_pair'].split('.')[0]
        meta['year2'] = meta['years_pair'].split('.')[1]
        meta['json_path'] = json_path
        meta['json_name'] = json_name
        result.append(meta)

    result = [meta for meta in result if meta["collection_type"] == "transicao"]

    if filter_layer:
        result = [meta for meta in result if meta["layer_name"] == filter_layer]

    if year1 != None and year2 != None:
        result = [meta for meta in result if meta["year1"] == year1]
        result = [meta for meta in result if meta["year2"] == year2]

    return result

def format_data(data, idprefix=0):
    arranjos = get_arranjos()
    print(arranjos)
    data_result = []

    for item in data:
        area_total = sum([i[1] for i in item['data']])
        territorio = int(item['featureid'])
        ano_inicial = str(item['year'])[:4]
        ano_final = str(item['year'])[4:]

        for values in item['data']:
            value_pixel = values[0]
            area = values[1]

            classe1 = arranjos[value_pixel][0]
            classe2 = arranjos[value_pixel][1]

            classe1 = 27 if classe1 == 0 else classe1
            classe2 = 27 if classe2 == 0 else classe2

            data_result.append({
                'territorio':int(territorio) + idprefix,
                'ano_inicial':ano_inicial,
                'ano_final':ano_final,
                'classe_inicial':classe1,
                'classe_final':classe2,
                'area':area,
                'porcentagem':round((area/area_total)*100, 4)
            })
        
    return data_result


def insert_postgres(data_postgres):

    conn = psycopg2.connect(dbname=config.postgres_db, user=config.postgres_user, host=config.postgres_host, port=config.postgres_port, password=config.postgres_password)


    cur = conn.cursor()

    sqlinsert = """INSERT INTO estatistica_transicoes (territorio, classe_inicial, classe_final, ano_inicial, ano_final, area, porcentagem)
             VALUES %s"""


    datainsert = [[a['territorio'], a['classe_inicial'], a['classe_final'],     
                    a['ano_inicial'], a['ano_final'], a['area'], a['porcentagem']]
                    for a in data_postgres] 
                    
 
    psycopg2.extras.execute_values (
    cur, sqlinsert, datainsert, template=None, page_size=500
    )

    conn.commit()
    conn.close()