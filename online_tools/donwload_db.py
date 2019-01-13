# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  Creation DATE:	June, 10, 2018         
# //
# //  Description:      + Downloading Info from the db
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
import matplotlib.patches as patches
import matplotlib; matplotlib.pyplot.switch_backend('agg')
import numpy as np
from astropy.table import Table, Column 
import pylab as py
import time
import datetime

from bokeh.plotting import *
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, Range1d, Label, TapTool, OpenURL, CustomJS
import INC_config
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mdb



#######################################
def add_time(myDict, dtime):
    
    date = dtime.strftime('%Y-%m-%d')
    if date in myDict:
        myDict[date]+=1
    else:
        myDict[date] = 1
#######################################
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
#######################################
#######################################
def time_serie(myDict, window=3, start=None):
    
    day_lst = []
    for key in myDict:
        a = ''
        for st in key.split('-'): a+=st
        day_lst.append(int(a))


    day_lst = np.sort(day_lst)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    
    if start is None:
        begin_day = datetime.datetime.strptime(str(day_lst[0]), "%Y%m%d")
    else: 
        begin_day = datetime.datetime.strptime(start, "%Y-%m-%d")

    current_day = begin_day.strftime('%Y-%m-%d')

    days = []
    days_string = []
    numbers = []

    while current_day!=tomorrow:
        
        c0 = datetime.datetime.strptime(current_day, "%Y-%m-%d")
        
        if current_day in myDict:
            days.append(c0)
            days_string.append(c0.strftime('%Y-%m-%d'))
            numbers.append(myDict[current_day])
        else: 
            days.append(c0)
            days_string.append(c0.strftime('%Y-%m-%d'))
            numbers.append(0)
        
        c =  c0 + datetime.timedelta(days=1)
        current_day = c.strftime('%Y-%m-%d')

    numbers = smooth(numbers, window)
    for i in range(len(numbers)): numbers[i]=int(numbers[i])
    
    return days, numbers, days_string
#######################################



db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)

cur=db.cursor()


query = "SELECT pgcID, checkinTime FROM Output_Manoa ORDER BY id DESC ;"
cur.execute(query)
results=cur.fetchall()
pgcID1 = np.asarray([int(x[0]) for x in results])
checkinTime1 = np.asarray([x[1] for x in results])


query = "SELECT pgcID, checkinTime, email, inputTable FROM Output_Guest ORDER BY id DESC ;"
cur.execute(query)
results=cur.fetchall()
pgcID2 = np.asarray([int(x[0]) for x in results])
checkinTime2 = np.asarray([x[1] for x in results])
email2 = np.asarray([x[2] for x in results])
inputTable2 = np.asarray([x[3] for x in results])

cur.close()


#######################################################

myDict = dict()
for i in range(len(pgcID1)):
    add_time(myDict, checkinTime1[i])
for i in range(len(pgcID2)):
    add_time(myDict, checkinTime2[i])

days, numbers, days_string = time_serie(myDict, window=3)


myDict_ = dict()
for i in range(len(pgcID2)):
    add_time(myDict_, checkinTime2[i])

days_, numbers_, days_string_ = time_serie(myDict_, window=3, start="2018-05-01")

fig, ax = plt.subplots()

# plot
p1, = ax.plot(days, numbers, label="Everybody")
#p2, = ax.plot(days_, numbers_, label="Amateurs")

plt.gcf().autofmt_xdate()

ax.set_ylabel("No. of galaxies", fontsize=12)
ax.set_xlabel("Date", fontsize=12)

date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")

hstTime =  time.strftime("%H")

ax.set_title("Last update: "+date+' '+hstTime+ ':00 HST')

# Legend
#lns = [p1, p2]
#ax.legend(handles=lns, loc='best')

#mpld3.show(fig)


ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='--', linewidth=1)
ax.xaxis.grid(color='gray', linestyle='--', linewidth=1)

plt.savefig('time_stats.png')
plt.close(fig)    # close the figure



### new Bokeh
hover = HoverTool(tooltips=[ 
    ("Date", "@days_string"),
    ("# of galaxies", "@numbers"),
    ])

TOOLS = [hover,'pan', 'tap', 'wheel_zoom', 'box_zoom', 'reset', 'save']

p = figure(tools=TOOLS, toolbar_location="below", plot_width=450, plot_height=350, x_axis_type="datetime", title="Last update: "+date+' '+hstTime+ ':00 HST')

p.background_fill_color = "beige"
p.grid.grid_line_color="gainsboro"

# plot
source = ColumnDataSource({'days':days, 'numbers':numbers, 'days_string':days_string})
p.line('days', 'numbers', source=source, line_width=2, color="blue", alpha=0.5)

#source = ColumnDataSource({'days':days_, 'numbers':numbers_, 'days_string':days_string_})
#p.line('days', 'numbers', source=source, line_width=2, color="red", alpha=0.5, legend="Amateurs")

#p.legend.location = "top_left"


p.yaxis.axis_label = "No. of galaxies"
p.yaxis.axis_label_text_color = "black"
p.yaxis.axis_label_text_font_size = "14pt"


p.xaxis.axis_label = "Date"
p.xaxis.axis_label_text_color = "black"
p.xaxis.axis_label_text_font_size = "14pt"

script, div = components(p)
script = '\n'.join(['' + line for line in script.split('\n')])

with open("time_stats.plot.txt", "w") as text_file:
    text_file.write(div)
    text_file.write(script)


#######################################################

inFile  = 'EDD_distance_cf4_v23.csv'
table   = np.genfromtxt(inFile , delimiter='|', filling_values=-1, names=True, dtype=None)
pgc = table['pgc']
inc     = table['inc']
inc_e   = table['inc_e']
inc_flg = table['inc_flg']
inc_n   = table['inc_n']

