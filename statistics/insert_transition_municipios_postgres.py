import psycopg2
import psycopg2.extras

import pprint
import json
import config

def get_data(path_json):

    data = json.load(open(path_json))["features"]

    data = [item['properties'] for item in data ]

    return data

def cal_arranjos():
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

def format_data_estados(data, idprefix=0):
    arranjos = cal_arranjos()

    data_estados = {}

    for item in data:

        estado = str(int(item['featureid']))[0:2]

        if estado not in data_estados:
            data_estados[estado] = {
                
                'classes':{},
                'ano_inicial':str(item['ANO'])[:4],
                'ano_final':str(item['ANO'])[4:],
                'area_total':0.0
            
            }

        for values in item['data']:
            value_pixel = values[0]
            area = values[1]

            if value_pixel not in data_estados[estado]['classes']:
                data_estados[estado]['classes'][value_pixel] = area
            else:
                data_estados[estado]['classes'][value_pixel] += area
            data_estados[estado]['area_total'] += area


    data_result = []
    for estadoid in data_estados:
        for classes in data_estados[estadoid]['classes']:


            value_pixel = classes
            area = data_estados[estadoid]['classes'][classes]

            classe1 = arranjos[value_pixel][0]
            classe2 = arranjos[value_pixel][1]

            ano_inicial = data_estados[estadoid]['ano_inicial']
            ano_final = data_estados[estadoid]['ano_final']

            area_total = data_estados[estadoid]['area_total']



            data_result.append(
                {

                    'territorio':int(estadoid) + idprefix,
                    'ano_inicial':ano_inicial,
                    'ano_final':ano_final,
                    'classe_inicial' : classe1,
                    'classe_final':classe2,
                    'area':area,
                    'porcentagem':round((area/area_total)*100, 4)
                }
            )

    return data_result


def format_data_pais(data, idprefix=0):
    arranjos = cal_arranjos()

    paisid = '10'

    data_pais = {}
 

    for item in data:

        if paisid not in data_pais:

            data_pais = {paisid:{

                'classes':{},
                'ano_inicial':str(item['ANO'])[:4],
                'ano_final':str(item['ANO'])[4:],
                'area_total':0.0


                }}

        for values in item['data']:
            value_pixel = values[0]
            area = values[1]

            if value_pixel not in data_pais[paisid]['classes']:
                data_pais[paisid]['classes'][value_pixel] = area
            else:
                data_pais[paisid]['classes'][value_pixel] += area
            data_pais[paisid]['area_total'] += area


    data_result = []
    for estadoid in data_pais:
        for classes in data_pais[estadoid]['classes']:


            value_pixel = classes
            area = data_pais[estadoid]['classes'][classes]

            classe1 = arranjos[value_pixel][0]
            classe2 = arranjos[value_pixel][1]

            ano_inicial = data_pais[estadoid]['ano_inicial']
            ano_final = data_pais[estadoid]['ano_final']

            area_total = data_pais[estadoid]['area_total']



            data_result.append(
                {

                    'territorio':int(estadoid) + idprefix,
                    'ano_inicial':ano_inicial,
                    'ano_final':ano_final,
                    'classe_inicial' : classe1,
                    'classe_final':classe2,
                    'area':area,
                    'porcentagem':round((area/area_total)*100, 4)
                }
            )

    return data_result

    
def format_data(data, idprefix=0):
    arranjos = cal_arranjos()

    data_result = []

    for item in data:
        area_total = sum([i[1] for i in item['data']])

        territorio = int(item['featureid'])

        ano_inicial = str(item['ANO'])[:4]
        ano_final = str(item['ANO'])[4:]

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
    cur, sqlinsert, datainsert, template=None, page_size=1000
    )

    conn.commit()
    conn.close()
