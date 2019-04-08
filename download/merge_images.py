
import os
import argparse

def get_list_names_raster():
    return ['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 'PAMPA', 'PANTANAL']

def buildvrt(folder_path, biome):
    osCommand = "gdalbuildvrt  " + folder_path + "/" + biome + ".vrt "   + folder_path + "/" + biome + "*"
    os.system(osCommand)

def merge_images(folder_path, biome):
    osCommand = 'gdal_translate -of GTiff -co "COMPRESS=LZW" ' + folder_path + "/" + biome + ".vrt " + folder_path + "/" + biome + ".tif"
    os.system(osCommand)

def execute(bioma, folder_vrt):

    osCommand = "mkdir -p " + folder_vrt
    os.system(osCommand)

    if bioma == 'all':
        
        names = get_list_names_raster()

        #execute vrt
        for name in names:
            print('executing vrt', name)
            buildvrt(folder_vrt, name)

        #execute merge
        for name in names:
            print('executing merge', name)
            merge_images(folder_vrt, name)

def interface():
    parser = argparse.ArgumentParser(description='Merge the images for download')

    parser.add_argument('name', type=str, help='choose the raster name', 
                        choices=['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 
                        'PAMPA', 'PANTANAL', 'all']) #TODO only 'all' works 

    parser.add_argument('folder_vrt', type=str,  help='choose the vrt folder')

    raster_name = parser.parse_args().name
    

