
import os

def buildvrt(folder_path, biome):
    osCommand = "gdalbuildvrt  " + folder_path + "/" + biome + ".vrt "   + folder_path + "/" + biome + "*"
    os.system(osCommand)

def merge_images(folder_path, biome)
    osCommand = 'gdal_translate -of GTiff -co "COMPRESS=LZW" ' + folder_path + "/" + biome + ".vrt " + folder_path + "/" + biome + ".tif"