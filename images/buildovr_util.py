import os
import re
import argparse
import json

def get_info_project(project_name):
    if project_name == 'chaco':
       data = json.load(open('info_chaco.json')) 
    else:
        raise Exception('this project name doesnt exist')
    return data

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

        os_command = "gdaladdo -r mode --config COMPRESS_OVERVIEW PACKBITS --config GDAL_CACHEMAX 2000 " + vrt + " 2 4 8 16"

        if process_start:
            print(os_command)
            os.system(os_command)

def ovr_transicao(pathInput, part):

    if part == 'all':
        transition_years = [ u'1985_1986', u'1986_1987', u'1987_1988', u'1988_1989', u'1989_1990', u'1990_1991',
                            u'1991_1992', u'1992_1993', u'1993_1994', u'1994_1995', u'1995_1996', u'1996_1997', 
                            u'1997_1998', u'1998_1999', u'1999_2000', u'2000_2001', u'2001_2002', u'2002_2003', 
                            u'2003_2004', u'2004_2005', u'2005_2006', u'2006_2007', u'2007_2008', u'2008_2009',
                            u'2009_2010', u'2010_2011', u'2011_2012', u'2012_2013', u'2013_2014', u'2014_2015', 
                            u'2015_2016', u'2016_2017', u'1985_1990', u'1990_1995', u'1995_2000', u'2000_2005', 
                            u'2005_2010', u'2010_2015', u'2015_2017', u'1990_2000', u'2000_2010', u'2010_2017', 
                            u'1985_2017', u'2008_2017', u'2012_2017', u'1994_2002', u'2002_2010', u'2010_2016']

    if part == '1':
        transition_years = [ u'1985_1986', u'1986_1987', u'1987_1988', u'1988_1989', u'1989_1990', u'1990_1991',
                            u'1991_1992', u'1992_1993', u'1993_1994', u'1994_1995', u'1995_1996', u'1996_1997']

    if part == '2':
        transition_years = [ u'1997_1998', u'1998_1999', u'1999_2000', u'2000_2001', u'2001_2002', u'2002_2003', 
                            u'2003_2004', u'2004_2005', u'2005_2006', u'2006_2007', u'2007_2008', u'2008_2009']

    if part == '3':
        transition_years = [u'2009_2010', u'2010_2011', u'2011_2012', u'2012_2013', u'2013_2014', u'2014_2015', 
                            u'2015_2016', u'2016_2017', u'1985_1990', u'1990_1995', u'1995_2000', u'2000_2005']

    if part == '4':
        transition_years = [u'2005_2010', u'2010_2015', u'2015_2017', u'1990_2000', u'2000_2010', u'2010_2017', 
                            u'1985_2017', u'2008_2017', u'2012_2017', u'1994_2002', u'2002_2010', u'2010_2016']


    files = [pathInput + "/" + f for f in os.listdir(pathInput) if f.endswith(".vrt") ]
    for vrt in files:

        process_start = False

        for years in transition_years:

            if years in vrt:

                process_start = True

        if process_start:
            osCommand = "gdaladdo -r mode --config COMPRESS_OVERVIEW LZW --config GDAL_CACHEMAX 4000 " + vrt + " 2 4 8 16"
            print(osCommand)
            os.system(osCommand)



def ovr_rgb(pathInput, part):

    files = [pathInput + "/" + f for f in os.listdir(pathInput) if f.endswith(".vrt")]


    for vrt in files:
        osCommand = "gdaladdo -r average --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC YCBCR --config BIGTIFF YES --config GDAL_CACHEMAX 6000 " + vrt + " 2 4 8 16"
        print(osCommand)
        os.system(osCommand)


def interface():

    parser = argparse.ArgumentParser(description='Create OVR (Overview) files')

    parser.add_argument('project', type=str, help='write the project name', choices=['brasil', 'chaco', 'raisg'])

    parser.add_argument('colecao', type=str, default='integracao', help='choose which collection', 
                    choices=['integracao', 'transicao', 'rgb'])

    parser.add_argument('dir_src', type=str,  help='the vrt folder')

    parser.add_argument('part', type=str, default='all', help='which part do you want to start', 
                        choices=['1','2','3','4', 'all'])

    
    project = parser.parse_args().project
    colecao = parser.parse_args().colecao
    path_input = parser.parse_args().dir_src
    part = parser.parse_args().part

    info_project = get_info_project(project)

    if colecao == "integracao":
        ovr_integracao(path_input, str(part), info_project)

    if colecao == "transicao":
        ovr_transicao(path_input, str(part))

    if colecao == "rgb":
        ovr_rgb(path_input, str(part))

if __name__ == "__main__":
    interface()



