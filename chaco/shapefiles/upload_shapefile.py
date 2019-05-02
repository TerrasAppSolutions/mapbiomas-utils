#shp2pgsql -I -s 2263 /home/dyeden/Documents/chaco/chaco-v2/paises/paises.shp DATATABLE | psql -U DATABASE_USER -d DATABASE_NAME
from config import postgres_db
from config import postgres_host
from config import postgres_password
from config import postgres_user
from config import postgres_port
import os
import argparse
import psycopg2

def ingest_postgres(path_shp, table_name):
    passCommand = "export PGPASSWORD=" + postgres_password + ";"
    shp2pgsqlCommand = "shp2pgsql -I -s 4326 " + path_shp + " " + table_name
    psqlCommand =  "psql -U " + postgres_user + " -d " + postgres_db + " -h " + postgres_host

    osCommand = passCommand + " " + shp2pgsqlCommand + " | "+ psqlCommand

    os.system(osCommand)

    # conn = psycopg2.connect(dbname=postgres_db, user=postgres_user, host=postgres_host, port=postgres_port, password=postgres_password)

    # cur = conn.cursor()

    # sql = '''INSERT INTO territorios (id, descricao, categoria, the_geom)
    #         SELECT featureid, name, categoria, geom
    #         FROM "''' + table_name + '"'

    # cur.execute(sql)

    # conn.commit()

    # sql = 'DROP TABLE "' + table_name + '";'

    # cur.execute(sql)

    # conn.commit()
    # conn.close()



def interface():
    parser = argparse.ArgumentParser(description='Import Shapefiles in Postgres/Postgis')    
    parser.add_argument('path_shp', type=str,  help='the shapefile path')
    parser.add_argument('table_name', type=str,  help='the table name in postgres')
    

    ingest_postgres(parser.parse_args().path_shp, parser.parse_args().table_name)
if __name__ == "__main__":
    interface()
