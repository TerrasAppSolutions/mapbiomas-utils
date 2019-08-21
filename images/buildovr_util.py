import os
import re
import argparse
import json
from info_lib import get_info_project

def ovr_integracao(path_input, part, info_project):


    year1 = info_project["ovr_integracao"][part][0]
    year2 = info_project["ovr_integracao"][part][1]

    years = [str(year) for year in range(year1, year2)]

    files = [path_input + "/" + f for f in os.listdir(path_input) if f.endswith(".vrt")]

    for vrt in files:
        process_start = False
        for year in years:            
            if year in vrt:
                process_start = True

        os_command = "gdaladdo -r mode --config COMPRESS_OVERVIEW PACKBITS --config BIGTIFF_OVERVIEW YES  --config GDAL_CACHEMAX 1000 " + vrt + " 2 4 8 16"

        if process_start:
            print(os_command)
            os.system(os_command)

def ovr_transicao(pathInput, part, info_project):

    transition_years = info_project['ovr_transicao'][part]

    files = [pathInput + "/" + f for f in os.listdir(pathInput) if f.endswith(".vrt") ]
    for vrt in files:
        process_start = False
        for years in transition_years:
            if years in vrt:
                process_start = True

        if process_start:
            osCommand = "gdaladdo -r mode --config COMPRESS_OVERVIEW PACKBITS --config BIGTIFF_OVERVIEW YES  --config GDAL_CACHEMAX 1000 " + vrt + " 2 4 8 16"
            print(osCommand)
            os.system(osCommand)

def ovr_rgb(pathInput, part):

    files = [pathInput + "/" + f for f in os.listdir(pathInput) if f.endswith(".vrt")]

    for vrt in files:
        osCommand = "gdaladdo -r average --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC YCBCR --config BIGTIFF YES --config GDAL_CACHEMAX 1000 " + vrt + " 2 4 8 16"
        print(osCommand)
        os.system(osCommand)


def interface():

    parser = argparse.ArgumentParser(description='Create OVR (Overview) files')

    parser.add_argument('project', type=str, help='write the project name', choices=['brasil', 'chaco', 'raisg'])

    parser.add_argument('colecao', type=str, default='integracao', help='choose which collection', 
                    choices=['integracao', 'transicao', 'rgb'])

    parser.add_argument('part', type=str, default='all', help='which part do you want to start', 
                        choices=['1','2','3','4', 'all'])

    
    project = parser.parse_args().project
    colecao = parser.parse_args().colecao
    part = parser.parse_args().part

    info_project = get_info_project(project)
    info = [item for item in info_project if item['col'] == '4'][0]

    if colecao == "integracao":
        path_input = info["folders"]["integracao_vrt"]
        ovr_integracao(path_input, str(part), info)

    if colecao == "transicao":
        path_input = info["folders"]["transicao_vrt"]
        ovr_transicao(path_input, str(part), info)

    if colecao == "rgb":
        ovr_rgb(path_input, str(part))

if __name__ == "__main__":
    interface()



