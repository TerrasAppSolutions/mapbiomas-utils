#!/usr/bin/python
import os
import argparse

def exportCoberturaGCSToServer(gcs_url, dir_dst):
    osCommand = "gsutil -m cp -r " + gcs_url + " " +  dir_dst
     
    print osCommand
    os.system(osCommand)
  

if __name__ == "__main__":
        

    parser = argparse.ArgumentParser(description='Export image from GCS to Server')

    parser.add_argument('gcs_url', type=str,  help='write the url in google cloud storage')

    parser.add_argument('dir_dst', type=str,  help='write the path in the server')
    

    gcs_url = parser.parse_args().gcs_url
    dir_dst = parser.parse_args().dir_dst

    exportCoberturaGCSToServer(gcs_url, dir_dst)

