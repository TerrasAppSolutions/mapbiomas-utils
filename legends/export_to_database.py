import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
import config
import legend_lib


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
    data = legend_lib.adjust_data(path_csv, versao)
    update_db_postgres(data)

if __name__ == "__main__":
    path_csv = "./data/legenda_brasil_col4_20190814.csv"
    versao = 4
    start(path_csv, versao)

