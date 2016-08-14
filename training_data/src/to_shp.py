#!/usr/bin/python

import os;
import shutil
import sys
import getopt;
from config import *

def main(argv):
   prepare_folder()

   # convert kml to shp file
   kml_to_shp()

   # generate merge shp
   generate_merge_shp()


def kml_to_shp():
   # get tagging folder list
   tagging_folders = next(os.walk(TAGGING_FOLDER))[1]

   # get kml files in each tagging folder
   for tagging_folder in tagging_folders:
      folder = TAGGING_FOLDER + "/" + tagging_folder
      kml_files = os.listdir(folder)

      for kml_file in kml_files:
         if ".kml" in kml_file:
            if "tbd" in kml_file:
               continue

            # assume default t2t3_hybrid
            tmp_shp_folder = SHP_FOLDER_T2T3_NEAR_LABEL
            if "t1" in kml_file:
               tmp_shp_folder = SHP_FOLDER_T1_LABEL

            # generate shp file
            cmd = "%s/ogr2ogr -f 'ESRI Shapefile' %s.shp %s" % (GDAL_PATH, tmp_shp_folder + "/" + kml_file, folder + "/" + kml_file )
            os.system( cmd )

def generate_merge_shp():
   # recreate output folder
   try:
      shutil.rmtree( OUTPUT_FOLDER )
   except:
      pass
   os.mkdir( OUTPUT_FOLDER )

   # merge
   merge_shp( T1_LABEL , SHP_FOLDER_T1_LABEL)
   merge_shp( T2T3_NEAR_LABEL, SHP_FOLDER_T2T3_NEAR_LABEL)

def merge_shp( shp_label, shp_folder ):
   shp_files = os.listdir( shp_folder )
   count = 0;
   for shp_file in shp_files:
      if ".shp" in shp_file:
         if count == 0:
            cmd = "%s/ogr2ogr -f 'ESRI Shapefile' %s.shp %s" % ( GDAL_PATH, OUTPUT_FOLDER + "/" + shp_label, shp_folder + "/" + shp_file )
            os.system(cmd)
         else:
            cmd = "%s/ogr2ogr -f 'ESRI Shapefile' -update -append %s.shp %s -nln %s" % ( GDAL_PATH, OUTPUT_FOLDER + "/" + shp_label, shp_folder + "/" + shp_file, shp_label )
            os.system(cmd)

         count = count + 1

def prepare_folder():
   # recreate shp folder
   try:
      shutil.rmtree( SHP_FOLDER_T1_LABEL )
   except:
      pass
   os.mkdir( SHP_FOLDER_T1_LABEL )

   try:
      shutil.rmtree( SHP_FOLDER_T2T3_NEAR_LABEL )
   except:
      pass
   os.mkdir( SHP_FOLDER_T2T3_NEAR_LABEL )

# main
if __name__ == "__main__":
   main(sys.argv[1:]) 

