from lib_basic_op import *
import operator
from osgeo import gdal, gdalnumeric, ogr, osr
import os
from PIL import Image
import math
import sys
import random
import numpy as np

patch_size = 100

def main():
    shapefile_path = '/Users/chinhui/Works/SolarFarmland/solar_farmland_analysis/training_data/output/t2t3_near_20151223_fs2_g004_crs_user.shp'
    raster_path = '/Users/chinhui/Works/SolarFarmland/Datasets/Fusion/FS2_G004_MS_L4f_20150122_020517_ot_NC.tif'
    # crop solar data
#    feature_id = crop_solar_data(patch_size, shapefile_path, raster_path, "sp_training_data_patch100_tmp", 0 )
    # crop non solar data
    progress_id = crop_non_solar_data(patch_size, shapefile_path, raster_path, "sp_training_data_patch100_tmp2", 0, 50)

    shapefile_path = '/Users/chinhui/Works/SolarFarmland/solar_farmland_analysis/training_data/output/t2t3_near_20151223_fs2_g005_crs_user.shp'
    raster_path = '/Users/chinhui/Works/SolarFarmland/Datasets/Fusion/FS2_G005_MS_L4f_20150122_020520_ot_NC.tif'
    # crop solar data
#    crop_solar_data(patch_size, shapefile_path, raster_path, "sp_training_data_patch100_tmp", feature_id )
    # crop non solar data
    crop_non_solar_data(patch_size, shapefile_path, raster_path, "sp_training_data_patch100_tmp2", progress_id, 20)


def crop_non_solar_data(patch_size, shapefile_path, raster_path, dest_path, progress_id ,sample_size):
   srcImage = gdal.Open(raster_path)
   geoTrans = srcImage.GetGeoTransform()
   image_crop = Image.open(raster_path)
   image_crop.load()
   w, h = image_crop.size

   sample_count = 0
   sample_index = []
   while(sample_count < sample_size):
      # sample between w, h
      sample_w = random.randint(0, w-1)
      sample_h = random.randint(0, h-1) 

      # check if duplicated
      if (sample_w, sample_h) in sample_index:
         continue
      # check if the patch is out of boundary
      elif sample_w + patch_size >= w or sample_h + patch_size >= h:
         continue
      # check if the starting pixel is (0, 0, 0)
      elif image_crop.getpixel((sample_w,sample_h)) == (0, 0, 0):
         continue
      # check if contain solar data
      solar_pos = generate_solar_pos_array(shapefile_path, geoTrans)
      if is_contain_solar_data( sample_w, sample_w + patch_size, sample_h, sample_h + patch_size, solar_pos ):
         continue

      # crop image
      cropped_image = image_crop.crop( (sample_w, sample_h, sample_w + patch_size, sample_h + patch_size) )
      cropped_arr = np.array(cropped_image)

      # check if the image contains (0, 0, 0)
      if is_contain_zero_rgb_val(cropped_arr, patch_size):
         continue

      # save image
      cropped_image.save( "%s/non_sp_%s.jpg" % ( dest_path ,progress_id ), 'JPEG' )

      # post processing
      sample_index.append( (sample_w, sample_h) )
      progress_id += 1
      sample_count += 1
   return progress_id

def is_contain_zero_rgb_val( cropped_arr, patch_size ):
   for i in range(patch_size):
      for j in range(patch_size):
         if cropped_arr[i][j][0] == 0 and cropped_arr[i][j][1] == 0 and cropped_arr[i][j][2] == 0:
            return True
   return False

def is_contain_solar_data(x_left, x_right, y_upper, y_lower, solar_pos):
   for pos in solar_pos: # 0:lrx, 1:ulx, 2:lry, 3:uly
      if pos[0] >= x_left and pos[0] <= x_right and pos[2] >= y_upper and pos[2] <= y_lower :
         return True
      elif pos[1] >= x_left and pos[1] <= x_right and pos[3] >= y_upper and pos[3] <= y_lower :
         return True
      elif pos[0] >= x_left and pos[0] <= x_right and pos[3] >= y_upper and pos[3] <= y_lower :
         return True
      elif pos[1] >= x_left and pos[1] <= x_right and pos[2] >= y_upper and pos[2] <= y_lower :
         return True
   return False

def generate_solar_pos_array(shapefile_path, geoTrans):
   shapef = ogr.Open(shapefile_path)
   lyr = shapef.GetLayer( os.path.split( os.path.splitext( shapefile_path )[0] )[1] )

   solar_pos = []
   while ( 1 ):
	poly = lyr.GetNextFeature()
	if(poly is None):
	    break
	geom = poly.GetGeometryRef()
        if geom is None:
           continue

	env = geom.GetEnvelope()				
	lrx, lry = world2Pixel(geoTrans, env[1], env[2])
	ulx, uly = world2Pixel(geoTrans, env[0], env[3])
         
        solar_pos.append( (lrx, ulx, lry, uly) )
   return solar_pos 


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

	# filter size>patch_size
	env = geom.GetEnvelope()				
	lrx, lry = world2Pixel(geoTrans, env[1], env[2])
	ulx, uly = world2Pixel(geoTrans, env[0], env[3])
	if ( (lrx-ulx)>patch_size or (lry-uly)>patch_size ):
		continue

 #       env_w = lrx-ulx
 #       env_h = lry-uly

	# set crop_patch upper left x,y
	ul_offx = math.ceil((patch_size-(lrx-ulx))/2)
	ul_offy = math.ceil((patch_size-(lry-uly))/2)
	ulx -= ul_offx
	uly -= ul_offy
        
        # check boundary case
	if( ulx < 0 or uly < 0 or (ulx+patch_size)>=w or (uly+patch_size)>=h ):
		continue

	# crop
	print "crop %s" % (feature_id)
	cropped_image = image_crop.crop((int(ulx), int(uly), int(ulx+patch_size), int(uly+patch_size)))

        # paster mask for test
#	cropped_image.paste( (200,200,200), [int(ul_offx),int(ul_offy), int(ul_offx + env_w), int(ul_offy + env_h) ] )

	cropped_image.save("%s/sp_%s.jpg" % (dest_path ,feature_id), 'JPEG')

        # post processing
	feature_id += 1

if __name__ == "__main__":
    main()
