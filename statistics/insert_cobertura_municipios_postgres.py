import pandas as pd
import psycopg2
import psycopg2.extras
from pprint import pprint
import json
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
            if area > 0:
                info[str(v)] = area
        result.append(info)
    df = pd.DataFrame(result)

    df.fillna(0.0, inplace=True)

    df['UF'] = df['featureid'].astype(str).str[0:2].astype(int)
    df['PAIS'] = 10
    return df

def get_data_municipios(data_frame):

    data_pandas = data_frame.drop(
        ['UF', 'PAIS'], axis=1)

    data_pandas = data_frame.T.to_dict().values()

    return data_pandas


def get_data_estados(data_frame):

    data_pandas = data_frame.drop(
        ['featureid', 'PAIS'], axis=1).groupby(['UF', 'year']).sum().reset_index()

    data_pandas = data_pandas.T.to_dict().values()

    return data_pandas


def get_data_pais(data_frame):

    data_pandas = data_frame.drop(
        ['featureid', 'UF'], axis=1).groupby(['PAIS', 'year']).sum().reset_index()

    data_pandas = data_pandas.T.to_dict().values()

    return data_pandas


def format_data(data_pandas, col_territorio='featureid', idprefix=0):
    classes = [str(i) for i in range(0, 34)]

    data_result = []
    for item in data_pandas:

        area_total = reduce(lambda a, b: a + item.get(b, 0.0), classes[1:], item.get('0', 0.0))

        territorio = int(item[col_territorio])

        ano = int(item['year'])
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
                    'territorio': territorio + idprefix,
                    'percentagem': round((area/area_total)*100, 4)

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
