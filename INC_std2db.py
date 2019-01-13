# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  Creation DATE:	February, 21, 2018         
# //
# //  Description:      + Generating table for Inclination Standard Galaxies
# //                    x Updating the Standard Scale table, that holds the initial image scaling parameters
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
 - Ingesting the inclination of the standard galaxies into the database. 
 - The input list has at least two columns, i.e. "pgc" and "inc" as the header

 - How to run: 
 
    $ python %prog -s [<standard_list> , e.g. std.73.lst] -t [<table_name> , e.g. Standards]
    $ python %prog -h 
      To see help and all available options.
 
 - Author: "Ehsan Kourkchi"
 - Copyright Frbruary 2018

""")
    

    parser.add_option("-s", "--standards",
                      type='string', action='store',
                      help="""The list of standards""") 
    
    parser.add_option("-t", "--table",
                      type='string', action='store',
                      help="""Standard Table name to be created in the Database""")       
    
    (opts, args) = parser.parse_args()
    return opts, args
########



###################################################
def create_Standards(db, table_name):
  cur=db.cursor()
  cur.execute("CREATE TABLE `"+table_name+"` ( \
   `id` int(11) NOT NULL AUTO_INCREMENT, \
   `pgcID` varchar(7) COLLATE utf8_unicode_ci NOT NULL, \
   `inc` numeric(6,2) NOT NULL, \
   PRIMARY KEY (`id`) \
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;")
  db.commit()
###################################################
def create_STDscales(db):
  cur=db.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS `STDscales` ( \
   `id` int(11) NOT NULL AUTO_INCREMENT, \
   `pgcID` varchar(7) COLLATE utf8_unicode_ci NOT NULL, \
   `dPA` numeric(10,5) NOT NULL, \
   `zoom` numeric(10,5) NOT NULL, \
   PRIMARY KEY (`id`) \
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;")
  db.commit()
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
standard_file = opts.standards
table_name = opts.table
print "Standard List Name           : ", standard_file
print "Standard Database Table Name : ", table_name
if None in [standard_file, table_name]:
       print "\nNot enough input arguments ..."
       print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" for help ...  \n"
       sys.exit(1)

###################################################
###################################################
# MAIN
# connect to mysql database
try:
    db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)
    # accept empty values in integer columns
except:
    print "There was an error connecting to the database"
    exit(1)

cur=db.cursor()    
cur.execute("DROP TABLE IF EXISTS "+table_name+";")
cur.close()


# create the Standard table
create_Standards(db, table_name)


#inFile = 'std.73.lst'
mytable = np.genfromtxt(standard_file , delimiter=',', filling_values=None, names=True, dtype=None )
pgcs    = mytable['pgc']
incs    = mytable['inc']

print "generating "+table_name+" table ..."

data = []
for pgc, inc in zip(pgcs, incs): 
    data.append((pgc,inc))


cur=db.cursor()
sql_command = "INSERT INTO "+table_name+" (pgcID, inc) VALUES (%s, %s)"
cur.executemany(sql_command,data)
db.commit()
cur.close()

###################################################
## Taking care of the Scale table
###################################################

create_STDscales(db)


cur=db.cursor()    
cur.execute("select pgcID from "+table_name+" where pgcID not in (SELECT pgcID FROM STDscales);")
missing_pgc = cur.fetchall()
cur.close()

missing_pgc = [x[0] for x in missing_pgc]

data = []
for pgc in missing_pgc: 
    data.append((pgc,0,1))   # default values: dPA=0 and zoom=1


cur=db.cursor()
sql_command = "INSERT INTO STDscales (pgcID, dPA, zoom) VALUES (%s, %s, %s)"
cur.executemany(sql_command,data)
db.commit()
cur.close()

###################################################
print(" ")
print(" Done ... !  :)")
print(" ")





