## Intro

產生標註shpefile:

由Google Earth標註完成的KML檔案，轉換成shpefile，並根據不同時間區間合併

training_data/output 為最新已合併的shapefile

## Generate tagging shape file

  1. Install required software
    1. python (>=2.7)
    2. install GDAL: http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries

  2. Update config.py
    1. go to training_data/src and update GDAL_PATH variable

  3. Generate shpefile
    1. type `cd training_data; make`

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

