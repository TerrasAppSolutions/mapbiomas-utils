import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
import config


def add_nivel(df):
    """
        The function should add a column showing 
        a number of the level of hierarchy
    """

    def get_next_level(parent, nivel):
        if parent == 0:
            return nivel
        
        parent_level = df.loc[df['id']==parent,'nivel'].values[0]
        
        next_level = None        
        if parent_level:
            next_level = parent_level + 1
        return next_level


    df['nivel'] = None

    df.loc[df.parent == 0, 'nivel'] = 1
    df['nivel'] = df.apply(lambda x: get_next_level(x['parent'], x['nivel']), axis=1)
    df['nivel'] = df.apply(lambda x: get_next_level(x['parent'], x['nivel']), axis=1)
    df['nivel'] = df['nivel'].astype(int)


def add_valor(df):

    def get_valor_l1_for_l3(x):
        r = df['parent'].loc[(df['id'] == x['valor_l2']) & (df['nivel'] == 2)].values
        r = r[0] if r else None
        return r


    df['valor'] = None
    df['valor_l1'] = None
    df['valor_l2'] = None
    df['valor_l3'] = None

    df['valor'] = df['id']


    #level 1
    df['valor_l1'] = df['id'].where(df['nivel'] == 1, df['valor_l1'])
    df['valor_l2'] = df['id'].where(df['nivel'] == 1, df['valor_l2'])
    df['valor_l3'] = df['id'].where(df['nivel'] == 1, df['valor_l3'])

    
    #level 2
    df['valor_l1'] = df['parent'].where(df['nivel'] == 2, df['valor_l1'])
    df['valor_l2'] = df['id'].where(df['nivel'] == 2, df['valor_l2'])
    df['valor_l3'] = df['id'].where(df['nivel'] == 2, df['valor_l3'])

    #level 3    
    f = lambda x: df['parent'].loc[(df['valor_l2'] == x['valor_l2']) & (df['nivel'] == 2)]
    
    df['valor_l2'] = df['parent'].where(df['nivel'] == 3, df['valor_l2'])
    df['valor_l1'] = np.where(df['nivel'] == 3, df.apply(get_valor_l1_for_l3, axis=1), df['valor_l1'])
    df['valor_l3'] = df['id'].where(df['nivel'] == 3, df['valor_l3'])

def rename_col(df):
    df.rename(columns={"parent": "parente"}, inplace=True)

def adjust_data(path, versao):
    df = pd.read_csv(path, sep=",")
    df.dropna(inplace=True, subset=['id', 'parent', 'cor'])

    df['versao'] = versao

    df['ativo'] = df['ativo'].apply(lambda x: bool(x))

    add_nivel(df)  

    add_valor(df)

    rename_col(df)

    return list(df.T.to_dict().values())

def insert_db_postgres(data):
    conn = psycopg2.connect(database=config.postgres_db, 
    user=config.postgres_user, 
    password=config.postgres_password,
    host=config.postgres_host,
    port=config.postgres_port
    )

    cur = conn.cursor(data)

    sqlinsert = """INSERT INTO classes (classe,cor,parente,ref,versao,valor,valor_l1,valor_l2,valor_l3,ativo)
                VALUES %s"""

    datainsert = [(a['classe'], a['cor'], a['parente'], a['ref'], a['versao'], a['valor'], a['valor_l1'], a['valor_l2'], a['valor_l3'], a['ativo'])
                for a in data]

    psycopg2.extras.execute_values(

        cur, sqlinsert, datainsert, template=None, page_size=100

    )

    conn.commit()
    conn.close()


def update_db_postgres(data):
    conn = psycopg2.connect(database=config.postgres_db, 
    user=config.postgres_user, 
    password=config.postgres_password,
    host=config.postgres_host,
    port=config.postgres_port
    )

    cur = conn.cursor()

    for a in data:
        sqlupdate = """UPDATE classes
                    SET classe = %s,
                        cor = %s,
                        parente = %s,
                        ref = %s,
                        versao = %s,
                        valor_l1 = %s,
                        valor_l2 = %s,
                        valor_l3 = %s,
                        ativo = %s
                    WHERE valor = %s"""

                    

        cur.execute(sqlupdate,
      (a['classe'], a['cor'], a['parente'], a['ref'], a['versao'], a['valor_l1'], a['valor_l2'], a['valor_l3'], a['ativo'], a['valor']))



    conn.commit()
    conn.close()

def start(path_csv, versao):
    data = adjust_data(path_csv, versao)
    update_db_postgres(data)

if __name__ == "__main__":
    path_csv = "./data/legenda_brasil_col4_20190814.csv"
    versao = 4
    start(path_csv, versao)

