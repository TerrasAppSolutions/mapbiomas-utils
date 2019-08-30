import pandas as pd
import pprint
import legend_lib

def gen_class_mapfile_n1(pixel, rgb):
    pixel_str = str(pixel)    

    return """

CLASS
  EXPRESSION ([pixel] = {0} AND "{0}" IN '%classification_ids%')
  STYLE 
    COLOR "{1}"
  END
END""".format(pixel_str, rgb)

def gen_class_mapfile_n2(pixel, pixel_c1, rgb):
    pixel_str = str(pixel)
    pixel_c1_str = str(pixel_c1)

    return """

CLASS
  EXPRESSION ([pixel] = {1} AND !("{1}" IN '%classification_ids%') AND ("{0}" IN '%classification_ids%'))
  STYLE 
    COLOR "{2}"
  END
END""".format(pixel_str, pixel_c1, rgb)

def gen_class_mapfile_n3(pixel, pixel_c1, pixel_c2, rgb):
    pixel_str = str(pixel)
    pixel_c1_str = str(pixel_c1)
    pixel_c2_str = str(pixel_c2)

    return """
    
CLASS
  EXPRESSION ([pixel] = {2} AND !("{1}" IN '%classification_ids%') AND !("{2}" IN '%classification_ids%') AND ("{0}" IN '%classification_ids%'))
  STYLE 
    COLOR "{3}"
  END
END""".format(pixel_str, pixel_c1, pixel_c2, rgb)

def get_mapfile_text_pixel(pixel, nivel, rgb, data):

    data_text = []
            
    title = """


    ##########################
    ##    CLASSE """ + str(pixel) + """ ##########
    ##########################
    """

    data_text.append(title)
    data_text.append(gen_class_mapfile_n1(pixel, rgb))

    if nivel == 1:
        
        legends_childrens_l2 = [_ for _ in data if _['valor_l1'] == pixel and _['nivel'] == 2]
        
        for item_children in legends_childrens_l2:
            
            class_mapfile = gen_class_mapfile_n2(pixel, item_children['valor'], rgb)
            data_text.append(class_mapfile)
            
        legends_childrens_l3 = [_ for _ in data if  _['valor_l1'] == pixel and _['nivel'] == 3]
        
        for item_children in legends_childrens_l3:
            
            pixel_c1 = item_children['valor_l2']            
            pixel_c2 = item_children['valor_l3']
            
            class_mapfile = gen_class_mapfile_n3(pixel, pixel_c1, pixel_c2, rgb)
            data_text.append(class_mapfile)

            
    if nivel == 2:
        
        legends_childrens_l2 = [_ for _ in data if _['valor_l2'] == pixel and _['nivel'] == 3]
        
        for item_children in legends_childrens_l2:
            
            class_mapfile = gen_class_mapfile_n2(pixel, item_children['valor'], rgb)
            data_text.append(class_mapfile)

    return data_text
        

def get_pixel_nivel(valor, valor_l1, valor_l2):
    nivel = None
    if valor_l1 == valor and valor_l2 == valor:
        nivel = 1
    elif valor_l1 != valor and valor_l2 == valor:
        nivel = 2
    elif valor_l1 != valor and valor_l2 != valor:
        nivel = 3
    return nivel

def get_mapfile_text(data):

    data_mapfile_text = []

    for legenda_meta in data:
        pixel = legenda_meta['valor']
        valor_l1 = legenda_meta['valor_l1']
        valor_l2 = legenda_meta['valor_l2']
        nivel = get_pixel_nivel(pixel, valor_l1, valor_l2)
        legenda_meta['nivel'] = nivel
    
 
    for legenda_meta in data:
        pixel = legenda_meta['valor']
        valor_l1 = legenda_meta['valor_l1']
        valor_l2 = legenda_meta['valor_l2']
        rgb = legenda_meta['cor']
        nivel = legenda_meta['nivel']
        data_mapfile_text = data_mapfile_text + get_mapfile_text_pixel(pixel, nivel, rgb, data)

    return "".join(data_mapfile_text) 

def write_mapfile(text, path):
    txt = open(path, 'w') 
    txt.write(text)
    txt.close()

def start(path_csv):

    data = legend_lib.adjust_data(path_csv)
    data = sorted(data, key = lambda i: i['valor']) 

    text = get_mapfile_text(data)

    write_mapfile(text, "style_coverage.map")

if __name__ == "__main__":
    path_csv = "./data/legenda_brasil_col4_20190829.csv"   

    start(path_csv)  