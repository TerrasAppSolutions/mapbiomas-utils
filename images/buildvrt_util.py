import os
import argparse
import json

def get_integration_years():

    years = range(2010, 2018)

    return years

def get_info_project(project_name):
    if project_name == 'chaco':
       data = json.load(open('info_chaco.json')) 
    else:
        raise Exception('this project name doesnt exist')
    return data

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

    parser.add_argument('dir_src', type=str,  help='the source folder')

    parser.add_argument('dir_dst', type=str,  help='the destination folder')
    
    project_name = parser.parse_args().project
    colecao = parser.parse_args().colecao
    dir_src = parser.parse_args().dir_src
    dir_dst = parser.parse_args().dir_dst

    if colecao == "integracao":
        vrt_integration(dir_src, dir_dst)

    if colecao == 'transicao':
        vrt_transition(dir_src, dir_dst, project_name)

    if colecao == 'rgb':
        vrt_rgb(dir_src, dir_dst)


if __name__ == "__main__":
    interface()

