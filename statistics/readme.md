# Commands

- Example Commands to export from cloud storage

```sh
mkdir -p BIOMAS/COBERTURA
mkdir -p BIOMAS/TRANSICAO

gsutil -m cp -r  gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO3_1/BIOMAS/COBERTURAV2/*.geojson  BIOMAS/COBERTURA/
gsutil -m cp -r  gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO3_1/BIOMAS/TRANSICAOV2/*.geojson  BIOMAS/TRANSICAO/
```
