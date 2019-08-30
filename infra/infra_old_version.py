import os
import pandas as pd
import psycopg2
import psycopg2.extras
from pprint import pprint
import json
import config


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
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' port='5432' password='postgres'")

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
        info['featureid'] = int(item['CD_GEOCMU'])  
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




# path_folder = "/home/dyeden/BASE_DADOS/estatisticas3/gee/data/infra/cobertura/"
path_folder = "/data/estatisticas/3.0/infra_v2/cobertura/"

paths = []
for path, subdirs, files in os.walk(path_folder):
    for name in files:
        if name[-8:] == ".geojson":
            paths.append(os.path.join(path, name))

    


# paths = [path for path in paths if "-5006_" not in path]
# paths = [path for path in paths if "-10006_" not in path]
# paths = [path for path in paths if "-20006_" not in path]
# paths = [path for path in paths if "-5019_" not in path]
# paths = [path for path in paths if "-10019_" not in path]
# paths = [path for path in paths if "-20019_" not in path]



#TODO nao tem na base
# paths = [path for path in paths if "-5057_" not in path]

# paths = [path for path in paths if "-10055_" not in path]

# newpath = []
# for i in ('10055', '10053', '5054','5057', '5056'):

#     newpath = newpath + [path for path in paths if "-" + i + "_" in path]


# paths = newpath

for path_json in paths:
    print path_json
    data = get_data(path_json)

    data_municipios = get_data_municipios(data)
    data_estados = get_data_estados(data)
    data_pais = get_data_pais(data)

    
    data_municipios = format_data(data_municipios, col_territorio='featureid')
    data_estados = format_data(data_estados, col_territorio='UF')
    data_pais = format_data(data_pais, col_territorio='PAIS')

    # print data_municipios[0]
    # print data_estados[0]
    # print data_pais[0]

    try:

        insert_postgres(data_municipios)
        insert_postgres(data_pais)
        insert_postgres(data_estados)

    except:
        print "\n" 
        print "ERROR"          
        print data_pais[0]
        print "\n"


        


# path_json = "/home/dyeden/BASE_DADOS/estatisticas3/gee/data/cobertura_municipios_v2/collection-3-cobertura-municipios-1985_ee_export.geojson"

# get_data(path_json)
