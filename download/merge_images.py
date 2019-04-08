
import os
import argparse

def get_list_names_raster():
    return ['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 'PAMPA', 'PANTANAL']

def buildvrt(folder_path, folder_vrt, biome):
    osCommand = "gdalbuildvrt  " + folder_vrt + "/" + biome + ".vrt "   + folder_path + "/" + biome + "*"
    os.system(osCommand)

def merge_images(folder_path, biome):
    osCommand = 'gdal_translate -of GTiff -co "COMPRESS=LZW" ' + folder_path + "/" + biome + ".vrt " + folder_path + "/" + biome + ".tif"
    os.system(osCommand)

def execute(raster_name, folder_path, folder_vrt):

    osCommand = "mkdir -p " + folder_vrt
    os.system(osCommand)

    if raster_name == 'all':
        
        names = get_list_names_raster()

        #execute vrt
        for name in names:
            print('executing vrt', name)
            buildvrt(folder_path, folder_vrt, name)

        #execute merge
        for name in names:
            print('executing merge', name)
            merge_images(folder_vrt, name)

def interface():
    parser = argparse.ArgumentParser(description='Merge the images for download')

    parser.add_argument('name', type=str, help='choose the raster name', 
                        choices=['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 
                        'PAMPA', 'PANTANAL', 'all']) #TODO only 'all' works 

    parser.add_argument('folder_path', type=str,  help='choose the raster folder')

    parser.add_argument('folder_vrt', type=str,  help='choose the vrt folder')

    raster_name = parser.parse_args().name
    folder_vrt = parser.parse_args().folder_vrt
    folder_path = parser.parse_args().folder_path

    execute(raster_name, folder_path, folder_vrt)
    


if __name__ == "__main__":
    interface()