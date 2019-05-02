
import os
import argparse

def get_list_names_raster():
    return ['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 'PAMPA', 'PANTANAL']

def buildvrt(folder_path, folder_vrt, biome):
    
    osCommand = "gdalbuildvrt  " + folder_vrt + "/" + biome + ".vrt "   + folder_path + "/" + biome + "*"
    os.system(osCommand)

def add_colors_legend(folder_path, biome):

def merge_images(folder_path, biome):
    #TODO change gdal translate example: gdal_translate -of GTiff -a_nodata 0 -co "TILED=YES" -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co BIGTIFF=YES -co COMPRESS=LZW CERRADO.vrt CERRADO2.tif
    osCommand = 'gdal_translate -of GTiff -a_nodata 0 -co BIGTIFF=YES -co "COMPRESS=LZW" ' + folder_path + "/" + biome + ".vrt " + folder_path + "/" + biome + ".tif"
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

    else:
        print('executing vrt', raster_name)
        buildvrt(folder_path, folder_vrt, raster_name)
        print('executing merge', raster_name)
        #TODO add script that will create legend and colors
        merge_images(folder_vrt, raster_name)


def interface():
    parser = argparse.ArgumentParser(description='Merge the images for download')

    parser.add_argument('name', type=str, help='choose the raster name', 
                        choices=['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 
                        'PAMPA', 'PANTANAL', 'all']) 

    parser.add_argument('folder_path', type=str,  help='choose the raster folder')

    parser.add_argument('folder_vrt', type=str,  help='choose the vrt folder')

    raster_name = parser.parse_args().name
    folder_vrt = parser.parse_args().folder_vrt
    folder_path = parser.parse_args().folder_path

    execute(raster_name, folder_path, folder_vrt)
    


if __name__ == "__main__":
    interface()