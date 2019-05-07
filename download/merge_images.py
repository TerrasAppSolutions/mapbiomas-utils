
import os
import argparse
import pandas

def get_list_names_raster():
    return ['AMAZONIA', 'CAATINGA', 'CERRADO', 'MATAATLANTICA', 'PAMPA', 'PANTANAL']

def buildvrt(folder_path, folder_vrt, biome):
    
    osCommand = "gdalbuildvrt  " + folder_vrt + "/" + biome + ".vrt "   + folder_path + "/*" + biome + "*.tif"
    os.system(osCommand)

def hex_to_rgb(hex):
    r = str(int(hex[1:3],16))
    g = str(int(hex[3:5],16))
    b = str(int(hex[5:7],16))
    
    return tuple([r,g,b])

def process_csv(csv_file):
    categories = "<Category>0  - Nodata<\/Category>\\\n"
    colors = "<Entry c1=\"0\"	c2=\"0\" c3=\"0\"  c4=\"0\"/>\\\n"
    data = pandas.read_csv(open(csv_file))
    data = data.sort_values(by=['valor'])
    identifier = data.valor.tolist()
    colors_hexadecimal = data.cor.tolist()
    classes = data.classe.tolist()    
    
    for i in range(0, len(colors_hexadecimal)):
        rgb = hex_to_rgb(colors_hexadecimal[i]) 
        colors= colors + "<Entry c1=\"" + rgb[0]+ "\" c2=\"" + rgb[1] + "\" c3=\"" + rgb[2] + "\" c4=\"255\"/>\\\n"
    
    for i in range(0, len(identifier)):
        classes[i] = classes[i].replace("'","\\x27")
        categories = categories + "<Category>" + str(identifier[i]) + " - " + classes[i] + "</Category>\\\n"
    
    tags = "<ColorTable>\\\n" + colors + "</ColorTable>\\\n<CategoryNames>\\\n" + categories + "</CategoryNames>"
    
    return tags

def add_colors_categories(folder_vrt, csv_file):
    changeColorInterpretation = "sed -i 's/Gray/Palette/g' " + folder_vrt + "/*.vrt"
    os.system(changeColorInterpretation)

    addTags =   "sed -i '/Palette/a\\" + process_csv(csv_file) + "' " + folder_vrt + "/*.vrt"
    os.system(addTags)


def merge_images(folder_path, biome):
    #TODO change gdal translate example: gdal_translate -of GTiff -a_nodata 0 -co "TILED=YES" -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co BIGTIFF=YES -co COMPRESS=LZW CERRADO.vrt CERRADO2.tif
    osCommand = 'gdal_translate -of GTiff -a_nodata 0 -co BIGTIFF=YES -co "COMPRESS=LZW" ' + folder_path + "/" + biome + ".vrt " + folder_path + "/" + biome + ".tif"
    os.system(osCommand)

def execute(raster_name, folder_path, folder_vrt, csv_file):

    osCommand = "mkdir -p " + folder_vrt
    os.system(osCommand)

    if raster_name == 'all':
        
        names = get_list_names_raster()

        #execute vrt
        for name in names:
            print('executing vrt', name)
            buildvrt(folder_path, folder_vrt, name)

        #add color table
        add_colors_categories(folder_vrt, csv_file)

        #execute merge
        for name in names:
            print('executing merge', name)
            merge_images(folder_vrt, name)

    else:
        print('executing vrt', raster_name)
        buildvrt(folder_path, folder_vrt, raster_name)
        print('executing merge', raster_name)
        add_colors_categories(folder_vrt, csv_file)
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
    csv_file = "legendas.csv"

    execute(raster_name, folder_path, folder_vrt, csv_file)
    


if __name__ == "__main__":
    interface()