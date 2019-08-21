#!/usr/bin/python
import os

def export_geojson_GCS_to_server(gcs_url, dir_dst):
    osCommand = "gsutil -m cp -R " + gcs_url + " " +  dir_dst
     
    print(osCommand)
    os.system(osCommand)