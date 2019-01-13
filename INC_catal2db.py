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

def arg_parser():
    parser = OptionParser(usage="""\
\n
 - Ingesting the Input catalog into the Data-Base 
 - The input list has at least one columns, i.e. "pgc" as the header

 - How to run: 
 
    $ python %prog -i [<input_list> , e.g. pgc_ehsan_calib.lst] -t [<table_name> , e.g. Input_ehsan_calib]
    $ python %prog -h 
      To see help and all available options.
 
 - Author: "Ehsan Kourkchi"
 - Copyright Frbruary 2018

""")
    

    parser.add_option("-i", "--input",
                      type='string', action='store',
                      help="""The input list""") 

    parser.add_option("-t", "--table",
                      type='string', action='store',
                      help="""Table name to be created in the Database""")    
    
    (opts, args) = parser.parse_args()
    return opts, args
########

###################################################
def create_inputList(db, table_name):
  cur=db.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS `"+table_name+"` ( \
   `id` int(11) NOT NULL AUTO_INCREMENT, \
   `pgcID` varchar(7) COLLATE utf8_unicode_ci NOT NULL, \
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
opts, args =  arg_parser()
input_list = opts.input
table_name = opts.table
print "Input List      : ", input_list
print "Table Name      : ", table_name
if None in [input_list, table_name]:
       print "\nNot enough input arguments ..."
       print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" for help ...  \n"
       sys.exit(1)


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
mytable = np.genfromtxt(input_list , delimiter=',', filling_values=None, names=True, dtype=None )
pgcs    = mytable['pgc']


# create the input list
create_inputList(db, table_name)

data = []
for pgc in pgcs: 
    data.append((pgc))   # default values: dPA=0 and zoom=1
    
cur=db.cursor()
sql_command = "INSERT INTO "+table_name+" (pgcID) VALUES (%s)"
cur.executemany(sql_command,data)
db.commit()
cur.close()


###################################################
print(" ")
print(" Done ... !  :)")
print(" ")


