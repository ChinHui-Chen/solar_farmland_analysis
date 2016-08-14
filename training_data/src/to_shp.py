#!/usr/bin/python

import os;
import shutil
import sys
import getopt;
from config import *

def main(argv):
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
            timestamp_label = "t2t3_near_20151223";
            if "t1" in kml_file:
               timestamp_label = "t1_2013_1123"

            # create shp folder
            tmp_shp_folder = SHP_FOLDER + "_" + timestamp_label
            try:
               os.mkdir( tmp_shp_folder )
            except:
               shutil.rmtree( tmp_shp_folder )
               os.mkdir( tmp_shp_folder )
            
            # generate shp file
            cmd = "%s/ogr2ogr -f 'ESRI Shapefile' %s.shp %s" % (GDAL_PATH, tmp_shp_folder + "/" + kml_file, folder + "/" + kml_file )
            os.system( cmd )

if __name__ == "__main__":
   main(sys.argv[1:]) 

