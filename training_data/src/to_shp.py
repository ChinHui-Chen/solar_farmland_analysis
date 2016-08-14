#!/usr/bin/python

import os;
import shutil
import sys
import getopt;
from config import *

def main(argv):
   # get tagging folder list
   tagging_folders = next(os.walk(TAGGING_FOLDER))[1]

   # recreate shp folder
   shutil.rmtree( SHP_FOLDER_T1_LABEL )
   os.mkdir( SHP_FOLDER_T1_LABEL )
   shutil.rmtree( SHP_FOLDER_T2T3_NEAR_LABEL )
   os.mkdir( SHP_FOLDER_T2T3_NEAR_LABEL )

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

   # generate merge shp


if __name__ == "__main__":
   main(sys.argv[1:]) 

