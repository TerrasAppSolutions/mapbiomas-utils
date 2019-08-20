import os
import argparse
import json
from info_lib import get_info_project

def get_integration_years():

    info = get_info_project(project_name)
    info = [item for item in info if item['col'] == '4'][0]
    years = info["years"]

    return years


def vrt_integration(pathInput, pathOutput):

    integrationYears = get_integration_years()

    bands = range(0,len(integrationYears))

    for band in bands:

        pathImageInput = pathInput + '/*.tif'
        pathImageOutput = pathOutput + "/INTEGRACAO_" + str(integrationYears[band]) + '.vrt'

        osCommand = 'gdalbuildvrt -b ' + str(band + 1) + " " + \
                     pathImageOutput + " "  + pathImageInput

        print(osCommand)
        os.system(osCommand)

def get_transition_years(project_name):

    transition_years = get_info_project(project_name)["transition_years"]

    return transition_years

def vrt_transition(pathInput, pathOutput, project_name):

    transitionYears = get_transition_years(project_name)

    bands = range(0, len(transitionYears))

    for band in bands:

        pathImageInput = pathInput + '/*.tif'
        pathImageOutput = pathOutput + "/TRANSICAO_" + str(transitionYears[band]) + '.vrt'

        osCommand = 'gdalbuildvrt -b ' + str(band + 1) + " " + \
                     pathImageOutput + " "  + pathImageInput

        print(osCommand)
        os.system(osCommand)


def vrt_rgb(pathInput, pathOutput):

    integrationYears = get_integration_years()

    bands = range(0,len(integrationYears))

    for band in bands:
        year = str(integrationYears[band])
        pathImageInput = pathInput + '/mosaic-rgb-collection1-' + year +  '*.tif'
        pathImageOutput = pathOutput + "/RGB_" + str(integrationYears[band]) + '.vrt'

        osCommand = 'gdalbuildvrt -allow_projection_difference -overwrite ' + \
                     pathImageOutput + " "  + pathImageInput

        print(osCommand)
        os.system(osCommand)



def interface():

    parser = argparse.ArgumentParser(description='Create VRT')

    parser.add_argument('project', type=str, help='write the project name', choices=['brasil', 'chaco', 'raisg'])

    parser.add_argument('colecao', type=str, default='integracao', help='choose which collection', 
                    choices=['integracao', 'transicao', 'rgb'])

    
    project_name = parser.parse_args().project
    colecao = parser.parse_args().colecao

    info = get_info_project(project_name)
    info = [item for item in info if item['col'] == '4'][0]

    if colecao == "integracao":
        dir_src = info["folders"]["integracao"]
        dir_dst = info["folders"]["integracao_vrt"]
        vrt_integration(dir_src, dir_dst)

    if colecao == 'transicao':
        dir_src = info["folders"]["transicao"]
        dir_dst = info["folders"]["transicao_vrt"]
        vrt_transition(dir_src, dir_dst, project_name)

    if colecao == 'rgb':
        vrt_rgb(dir_src, dir_dst)


if __name__ == "__main__":
    interface()

