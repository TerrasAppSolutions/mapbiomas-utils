import os
import argparse


def get_integration_years():

    years = range(2010, 2018)

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

def get_transition_years():
    transition_years = [ u'1985_1986', u'1986_1987', u'1987_1988', u'1988_1989', u'1989_1990', u'1990_1991',
                         u'1991_1992', u'1992_1993', u'1993_1994', u'1994_1995', u'1995_1996', u'1996_1997', 
                         u'1997_1998', u'1998_1999', u'1999_2000', u'2000_2001', u'2001_2002', u'2002_2003', 
                         u'2003_2004', u'2004_2005', u'2005_2006', u'2006_2007', u'2007_2008', u'2008_2009', 
                         u'2009_2010', u'2010_2011', u'2011_2012', u'2012_2013', u'2013_2014', u'2014_2015', 
                         u'2015_2016', u'2016_2017', u'1985_1990', u'1990_1995', u'1995_2000', u'2000_2005', 
                         u'2005_2010', u'2010_2015', u'2015_2017', u'1990_2000', u'2000_2010', u'2010_2017', 
                         u'1985_2017', u'2008_2017', u'2012_2017', u'1994_2002', u'2002_2010', u'2010_2016']

    return transition_years

def vrt_transition(pathInput, pathOutput):

    transitionYears = get_transition_years()

    bands = range(0, len(get_transition_years()))

    for band in bands:

        pathImageInput = pathInput + '/*.tif'
        pathImageOutput = pathOutput + "/TRANSICAO_" + str(transitionYears[band]) + '.vrt'

        osCommand = 'gdalbuildvrt -b ' + str(band + 1) + " " + \
                     pathImageOutput + " "  + pathImageInput

        print(osCommand)
        os.system(osCommand)


def vrt_rgb(pathInput, pathOutput):

    integrationYears = get_integration_years()

    bands = range(0,33)

    for band in bands:
        year = str(integrationYears[band])
        pathImageInput = pathInput + '/mosaic-rgb-collection3-' + year +  '*.tif'
        pathImageOutput = pathOutput + "/RGB_" + str(integrationYears[band]) + '.vrt'

        osCommand = 'gdalbuildvrt -allow_projection_difference -overwrite ' + \
                     pathImageOutput + " "  + pathImageInput

        print(osCommand)
        os.system(osCommand)



def interface():

    parser = argparse.ArgumentParser(description='Create VRT')

    parser.add_argument('colecao', type=str, default='integracao', help='choose which collection', 
                    choices=['integracao', 'transicao', 'rgb'])

    parser.add_argument('dir_src', type=str,  help='the source folder')

    parser.add_argument('dir_dst', type=str,  help='the destination folder')
    
    colecao = parser.parse_args().colecao
    dir_src = parser.parse_args().dir_src
    dir_dst = parser.parse_args().dir_dst

    if colecao == "integracao":
        vrt_integration(dir_src, dir_dst)

    if colecao == 'transicao':
        vrt_transition(dir_src, dir_dst)

    if colecao == 'rgb':
        vrt_rgb(dir_src, dir_dst)


if __name__ == "__main__":
    interface()

