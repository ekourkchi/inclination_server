# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  Creation DATE:	February, 21, 2018         
# //
# //  Description:      + Generating table for Input catalog of galaxies to be used
# //                      in the database preferably for each individual user
# //                    
# //****************************************************************/

# import necessary packages
#import _mysql
import MySQLdb as mdb
import sys
import numpy as np
from optparse import OptionParser
import INC_config


###################################################


###################################################
def create_inputList(db, table_name):
  cur=db.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS `"+table_name+"` ( \
   `id` int(11) NOT NULL AUTO_INCREMENT, \
   `pgcID` varchar(7) COLLATE utf8_unicode_ci NOT NULL, \
   `note` varchar(80) COLLATE utf8_unicode_ci NOT NULL, \
   PRIMARY KEY (`id`) \
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;")
  db.commit()
###################################################
def checkTableExists(db, table_name):
    stmt = "SHOW TABLES LIKE '"+table_name+"'"
    cursor=db.cursor()
    cursor.execute(stmt)
    result = cursor.fetchone()
    if result:
        # there is a table named "tableName"
        return True
    else:
        # there are no tables named "tableName"
        return False
###################################################
###################################################
###################################################
###################################################
## MAIN
## MAIN
###################################################
###################################################
# Handling the Input Arguments
###################################################
input_list = 'example_bad_galaxie_dollor_separated.csv'
table_name = 'example_bad_galaxie'



###################################################
# MAIN
# connect to mysql database
try:
    db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)
    # accept empty values in integer columns
except:
    print "There was an error connecting to the database"
    exit(1)
###################################################

if checkTableExists(db, table_name):
    print '"'+table_name+'"'+" already exists. Choose another name, or Drop the existing one."
    exit(1)
###################################################
mytable = np.genfromtxt(input_list , delimiter='$', filling_values=None, names=True, dtype=None )
pgcs   = mytable['pgc']
notes  = mytable['note']

# create the input list
create_inputList(db, table_name)

data = []
for i in range(len(pgcs)): 
    data.append((pgcs[i],notes[i]))   
    
cur=db.cursor()
sql_command = "INSERT INTO "+table_name+" (pgcID, note) VALUES (%s, %s)"
cur.executemany(sql_command,data)
db.commit()
cur.close()


###################################################
print(" ")
print("table example_bad_galaxie created.")
print(" Done ... !  :)")
print(" ")


