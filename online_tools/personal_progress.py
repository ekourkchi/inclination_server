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
        try:
            begin_day = datetime.datetime.strptime(str(day_lst[0]), "%Y%m%d")
        except:
            start="2018-05-01"
            begin_day = datetime.datetime.strptime(start, "%Y-%m-%d")
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

    #numbers = smooth(numbers, window)
    for i in range(len(numbers)): numbers[i]=int(numbers[i])
    
    return days, numbers, days_string
#######################################


db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)

cur=db.cursor()


query = "SELECT pgcID, checkinTime, email, inputTable FROM Output_Manoa ORDER BY id DESC ;"
cur.execute(query)
results=cur.fetchall()
pgcID1 = np.asarray([int(x[0]) for x in results])
checkinTime1 = np.asarray([x[1] for x in results])
email1 = np.asarray([x[2] for x in results])
inputTable1 = np.asarray([x[3] for x in results])

query = "SELECT pgcID, checkinTime, email, inputTable FROM Output_Guest ORDER BY id DESC ;"
cur.execute(query)
results=cur.fetchall()
pgcID2 = np.asarray([int(x[0]) for x in results])
checkinTime2 = np.asarray([x[1] for x in results])
email2 = np.asarray([x[2] for x in results])
inputTable2 = np.asarray([x[3] for x in results])

query = "select id, email, created, first_name from users;"
cur.execute(query)
results=cur.fetchall()
ids = np.asarray([x[0] for x in results])
emails = np.asarray([x[1] for x in results])
created = np.asarray([x[2] for x in results])
first_name = np.asarray([x[3] for x in results])

cur.close()
#######################################################

for pp in range(len(ids)):

    myEmail = emails[pp]
    
    try:
        emailID = myEmail.split('@')[0]
    except:
        emailID = myEmail

    fname=str(ids[pp])+'_'+emailID+'_'+created[pp].strftime("%Y%m%d")+'.png'
    
    fname_bokeh=str(ids[pp])+'_'+emailID+'_'+created[pp].strftime("%Y%m%d")+'.plot.txt'

    myDict = dict()
    for i in range(len(pgcID1)):
        if email1[i]==myEmail:
            add_time(myDict, checkinTime1[i])
    for i in range(len(pgcID2)):
        if email2[i]==myEmail:
            add_time(myDict, checkinTime2[i])

    days, numbers, days_string = time_serie(myDict, window=3)



    fig, ax = plt.subplots()

    # plot
    p1, = ax.plot(days, numbers, label=first_name[pp], color='green')

    plt.gcf().autofmt_xdate()

    ax.set_ylabel("No. of galaxies", fontsize=12)
    ax.set_xlabel("Date", fontsize=12)

    date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")

    hstTime =  time.strftime("%H")

    ax.set_title("Last update: "+date+' '+hstTime+ ':00 HST')

    # Legend
    lns = [p1]
    ax.legend(handles=lns, loc='best')

    #mpld3.show(fig)



    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='--', linewidth=1)
    ax.xaxis.grid(color='gray', linestyle='--', linewidth=1)

    plt.savefig(fname)
    plt.close(fig)    # close the figure

    
    #################################
    ### Bokeh 
    #################################
    hover = HoverTool(tooltips=[ 
        ("Date", "@days_string"),
        ("# of galaxies", "@numbers"),
        ])

    TOOLS = [hover,'pan', 'tap', 'wheel_zoom', 'box_zoom', 'reset', 'save']

    p = figure(tools=TOOLS, toolbar_location="below", plot_width=450, plot_height=350, x_axis_type="datetime", title="Last update: "+date+' '+hstTime+ ':00 HST')

    #p.background_fill_color = "beige"
    p.grid.grid_line_color="gainsboro"

    # plot
    source = ColumnDataSource({'days':days, 'numbers':numbers, 'days_string':days_string})
    p.line('days', 'numbers', source=source, line_width=2, color="green", alpha=0.5, legend=first_name[pp])


    p.legend.location = "top_left"


    p.yaxis.axis_label = "No. of galaxies"
    p.yaxis.axis_label_text_color = "black"
    p.yaxis.axis_label_text_font_size = "14pt"


    p.xaxis.axis_label = "Date"
    p.xaxis.axis_label_text_color = "black"
    p.xaxis.axis_label_text_font_size = "14pt"

    script, div = components(p)
    script = '\n'.join(['' + line for line in script.split('\n')])

    with open(fname_bokeh, "w") as text_file:
        text_file.write(div)
        text_file.write(script)    
    






















