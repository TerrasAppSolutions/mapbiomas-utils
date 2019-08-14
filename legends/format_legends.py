import pandas as pd
import psycopg2
import psycopg2.extras
import config

def format_data(path):
    df = pd.read_csv(path, sep=",")
    print(df.head())

def format_legends(path):
    df = pd.read_csv(path, sep=",")
    df.dropna(inplace=True, subset=['id', 'parent', 'cor'])

    data = []
    for item in df.T.to_dict().values():
        data.append({
            "nivel":None,
            "rgb":eval(item['RGB']),
            "classe":item['Legend'], 
            "cor":item['COR'],
            "parente":item['Parent'],
            "ref":item['Ref'],
            "versao":1,
            "valor":int(item['COD']),
            "valor_l1":None,
            "valor_l2":None,
            "valor_l3":int(item['COD']),
            "ativo":bool(item["Active"])
        })  

    for item in data:         
        if item['parente'] == 0:
            item['valor_l2'] = item['valor_l3']        
            item['valor_l1'] = item['valor_l3']
        if item['nivel'] == 3:
            item['valor_l2'] = item['parente']
            item['valor_l1'] = df.loc[df['COD']== item['valor_l2'], 'Parent'].to_list()[0]
        if item['nivel'] == 2:
            item['valor_l1'] = item['parente']
            item['valor_l2'] = item['valor_l3']
    return data

def upload_to_postgres(data):
    conn = psycopg2.connect(database=config.postgres_db, 
    user=config.postgres_user, 
    password=config.postgres_password,
    host=config.postgres_host,
    port=config.postgres_port
    )

    cur = conn.cursor()

    sqlinsert = """INSERT INTO classes (classe,cor,parente,ref,versao,valor,valor_l1,valor_l2,valor_l3,ativo)
                VALUES %s"""

    datainsert = [(a['classe'], a['cor'], a['parente'], a['ref'], a['versao'], a['valor'], a['valor_l1'], a['valor_l2'], a['valor_l3'], a['ativo'])
                for a in data]

    psycopg2.extras.execute_values(

        cur, sqlinsert, datainsert, template=None, page_size=100

    )

    conn.commit()
    conn.close()

format_data("./data/legenda_brasil_col4_20190814.csv")


# data = format_data("./data/legenda_brasil_col4_20190814.csv")
# import pprint
# pprint.pprint(data)
# upload_to_postgres(data)

