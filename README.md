## Intro

產生標註shpefile:

由Google Earth標註完成的KML檔案，轉換成shpefile，並根據不同時間區間合併

training_data/output 為最新已合併的shapefile

## Generate tagging shape file

### Install required software

  * python
  * install GDAL: http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries

### Update config.py

  * go to training_data/src and update GDAL_PATH variable

### Generate shpefile

  * cd training_data; make

## Contributor

  * Chan-Kuan Hou
  * Chia-Ching Lin
  * Chia-Kai Liu
  * Chin-Hui Chen
  * Dongpo Deng
  * Johnson Hsieh
  * Yen-Lin Wu
  * 周立筠
  * 楊承翰

