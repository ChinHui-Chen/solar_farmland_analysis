#!/usr/bin/python

from osgeo import ogr
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

def add_field( shp_file, field_name, field_type, field_val ):
         driver = ogr.GetDriverByName('ESRI Shapefile')
         dataSource = driver.Open( shp_file , 1)
         layer = dataSource.GetLayer()
         field_defn = ogr.FieldDefn( field_name, field_type )
         layer.CreateField(field_defn)
         for i in layer:
            layer.SetFeature(i)
            i.SetField( field_name, field_val )
            layer.SetFeature(i)

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
         # get t,a,b
         shp_filename, _, _ = shp_file.split(".");
         township, solar_time, solar_type, solar_pos = shp_filename.split("_");
         if( solar_time != "t1" ):
            solar_time = "t2t3"
         combine = solar_time + "_" + solar_type + "_" + solar_pos

         # update shp file field
         add_field( shp_folder + "/" + shp_file, "Class", ogr.OFTInteger, 1 ) ;
         add_field( shp_folder + "/" + shp_file, "township", ogr.OFTString, township ) ;
         add_field( shp_folder + "/" + shp_file, "solar_time", ogr.OFTString, solar_time ) ;
         add_field( shp_folder + "/" + shp_file, "solar_type", ogr.OFTString, solar_type ) ;
         add_field( shp_folder + "/" + shp_file, "solar_pos", ogr.OFTString, solar_pos ) ;
         add_field( shp_folder + "/" + shp_file, "combine", ogr.OFTString, combine ) ;
         
         #while feature:
         #      feature.CreateField(field_defn)
         #      feature.SetField("Class", 1)
         #      layer.SetFeature(feature)
         #      feature = layer.GetNextFeature()

         #cmd = "%s/ogrinfo %s -sql \"ALTER TABLE %s.kml ADD COLUMN township character(50)\"" % ( GDAL_PATH, shp_folder + "/" + shp_file , shp_filename )
         #print cmd
         #os.system(cmd)
         #cmd = "%s/ogrinfo %s -sql \"UPDATE TABLE %s.kml township = \'%s\'\"" % ( GDAL_PATH, shp_folder + "/" + shp_file , shp_filename, township )
         #print cmd
         #os.system(cmd)
         #cmd = "%s/ogrinfo %s -sql \"ALTER TABLE %s.kml ADD COLUMN Class integer(1)\"" % ( GDAL_PATH, shp_folder + "/" + shp_file , shp_filename )

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

