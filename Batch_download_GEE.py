# -*- coding: utf-8 -*-

import ee
ee.Initialize()  
import time
from ee import batch 

imagelist =[]
#the ImageCollection to donwload 
ImageCollection = 'COPERNICUS/S2'

shp_name    = 'aoi'#South' # Centarl  # North
resolution  = '20m' # '10m'

fc_name     = 'users/davidhelman1/General/shp/'+shp_name
folder_name = 'data_S2_'+shp_name
folder      = folder_name + resolution	


fc = ee.FeatureCollection(fc_name)#KML IN ISERAL-all saad
#getInfo call data from the sever to my pc
regiontosave =fc.getInfo()['features'][0]['geometry']['coordinates']

#filterDate the date of the ImageCollection to donwload 
collection = (ee.ImageCollection(ImageCollection).filterDate('2018-05-01','2018-05-21').filterBounds(fc))
#sort by  the date of the ImageCollection
Collectiondata = collection.sort('system:start_time').limit(1000)
#get data to my pc
Dictionarydata = Collectiondata.getInfo()['features']

# get image name
for a in Dictionarydata:
    imagelist.append(str(a['id']))

for image  in imagelist:
    time.sleep(2) 
  #  enddata = ee.Image(str(image)).select('B2','B3','B4','B8')
    enddata = ee.Image(str(image)).select('B5','B6','B7','B8A','B10','B11')

    out = batch.Export.image.toDrive(enddata,folder = folder\
                                     , description= 'S2_'+resolution+'_'+image[14:22]\
                                     , scale=10,maxPixels=298523062\
                                     ,region = regiontosave,crs = 'EPSG:4326')
    process = batch.Task.start(out)