import ee
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd
import requests
from tqdm import tqdm
import zipfile
import os
import pandas as pd

# initialize google earth engine if it hasn't been initialized yet
if not ee.data._credentials:
    ee.Authenticate()
    ee.Initialize()

# functions for use in the lab

def ee_imgcoll_to_df(imagecollection, lat,lon):
    """Transforms client-side ee.Image.getRegion array to pandas.DataFrame."""
    poi = ee.Geometry.Point(lon, lat)
    arr = imagecollection.getRegion(poi,500).getInfo()

    list_of_bands = imagecollection.first().bandNames().getInfo()

    df = pd.DataFrame(arr)

    # Rearrange the header.
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)

    # Remove rows without data inside.
    df = df[['longitude', 'latitude', 'time', *list_of_bands]].dropna()

    # Convert the data to numeric values.
    for band in list_of_bands:
        df[band] = pd.to_numeric(df[band], errors='coerce')

    # Convert the time field into a datetime.
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')

    # Keep the columns of interest.
    df = df[['time','datetime',  *list_of_bands]]

    return df

# to get the link to download an earth engine image
def getLink(image,fname,aoi):
  link = image.getDownloadURL({
    'scale': 1000,
    'crs': 'EPSG:4326',
    'fileFormat': 'GeoTIFF',
    'region': aoi,
    'name': fname})
  # print(link)
  return(link)
  
# create an earth engine geometry polygon
def addGeometry(min_lon,max_lon,min_lat,max_lat):
  geom = ee.Geometry.Polygon(
      [[[min_lon, max_lat],
        [min_lon, min_lat],
        [max_lon, min_lat],
        [max_lon, max_lat]]])
  return(geom)

# load prism data
def get_prism_image(date1,date2,geometry):
  prism = ee.ImageCollection('OREGONSTATE/PRISM/AN81m')
  prism_img = prism.filterDate(date1,date2).select('ppt').sum().clip(geometry)
  return(prism_img) # returns prism total precipitation, in mm

def get_elev(geometry):
  elev = ee.Image('USGS/NED').clip(geometry)
  return(elev)

def get_srtm(geometry):
  elev = ee.Image('USGS/SRTMGL1_003').clip(geometry)
  return(elev)

def get_gpm_image(date1,date2,geometry):
  gpm = ee.ImageCollection('NASA/GPM_L3/IMERG_MONTHLY_V06')
  gpm_img = gpm.filterDate(date1,date2).select('precipitation').sum().multiply(24*365/12).clip(geometry)
  return(gpm_img) # returns total gpm precipitation in mm

def get_mod16ET(date1,date2,geometry):
  mod16 = ee.ImageCollection('MODIS/006/MOD16A2')
  mod16_img = mod16.filterDate(date1,date2).select('ET').sum().divide(10).clip(geometry)
  return(mod16_img)

def get_mod16PET(date1,date2,geometry):
  mod16 = ee.ImageCollection('MODIS/006/MOD16A2')
  mod16_img = mod16.filterDate(date1,date2).select('PET').sum().divide(10).clip(geometry)
  return(mod16_img)

def download_img(img,geom,fname):
    linkname = getLink(img,fname,geom)
    response = requests.get(linkname, stream=True)
    zipped = fname+'.zip'
    with open(zipped, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    
    with zipfile.ZipFile(zipped, 'r') as zip_ref:
        zip_ref.extractall('')
    os.remove(zipped)
    
# create a bounding box that defines the study area
geom = addGeometry(-95, -85,30,40) # min long, max long, min lat, max lat

# define dates of interest (inclusive).
start = '2017-04-01'
end = '2018-04-01' #can go up to april 2021

# now get gpm precipitation over the same region for a specified time period
gpm_img = get_gpm_image(start,end,geom)
download_img(gpm_img,geom,'gpm_data')

# now get MOD16 ET data over the same time period/region
et_img = get_mod16ET(start,end,geom)
download_img(et_img,geom,'MOD16_ET')

pet_img = get_mod16PET(start,end,geom)
download_img(pet_img,geom,'MOD16_PET')

# now we'll load the rasters
gpm_r = rasterio.open('gpm_data.precipitation.tif')
et_r = rasterio.open('MOD16_ET.ET.tif')
pet_r = rasterio.open('MOD16_PET.PET.tif')

# let's plot them all together. make sure your plots are set to plot outside of thhe console
# check this by going to tools > preferences > ipython console > graphics > graphics backend > Qt5
# expand the plot and zoom in
# comment on the differences between potential evapotranspiratoin and evapotranspiration
plt.figure()
plt.subplot(2,2,1);show(gpm_r);plt.title('Precip, mm, GPM')
plt.subplot(2,2,2);show(et_r);plt.title('ET, mm, MOD16')
plt.subplot(2,2,3);show(pet_r);plt.title('PET, mm, MOD16')
plt.subplot(2,2,4);show(pet_r.read()-et_r.read(),transform=et_r.transform);plt.title('PET - ET, mm, MOD16')

# let's look at a time series at a location that has Eddy Covariance data
# take a look at this link to get an idea of the site: https://ameriflux.lbl.gov/sites/siteinfo/US-HRA
mod16_image_collection =  ee.ImageCollection('MODIS/006/MOD16A2').filterDate(start,end)

mod16_df = ee_imgcoll_to_df(mod16_image_collection,34.5852, -91.7517)

print(mod16_df)

plt.figure();
plt.plot(mod16_df['datetime'],mod16_df['ET']/10/8) #daily ET, mm
plt.plot(mod16_df['datetime'],mod16_df['PET']/10/8) # daily ET, mm
plt.legend(['ET','PET'])

rice_eddy_data = pd.read_csv('AMF_US-HRA_BASE_HH_3-5.csv',skiprows=2,
                             parse_dates=['TIMESTAMP_START','TIMESTAMP_END'],na_values=-9999)

# the column 'LE' has latent heat flux data. How can you convert this to daily ET in mm?
conversion_factor=1234 # change this to some value that makes sense!
rice_eddy_data['ET'] = rice_eddy_data.LE*conversion_factor
rice_eddy_ET = rice_eddy_data[['TIMESTAMP_START','ET']]
rice_eddy_ET = rice_eddy_ET.dropna()

rice_eddy_ET = rice_eddy_ET.set_index('TIMESTAMP_START')

rice_eddy_daily = rice_eddy_ET.resample('W').mean()

plt.plot(rice_eddy_daily)

# comment on the differences between measured ET and estimated ET

# use the remaining lab time to download ET (you choose the dataset) over your study area.
# share one or two figures in your lab report and describe what you did.
