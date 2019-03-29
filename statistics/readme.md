# Commands

### Example Commands to export from cloud storage

- Create Folders Where do you want to save the geojson

```sh
mkdir -p BIOMAS/COBERTURA
mkdir -p BIOMAS/TRANSICAO
mkdir -p BACIAS/COBERTURA
mkdir -p BACIAS/TRANSICAO
```

- Upload from Cloud Storage

```sh
gsutil -m cp -r  gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO3_1/BIOMAS/COBERTURAV2/*.geojson  BIOMAS/COBERTURA/
gsutil -m cp -r  gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO3_1/BIOMAS/TRANSICAOV2/*.geojson  BIOMAS/TRANSICAO/
gsutil -m cp -r  gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO3_1/BACIAS/COBERTURAV2/*.geojson  BACIAS/COBERTURA/
gsutil -m cp -r  gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO3_1/BACIAS/TRANSICAOV2/*.geojson  BACIAS/TRANSICAO/
```
