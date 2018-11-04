import sys
from netCDF4 import Dataset
import numpy
import fiona
import shapely.geometry
import shapely.prepared
import rtree

def init():
    # Opening the file
    netcdf_dataset = Dataset( sys.argv[1], 'r', format = "NETCDF4")
    # init files meta-data
    point_file_driver = polygon.driver
    coordsys = polygons.crs
    schema = {'geometry': 'Point','properties': {'lon': 'int:4','lat': 'int:4'}}
    #  making points on the map in shape file  
    
    result_to = "../output/SERVIR_STK/GLDAS_VIC.pnt_tst.shp" # location to store results
    with fiona.open( result_to, 'w', driver=netcdf_dataset, crs=coordsys, schema=schema) as temp:
    for i in range(len(netcdf_dataset.dimensions['lon'])):
        lont = netcdf_dataset.variables['lon'][i]

        for j in range(len(netcdf_dataset.dimensions['lat'])):
            lat = netcdf_dataset.variables['lat'][j]
            pfProperty = { 'lon': lont, 'lat': lat }
            pfGeometry = shapely.geometry.mapping(
                        shapely.geometry.Point((lont, lat)))
            temp.write({ 'properties': pfProperty,'geometry': pfGeometry,})

    print("***************************DONE****************************************")
    gridCell(result_to)

def gridCell(result_to):
   
    # Loading points into an rtree index with the shapely default value 
    points = fiona.open(result_to, 'r')
    index = rtree.index.Index()

    for point in points:
        point_id = int(point['id'])
        shape = shapely.geometry.shape(point['geometry'])
        index.insert(point_id, shape.bounds)

    total = 0
    longitudes, latitudes = list(), list()
    polygon = fiona.open( sys.argv[2], 'r')

    for polygon in polygons:
        poly_geom = shapely.geometry.shape(polygon['geometry'])
        prep_geom = shapely.prepared.prep(poly_geom)
        for point_id in [int(x) for x in list(index.intersection(poly_geom.bounds))]:
            point = points[point_id]
            point_geom = shapely.geometry.shape(point['geometry'])
            if prep_geom.contains(point_geom):
                point_lon = point["properties"]['lon']
                point_lat = point["properties"]["lat"]
                longitudes.append(point_lon)
                latitudes.append(point_lat)
                total += 1
    print("Done Solving, found the following:")
    print("Number of grid cells of interest: " + str(total))
    print("Latitudes of interest:", interest_latitudes)
    print("Longitude of interest:", s)

    if __name__ == "__main__":
        init()
