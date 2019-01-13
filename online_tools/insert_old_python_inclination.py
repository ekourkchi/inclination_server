#!/usr/bin/python
import sys
import os
import os.path
import subprocess
import math
import numpy as np
import datetime

import INC_config
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mdb


db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)
db.autocommit(True)

cur=db.cursor()


inFile  = 'oldPython_accepted_pgc_incs.csv'
table   = np.genfromtxt(inFile , delimiter=',', filling_values=-1, names=True, dtype=None)


pgcID = table['pgcID']
inc = table['inc']
email = [' '.join(dummy.split()) for dummy in table['email']]

time = datetime.datetime.strptime("2018-02-20 00:00:00", "%Y-%m-%d %H:%M:%S")
for i in range(len(pgcID)):
    
    
    
    time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    
    query =  "insert into Output_Manoa set pgcID='"+str(pgcID[i])+"', inc="+str(inc[i])+", email='"+email[i]+"', checkoutTime='"+time_str+"', checkinTime='"+time_str+"', inputTable='Old_Python', pgcID1='', pgcID2='', flag=0, not_sure=0, better_image=0, bad_TF=0, ambiguous=0, disturbed=0, HI=0, face_on=0, not_spiral=0, multiple=0, note='', dPA=0.0, zoom=1.0, prjID='Manoa', prjGP='Manoa', ip='255.255.255.255', countryCode='', countryName='', regionName='', cityName='', zipCode='', latitude=0.0, longitude=0.0, timezone='', browser='Python' ;"
    
    cur.execute(query)


    
    
    if i%200==0: 
        
        time =  time + datetime.timedelta(days=1)

cur.close()
