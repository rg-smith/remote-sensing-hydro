import rasterio
from rasterio.warp import reproject, Resampling
import ee

def reproject_rasterio(src,dest): # reprojects a rasterio raster to exactly match grid of anothe rasterio raster
    dat,transform=reproject(rasterio.band(src,1),dest.read(1),
              dst_crs=dest.crs,dst_resolution=dest.res,
              dst_transform=dest.transform,
              dst_nodata=np.nan)
    return(dat,transform)

def reproject_rasterio_crs(src,res,epsg): # reprojects a rasterio raster with a user-defined resolution and epsg
    crs=rasterio.crs.CRS.from_epsg(epsg)
    dat,transform=reproject(rasterio.band(src,1),
              dst_crs=crs,dst_resolution=res,
              dst_nodata=np.nan)
    return(dat,transform)
  
def get_prism_image(date1,date2,geometry): # pulls precipitation data from PRISM
  prism = ee.ImageCollection('OREGONSTATE/PRISM/AN81m')
  prism_img = prism.filterDate(date1,date2).select('ppt').sum().clip(geometry)
  return(prism_img) # returns prism total  precipitation, derived from monthly, in mm

def get_mod16(date1,date2,geometry): # pulls evapotranspiration data from MODIS
  mod16 = ee.ImageCollection('MODIS/006/MOD16A2')
  mod16_img = mod16.filterDate(date1,date2).select('ET').sum().divide(10)
  return(mod16_img) # returns prism average monthly precipitation, in mm    

def get_ndwi(date1,date2,geometry): # pulls NDWI derived from MODIS
  date11=date1[0:4]+'-01-01'
  date22=date1[0:4]+'-12-31'
  def normalized_diff(image):
      nir = image.select('sur_refl_b02')
      swir = image.select('sur_refl_b05')
      ndwi = nir.subtract(swir).divide(nir.add(swir)).rename('NDWI')
      # image = image.set('value', img2).rename('NDWI')
      return(ndwi)
  modis = ee.ImageCollection('MODIS/006/MOD09A1').select(['sur_refl_b02','sur_refl_b05']).filterDate(date1,date2)
  ndwi = modis.map(normalized_diff)
  ndwi_img = ndwi.select('NDWI').mean()
  return(ndwi_img) # returns average NDWI from MODIS

def export_to_drive(raster,filename,foldername,geometry): # exports a single google earth engine image to google drive
  # Export the image, specifying scale and region.
  task = ee.batch.Export.image.toDrive(**{
      'image': raster,
      'description': filename,
      'folder': foldername,
      'fileNamePrefix': filename,
      'scale': 1000,
      'region': geometry,
      'fileFormat': 'GeoTIFF',
      'formatOptions': {
        'cloudOptimized': 'true'
      },
  })
  task.start()
  
def addGeometry(min_lon,max_lon,min_lat,max_lat): # creates a geometry (polygon) with min/max lat and lon values
  geom = ee.Geometry.Polygon(
      [[[min_lon, max_lat],
        [min_lon, min_lat],
        [max_lon, min_lat],
        [max_lon, max_lat]]])
  return(geom)

def getLink(image,fname,aoi,scale=500): # creates a link to download a single google earth engine image to local computer
  link = image.getDownloadURL({
    'scale': scale,
    'crs': 'EPSG:4326',
    'fileFormat': 'GeoTIFF',
    'region': aoi,
    'name': fname})
  # print(link)
  return(link)

def download_img(img,geom,fname): # downloads a single google earth engine image to local computer
    linkname = getLink(img,fname,geom)
    response = requests.get(linkname, stream=True)
    zipped = fname+'.zip'
    with open(zipped, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    
    with zipfile.ZipFile(zipped, 'r') as zip_ref:
        zip_ref.extractall('')
    os.remove(zipped)