pgcID = np.concatenate((pgcID1, pgcID2))

Na = len(pgc)
N3 = 0
N2 = 0
N1 = 0
N4 = 0 
N5 = 0

N0 = 0
for i in range(len(pgc)):
    
    if inc_flg[i]>0: N0+=1
    

for i in range(Na):
    
    if pgc[i] in pgcID:
        ind = np.where(pgcID==pgc[i])
        N =  len(ind[0])
        
        if N>=5: N5+=1
        if N>=4: N4+=1
        if N>=3: N3+=1
        if N>=2: N2+=1
        if N>=1: N1+=1
        
fig, ax = plt.subplots()

ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='--', linewidth=1)

ax.add_patch(patches.Rectangle((0.5,Na-N0), 6, N0, color='black', alpha=0.2, linewidth=0))


rects1 = ax.bar([1], [Na], 0.5, color='blue')
rects2 = ax.bar([2], [N1], 0.5, color='red')
rects2 = ax.bar([3], [N2], 0.5, color='orange')
rects2 = ax.bar([4], [N3], 0.5, color='green')
rects2 = ax.bar([5], [N4], 0.5, color='dodgerblue')
rects2 = ax.bar([6], [N5], 0.5, color='darkorchid')

ax.annotate("%d"% (100.*N1/Na)+"%",(1.75,N1-1200), fontsize=10)
ax.annotate("%d"% (100.*N2/Na)+"%",(2.80,N2-1200), fontsize=12)
ax.annotate("%d"% (100.*N3/Na)+"%",(3.80,N3-1200), fontsize=12)
ax.annotate("%d"% (100.*N4/Na)+"%",(4.80,N4-1200), fontsize=12)
ax.annotate("%d"% (100.*N5/Na)+"%",(5.80,N5-1200), fontsize=12)

ax.annotate("Rejected Galaxies",(4, 18000), fontsize=14, color='gray')

ax.tick_params(bottom='off')
#py.setp(ax.get_xticklabels(), visible=False)
ax.set_xticks(range(1,7))
ax.set_xticklabels(['Total','N1','N2','N3', 'N4', 'N5'], fontsize=12)

ax.set_ylim([0, 20000])
ax.set_ylabel("No. of galaxies", fontsize=12)

ax.set_title("Last update: "+date+' '+hstTime+ ':00 HST')

plt.savefig('histo_stats.png')
plt.close(fig)    # close the figure

############# Bokeh
hover = HoverTool(tooltips=[ 
    ("# of galaxies", "@numbers"),
    ])  
        
        
TOOLS = [hover, 'save']

fruits = ['Total', 'N1', 'N2', 'N3', 'N4', 'N5']

p = figure(x_range=fruits, tools=TOOLS, toolbar_location="below",plot_width=450, plot_height=350, title="Last update: "+date)

source = ColumnDataSource(data=dict(top=[Na], bottom=[Na-N0], left=[0.5], right=[6.5], numbers=[N0]))
p.quad(top='top', bottom='bottom', left='left', right='right', color="black", alpha=0.2, source=source)

f = ['Total']
source = ColumnDataSource(data=dict(f=f, numbers=[Na]))
p.vbar(x='f', top='numbers', width=0.5, color='blue', alpha=0.95, source=source)

f = ['N1']
source = ColumnDataSource(data=dict(f=f, numbers=[N1]))
p.vbar(x='f', top='numbers', width=0.5, color='red', alpha=0.95, source=source)

f = ['N2']
source = ColumnDataSource(data=dict(f=f, numbers=[N2]))
p.vbar(x='f', top='numbers', width=0.5, color='orange', alpha=0.95, source=source)

f = ['N3']
source = ColumnDataSource(data=dict(f=f, numbers=[N3]))
p.vbar(x='f', top='numbers', width=0.5, color='green', alpha=0.95, source=source)

f = ['N4']
source = ColumnDataSource(data=dict(f=f, numbers=[N4]))
p.vbar(x='f', top='numbers', width=0.5, color='dodgerblue', alpha=0.95, source=source)

f = ['N5']
source = ColumnDataSource(data=dict(f=f, numbers=[N5]))
p.vbar(x='f', top='numbers', width=0.5, color='darkorchid', alpha=0.95, source=source)

p.xgrid.grid_line_color = "grey"
p.ygrid.grid_line_color = "grey"

p.y_range.start = 0
p.yaxis.axis_label = 'No. of galaxies'
p.yaxis.axis_label_text_font_size = "14pt"

p.xaxis.axis_label = 'No. of measurements'
p.xaxis.axis_label_text_font_size = "14pt"
p.xaxis.major_label_text_font = "18pt"


mytext = Label(x=1.27, y=N1-1500, text="%d"% (100.*N1/Na)+"%", text_color='black', text_font_size='10pt')
p.add_layout(mytext)

mytext = Label(x=2.27, y=N2-1500, text="%d"% (100.*N2/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=3.27, y=N3-1500, text="%d"% (100.*N3/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=4.27, y=N4-1500, text="%d"% (100.*N4/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=5.27, y=N5-1500, text="%d"% (100.*N5/Na)+"%", text_color='black', text_font_size='11pt')
p.add_layout(mytext)

mytext = Label(x=3, y=17000, text="Rejected Galaxies", text_color='gray', text_font_size='14pt')
p.add_layout(mytext)

script, div = components(p)
script = '\n'.join(['' + line for line in script.split('\n')])

with open("histo_stats.plot.txt", "w") as text_file:
    text_file.write(div)
    text_file.write(script)

print date+' '+hstTime+ ' HST'







