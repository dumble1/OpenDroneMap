import rasterio
import numpy as np
import sys

with rasterio.open(sys.argv[1]) as src:
    dem = src.read(1)
#print (dem[1000:4000,2000])
#print(src.dtypes)

min_h = dem[dem>src.nodata].min()
max_h = dem.max()
act_h = max_h-min_h
color_period = act_h/4
center= max_h-(act_h/2)

#print(dem)
#print(min_h,max_h, center, color_period)
r = np.zeros(dem.shape)
g = np.zeros(dem.shape)
b = np.zeros(dem.shape)



r += np.floor(255 * (dem-center)/color_period)
g += np.floor(510 - abs(dem-center)*255/color_period)
b += np.floor(255 *abs(center-src.nodata)/(color_period*2) - abs(dem-(center+src.nodata)/2)*255/color_period)

#print (b[1000:4000,2000])
r[r>255] =255
r[r<0] = 0
g[g>255]=255
g[g<0] =0
b[b>255]=255
b[b<0]=0


meta = src.meta
meta["dtype"]=rasterio.uint8
meta["nodata"]=0
meta["count"]=3

with rasterio.open(sys.argv[2], 'w', **meta) as dst:
    dst.write_band(1, r.astype(rasterio.uint8))
    dst.write_band(2, g.astype(rasterio.uint8))
    dst.write_band(3, b.astype(rasterio.uint8))
