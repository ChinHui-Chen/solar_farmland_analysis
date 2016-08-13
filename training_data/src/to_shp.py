import os;
import sys, getopt;

# /Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr -f 'ESRI Shapefile' Cihtong_t1_a1_b1.shp Cihtong_t1_a1_b1.kml

#folder_list = [ "../Baozhong", "../Cihtong", "../Dapi", "../Dounan", "../Huwei", "../Siluo" ]
folder_list = [ "../tagging/Beigang", "../tagging/Lunbei", "../tagging/Eulen"]

for folder in folder_list:
   kml_list = os.listdir(folder)

   for kml in kml_list:
      if ".kml" in kml:
         name = os.path.splitext(kml)[0]
         name_with_path = folder + "/" + name
         cmd = "/Library/Frameworks/GDAL.framework/Versions/1.11/Programs/ogr2ogr -f 'ESRI Shapefile' %s.shp %s.kml" % ( name_with_path, name_with_path )
         os.system( cmd )

