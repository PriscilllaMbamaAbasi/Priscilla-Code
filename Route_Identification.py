#pip install -r required_Packages.txt

#Load packages
import geopandas as gpd
import pandas as pd
import os
import shapely.geometry as point
from sys import argv
from pyproj import crs
import argparse


def printLoadSuccess():
    print("\"LOADED ALL REQUIRED PACKAGES\"")

def main(routes, debug):
    printLoadSuccess()
    
    #Add the details of the location to be blocked
    Town = str(input("Enter Name of the town:"))
    Lat = float(input("Enter Latitude:"))
    Long = float(input("Enter Longitude:"))
    
    '''#Add the details of the location to be blocked
    Town = input("Enter Name of the town:")
    Lat = input("Enter Latitude:")
    Long = input("Enter Longitude:")
    
    try:
        Town = str(input("Enter Name of the town:"))
        Lat = float(input("Enter Latitude:"))
        Long = float(input("Enter Longitude:"))
    except ValueError:
        print("Error! Please enter the correct name of the town and coordinates")
    finally:
        print("Your inputs are:", Town, Lat, Long)'''
    
    print ("\"CONVERTING INPUT (Lat & Long) TO GEODATAFRAME\"")
    #make output filenames
    routes_affected_csv = "{town}_affected_routes.csv".format(town=Town)
    routes_affected_shp = "{town}_affected_routes.shp".format(town=Town)

    #Convert input to a dataframe
    df = pd.DataFrame({"Town": [Town], "Lat" :[Lat], "Long" :[Long]})
    #Convert dataframe to geodataframe
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Long, df.Lat))
    #export the coordinates of the location to be blocked to csv
    

    #Convert route shapefile to Geodataframe
    routes = gpd.GeoDataFrame.from_file(routes)
    #print(routes)
    
    print("\"CHECKING THE CRS OF THE TOWN.....\"")

    #convert coordinates/geodataframe from epsg 4326 to epsg 32360
    #gdf.crs = {"init" : "epsg:4326"} #deprecated and will not be in future versions
    gdf.crs =  "epsg:4326"
    gdf_new = gdf.to_crs("epsg:32630")
    print("The CRS of the location to be blocked is:", gdf_new.crs)
    
    print("\"CHECKING THE CRS OF THE ROUTES.....\"")
     
    #routes.crs = {"init" : "epsg:4326"} #deprecated and will not be in future versions
    routes.crs = "epsg:4326"
    routes_new = routes.to_crs("epsg:32630")
    print("The CRS of the routes are:", routes_new.crs)

    #create a buffer
    distance = int(input("Enter the buffer radius in metres: "))
    buffer_200= gdf_new['geometry'].buffer(distance)
    #print(buffer_200)
    #type(buffer_200)

    #Covert Geoseries to Geodataframe
    buffer_gdf = gpd.GeoDataFrame(gpd.GeoSeries(buffer_200))
    buffer_gdf = buffer_gdf.rename(columns={0:'geometry'}).set_geometry('geometry')
    #Specified CRS of the buffer to remove warnings from script
    buffer_gdf.crs = "epsg:32630"
    print("The CRS of the routes are:", buffer_gdf.crs)
    #type(buffer_gdf)
    if debug:
        buffer_gdf.to_file("debug_buffer.shp")
        
    print("\"CALCULATING INTERSECTIONS.....\"")

    #create intersection
    routes_affected = gpd.overlay(routes_new, buffer_gdf, how = "intersection")
    output = gpd.GeoDataFrame(routes_affected)
    routes_affected[['Name']].to_csv(routes_affected_csv)
    routes_affected.to_file(routes_affected_shp)
    
    print( "\"ALL DONE!\"")
    print ("\"FIND THE LIST OF ROUTES TO BE BLOCKED IN YOUR FOLDER.\"")

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--routes', '-r', required=True, help='Input Shp file of flight routes')
    parser.add_argument('--debug', '-d', required=False, default=False, help='Flag to generate debug output')
    args=parser.parse_args()
    main(args.routes, args.debug)

