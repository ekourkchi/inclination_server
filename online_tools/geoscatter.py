# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  Creation DATE:	June, 14, 2018         
# //
# //  Description:      + Geolocation Scatter
# //                    
# //****************************************************************/

# import necessary packages
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import subprocess
import math
import matplotlib.pyplot as plt
import matplotlib; matplotlib.pyplot.switch_backend('agg')
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

import numpy as np
from astropy.table import Table, Column 
import pylab as py
import time
import datetime

import INC_config
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mdb

import pygeoip
gi = pygeoip.GeoIP('GeoLiteCity.dat')
####http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

#######################################
def add_ip(myDict, ip):
    
    global gi
    
    try: 
        if not ip in myDict:
            myDict[ip] = gi.record_by_addr(ip)
    except: 
        ip = '94.184.211.152'
        if not ip in myDict:
            myDict[ip] = gi.record_by_addr(ip)
        
#######################################
def length(myDict):
    
    n=0
    for key in myDict: n+=1
    return n
#######################################
db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)
cur=db.cursor()

query = "SELECT ip FROM Output_Manoa;"
cur.execute(query)
results=cur.fetchall()
ip1 = np.asarray([x[0] for x in results])


query = "SELECT ip FROM Output_Guest;"
cur.execute(query)
results=cur.fetchall()
ip2 = np.asarray([x[0] for x in results])

myDict = dict()
for i in range(len(ip1)):
    add_ip(myDict, ip1[i])
for i in range(len(ip2)):
    add_ip(myDict, ip2[i])


#############################################################

fig=plt.figure(figsize=(8,4))
ax = fig.add_axes([0.05,0.05,0.9,0.9])

map = Basemap(projection='cyl')

map.drawmapboundary(fill_color='lightskyblue')
map.fillcontinents(color='khaki',lake_color='lightskyblue')
map.drawcoastlines()

for ip in myDict:
    
    addr = myDict[ip]
    lon = addr['longitude']
    lat = addr['latitude']
    x, y = map(lon, lat)
    map.plot(x, y, marker='o',color='red',markersize=3)


ax.annotate("Hawaii",(-171,11), fontsize=11)

plt.savefig('globe_map.png')
plt.close(fig)    # close the figure
#############################################################
fig=plt.figure(figsize=(6,4))
ax = fig.add_axes([0.05,0.05,0.9,0.9])

map = Basemap(llcrnrlon=-160.5,llcrnrlat=18.5,urcrnrlon=-154.5,urcrnrlat=22.5, projection='cyl')

shp_info = map.readshapefile('st99_d00','states',drawbounds=True,
                           linewidth=0.45,color='gray')
shp_info_ = map.readshapefile('st99_d00','states',drawbounds=False)


map.drawmapboundary(fill_color='lightskyblue')

for ip in myDict:
    
    addr = myDict[ip]
    lon = addr['longitude']
    lat = addr['latitude']
    x, y = map(lon, lat)
    map.plot(x, y, marker='o',color='red',markersize=3)

for nshape, shapedict in enumerate(map.states_info):
     if shapedict['NAME'] in ['Hawaii']:
         seg = map.states[int(shapedict['SHAPENUM'] - 1)]
         poly = Polygon(seg, facecolor='khaki', edgecolor='gray', linewidth=.45)
         ax.add_patch(poly)

ax.annotate("Oahu",(-158.27,21.8), fontsize=12)
ax.annotate("Maui",(-156.28,20.98), fontsize=12)
ax.annotate("Hawaii",(-155.8,19.54), fontsize=12)
ax.annotate("Molokai",(-157.23,21.31), fontsize=12)
ax.annotate("Kauai",(-159.7,21.7), fontsize=12)
ax.annotate("Lanai",(-157.55,20.74), fontsize=12)

ax.annotate("HAWAII",(-160.24,18.75), fontsize=16)


plt.savefig('hawaii_map.png')
plt.close(fig)    # close the figure
#############################################################

























