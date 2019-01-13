from time import time
import sys
import os
import numpy as np
from math import *
import random 



#################################################################
def my_shuffle(array):
        random.seed(0)
        random.shuffle(array)
        return array
    
    
    

mytable = np.genfromtxt('Input_Grand_ALL.catal.online.hard' , delimiter=',', filling_values=None, names=True, dtype=None )
pgcs    = mytable['pgc']

indices = np.arange(len(pgcs))
indices = my_shuffle(indices)
pgcs = pgcs[indices]

for pgc in pgcs:
    
    print pgc




