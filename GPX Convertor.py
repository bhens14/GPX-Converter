import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime, date, time, timezone

plotdf = pd.read_csv('MSH plot locations.csv', usecols=['Plot Name','lat','long'])
plotdf['lat'] = plotdf['lat']*-1

#Lat and long are switched in the input data
ds = gpd.GeoSeries([Point(x,y) for x, y in zip(plotdf['lat'], plotdf['long'])])

plots_NAD27 = gpd.GeoDataFrame(plotdf, geometry=ds)
plots_NAD27.crs = "EPSG:4267"

plots_WGS84 = plots_NAD27.to_crs("EPSG:4326")
plots_export = plots_WGS84[['geometry']]
#plots_export['ele'] = float(0)
#plots_export['magvar'] = float(0)
#plots_export['time'] = datetime.combine(date(1900,1,1),time(0,0))
#plots_export['geoidheight'] = float(0)
plots_export['name'] = plots_WGS84[['Plot Name']]
print(plots_export)

plots_export.to_file('MSHplots.gpx', 'GPX')
