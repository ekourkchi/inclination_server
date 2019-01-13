#!/usr/bin/python
import sys
import os
import os.path
import subprocess
import math
import numpy as np
######################################
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
 
######################################
######################################
def xcmd(cmd,verbose):

  if verbose: print '\n'+cmd

  tmp=os.popen(cmd)
  output=''
  for x in tmp: output+=x
  if 'abort' in output:
    failure=True
  else:
    failure=tmp.close()
  if False:
    print 'execution of %s failed' % cmd
    print 'error is as follows',output
    sys.exit()
  else:
    return output

######################################

inFile = '/home/opik/distance/INCLINATION_tools/std_modified.lst'
table = np.genfromtxt(inFile , delimiter=',', filling_values=None, names=True, dtype=None)
pgc  = table['pgc']
inc = table['inc']

for i in range(0, len(pgc)):
    
    cmd = 'cp galaxies.back/pgc'+str(pgc[i])+'*  galaxies/.'
    xcmd(cmd, True)
















