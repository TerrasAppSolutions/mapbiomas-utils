import ee
import argparse

ee.Initialize()


INTEGRACAO = ee.Image("projects/mapbiomas-workspace/public/collection3_1/mapbiomas_collection31_integration_v1")

BIOMAS_IMAGE = ee.Image("projects/mapbiomas-workspace/AUXILIAR/biomas-raster")

GEOMETRY = BIOMAS_IMAGE.geometry().bounds().getInfo()['coordinates']

BIOMAS_LIST = ["AMAZONIA", "CAATINGA", "CERRADO", "MATAATLANTICA", "PAMPA", "PANTANAL"]

IDS_BIOMAS = {
  "AMAZONIA":1,
  "CAATINGA":5,
  "CERRADO":4,
  "MATAATLANTICA":2,
  "PAMPA":6,
  "PANTANAL":3
}



def ExportImage(image, biomaName, bucketPrefix):

    imageName = "INTEGRACAO_BIOMA_" + biomaName

    task = ee.batch.Export.image.toCloudStorage(**{
        "image": image,
        "bucket":"mapbiomas-dev-storage",
        "fileNamePrefix": bucketPrefix + "/" + biomaName + "_",
        "description": imageName,
        "region": GEOMETRY,
        "scale": 30,
        "maxPixels": 1e13,
        "skipEmptyTiles":True,
        'pyramidingPolicy':'{".default":"mode"}'
        
    }
    )

    task.start()

    print(task.status())



def ExportAllBiomas(bucketPrefix):

    for bioma in BIOMAS_LIST:
        image = INTEGRACAO.mask(BIOMAS_IMAGE.eq(IDS_BIOMAS[bioma]))
        ExportImage(image, bioma, bucketPrefix)


def interface():
    parser = argparse.ArgumentParser(description='Export the images to Google Cloud Storage')

    parser.add_argument('bucketPrefix', type=str, help='Write the bucket prefix path')

    bucketPrefix = parser.parse_args().bucketPrefix

    ExportAllBiomas(bucketPrefix)

if __name__ == "__main__":
    interface()








