import insert_transition_postgres
import argparse
from functools import reduce


def send_to_postgres(path_json, idprefix = 0):
    data = insert_transition_postgres.get_data(path_json)
    data_formatted = insert_transition_postgres.format_data(data, idprefix)
    insert_transition_postgres.insert_postgres(data_formatted)

def get_path_json(path_folder, years_pair, filter_layer):
    year1 = years_pair.split('_')[0]
    year2 = years_pair.split('_')[1]
    json_name = insert_transition_postgres.get_transitions_meta(path_folder,
    filter_layer, year1=year1, year2=year2)[0]['json_name']
    return path_folder + "/" + json_name

def biomas(path_folder, transition_years):
    for years_pair in transition_years:
        filter_layer = 'biomas'
        path_json = get_path_json(path_folder, years_pair, filter_layer)
        send_to_postgres(path_json)

def interface():

    parser = argparse.ArgumentParser(description='Export the statistics for the postgres database')


    parser.add_argument('layer', type=str, help='choose the layer', 
                        choices=['biomas', 'car_biomas', 'bacias_nivel_1', 'bacias_nivel_2', 
                        'municipios_estado_pais', 'car_municipios', 'all'])

    parser.add_argument('dir_geojson', type=str,  help='the geojson folder')

    layer = parser.parse_args().layer
    dir_geojson = parser.parse_args().dir_geojson


    transition_years = ["1985_1986", "1986_1987", "1987_1988", "1988_1989", "1989_1990", "1990_1991", "1991_1992", "1992_1993", 
                        "1993_1994", "1994_1995", "1995_1996", "1996_1997", "1997_1998", "1998_1999", "1999_2000", "2000_2001",
                        "2001_2002", "2002_2003", "2003_2004", "2004_2005", "2005_2006", "2006_2007", "2007_2008", "2008_2009", 
                        "2009_2010", "2010_2011", "2011_2012", "2012_2013", "2013_2014", "2014_2015", "2015_2016", "2016_2017",
                        "1985_1990", "1990_1995", "1995_2000", "2000_2005", "2005_2010", "2010_2015", "2015_2017", "1990_2000", 
                        "2000_2010", "2010_2017", "1985_2017", "2008_2017", "2012_2017" ]


    if layer == "biomas":
        biomas(dir_geojson, transition_years)

if __name__ == "__main__":
    interface()