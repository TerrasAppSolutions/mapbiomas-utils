
python export_gcs_servidor.py "gs://mapbiomas-dev-storage/COLECOES/COLECAO31/INTEGRACAOV2/*.tif"  "/mnt/disks/data/data2/collections/COLECAO3_1/INTEGRACAO"


python export_gcs_servidor.py "gs://mapbiomas-dev-storage/COLECOES/COLECAO31/TRANSICAOV2/*.tif"  "/mnt/disks/data/data2/collections/COLECAO3_1/TRANSICAO"

python buildvrt_util.py integracao "/mnt/disks/data/data2/collections/COLECAO3_1/INTEGRACAO" "/mnt/disks/data/data2/collections/COLECAO3_1/VRT/INTEGRACAO"

python buildvrt_util.py transicao "/mnt/disks/data/data2/collections/COLECAO3_1/TRANSICAO" "/mnt/disks/data/data2/collections/COLECAO3_1/VRT/TRANSICAO"


python buildovr_util.py integracao  "/mnt/disks/data/data2/collections/COLECAO3_1/VRT/INTEGRACAO" 1 &


python buildovr_util.py integracao  "/mnt/disks/data/data2/collections/COLECAO3_1/VRT/INTEGRACAO" 2 &