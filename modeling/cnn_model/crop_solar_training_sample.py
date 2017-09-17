from lib_basic_op import *
import operator
from osgeo import gdal, gdalnumeric, ogr, osr
import os
from PIL import Image
import math
import sys

patch_size = 100


def main():
    #shapefile_path = '/home/solarfarm/solar_farmland_analysis/training_data/output/t2t3_near_20151223_crs.shp'
    #shapefile_path = '/Users/chinhui/Works/SolarFarmland/solar_farmland_analysis/training_data/output/t2t3_near_20151223_crs.shp'
    shapefile_path = '/Users/chinhui/Works/SolarFarmland/solar_farmland_analysis/training_data/output/t2t3_near_20151223_fs2_g004_crs_user.shp'

    #raster = '/home/solarfarm/D4SP/solar/Datasets/Fusion/FS2_G004_MS_L4f_20150122_020517_ot_NC.tif'
    raster_path = '/Users/chinhui/Works/SolarFarmland/Datasets/Fusion/FS2_G004_MS_L4f_20150122_020517_ot_NC.tif'
    feature_id = crop_solar_data(patch_size, shapefile_path, raster_path, "sp_training_data_patch100_tmp", 0 )

    shapefile_path = '/Users/chinhui/Works/SolarFarmland/solar_farmland_analysis/training_data/output/t2t3_near_20151223_fs2_g005_crs_user.shp'
    raster_path = '/Users/chinhui/Works/SolarFarmland/Datasets/Fusion/FS2_G005_MS_L4f_20150122_020520_ot_NC.tif'
    crop_solar_data(patch_size, shapefile_path, raster_path, "sp_training_data_patch100_tmp", feature_id )

def crop_solar_data(patch_size, shapefile_path, raster_path, dest_path, feature_id):
   # read raster
   srcImage = gdal.Open(raster_path)
   geoTrans = srcImage.GetGeoTransform()
   image_crop = Image.open(raster_path)
   image_crop.load()
   w, h = image_crop.size

   # read solar position
   shapef = ogr.Open(shapefile_path)
   lyr = shapef.GetLayer( os.path.split( os.path.splitext( shapefile_path )[0] )[1] )
   
   while ( 1 ):
	poly = lyr.GetNextFeature()
	if(poly is None):
	    return feature_id
	points = []
	pixels = []
	geom = poly.GetGeometryRef()
        if geom is None:
           continue

#	iden = poly.GetFieldAsString(0).replace("/","_").replace(" ","_")
#	pts = geom.GetGeometryRef(0)
#	for p in range(pts.GetPointCount()):
#		points.append((pts.GetX(p), pts.GetY(p)))
#	for p in points:
#		pixels.append(world2Pixel(geoTrans, p[0], p[1]))
#

	# filter size >patch_size
	print geom.GetGeometryName()
	env = geom.GetEnvelope()				

	lrx, lry = world2Pixel(geoTrans, env[1], env[2])
	ulx, uly = world2Pixel(geoTrans, env[0], env[3])
	if ( (lrx-ulx)>patch_size or (lry-uly)>patch_size ):
		continue

 #       env_w = lrx-ulx
 #       env_h = lry-uly

	# set crop_patch ul xy
	ul_offx = math.ceil((patch_size-(lrx-ulx))/2)
	ul_offy = math.ceil((patch_size-(lry-uly))/2)

	ulx -= ul_offx
	uly -= ul_offy

	if( ulx < 0 or uly < 0 or (ulx+patch_size)>=w or (uly+patch_size)>=h ):
		continue

	# crop
	print "crop %s" % (feature_id)

	cropped_image = image_crop.crop((int(ulx), int(uly), int(ulx+patch_size), int(uly+patch_size)))

        # paster mask for test
#	cropped_image.paste( (200,200,200), [int(ul_offx),int(ul_offy), int(ul_offx + env_w), int(ul_offy + env_h) ] )

	#cropped_image.save("sp_training_data_patch100/sp_%s.tif" % feature_id)
	cropped_image.save("%s/sp_%s.jpg" % (dest_path ,feature_id), 'JPEG')

	feature_id += 1

if __name__ == "__main__":
    main()
