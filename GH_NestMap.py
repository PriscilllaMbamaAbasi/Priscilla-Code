#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.geometry import Point


# In[2]:


#Import world data from geopandas library

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

#plot world map filled with colour
#world.plot()

#plot boundary or outline of the world only
world.boundary.plot()


# In[3]:


#Load all shapefiles
print ("Loading shapefiles.....")
ghana = gpd.read_file("D:\DSP\Databases\Ghana\Ghana_New_16_Region")
district = gpd.read_file("D:\DSP\Databases\Ghana\Ghana_New_260_District")
nest = gpd.read_file("D:\DSP\Databases\Ghana\Ghana Nest Locations.shp")
service_range = gpd.read_file("D:\DSP\Databases\Ghana\Range\GH_ServiceRange.shp")
print ("All shapefiles loaded!")


# In[4]:


fig, ax = plt.subplots(figsize = (12,8))
ghana.boundary.plot(ax=ax, color="black")
service_range.boundary.plot(ax=ax, color = "red")
nest.plot(ax=ax, color="black")

#without this, the map will still show
#plt.show()

# This line removes the axis/border around the map 
fig, ax.axis('off')


# In[5]:


#Coloring a shapefile
#fill - inside part
#stroken/line/edge - outline
#StyleMaps

print("Styling the map")
fig, ax = plt.subplots(figsize = (12,12))
#ghana.plot(ax=ax, color="grey", edgecolor = "white")
#ghana.plot(ax=ax, color="#F0EAD7", edgecolor = "white")
ghana.plot(ax=ax, color="#F0EAD7", edgecolor = "#828282", linewidth =0.25)
service_range.boundary.plot(ax=ax, color = "red", linewidth = 0.5)
nest.plot(ax=ax, color="black") 
ax.axis('off')
ax.set_title("ZIPLINE GHANA", fontsize = 20, fontweight = "bold", fontname = "Times New Roman")
plt.show()


# In[6]:


#save map as png
'''
import gmaps
m= gmaps.Map()
m.add_layer(gh_map)
m.save("map.png")
'''


# In[7]:


plt.savefig('ghmap.jpg')


# In[ ]:




