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
import os.path
import subprocess
import math
import matplotlib.pyplot as plt
import matplotlib; matplotlib.pyplot.switch_backend('agg')
import numpy as np
import pylab as py
from astropy.table import Table, Column 
import time
import datetime
from bokeh.plotting import *
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, Range1d, Label, TapTool, OpenURL, CustomJS

import INC_config
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mdb




######################################
def addNote(note, text):
    
    if text=='': return note
    
    if note=='':
        note = '['+text+']'
    else:
        note = note+' '+'['+text+']'
    
    return note
    

def addConcern(note, cncrn):
    
    if cncrn[0]>0: note = addNote(note, 'not_sure')
    if cncrn[1]>0: note = addNote(note, 'better_image')
    if cncrn[2]>0: note = addNote(note, 'bad_TF')
    if cncrn[3]>0: note = addNote(note, 'ambiguous')
    if cncrn[4]>0: note = addNote(note, 'disturbed')
    if cncrn[5]>0: note = addNote(note, 'HI')
    if cncrn[6]>0: note = addNote(note, 'face_on')
    if cncrn[7]>0: note = addNote(note, 'not_spiral')
    if cncrn[8]>0: note = addNote(note, 'multiple')
    return note
######################################
#######################################
def getINC(exclude_Email=[]):
    
    db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)
    cur=db.cursor()
    
    
    #### Manoa
    query = "select pgcID,inc,flag,note,email,not_sure,better_image,bad_TF,ambiguous,disturbed,HI,face_on,not_spiral,multiple from Output_Manoa;"
    
    cur.execute(query)
    results=cur.fetchall()

    pgc_incout    = np.asarray([int(x[0]) for x in results])
    inc_incout    = np.asarray([float(x[1]) for x in results])
    flag_incout   = np.asarray([int(x[2]) for x in results])
    note          = np.asarray([x[3] for x in results])
    email         = np.asarray([x[4] for x in results])
    NS = np.asarray([x[5] for x in results])
    BI = np.asarray([x[6] for x in results])
    TF = np.asarray([x[7] for x in results])
    AM = np.asarray([x[8] for x in results])
    DI = np.asarray([x[9] for x in results])
    HI = np.asarray([x[10] for x in results])
    FO = np.asarray([x[11] for x in results])
    NP = np.asarray([x[12] for x in results])
    MU = np.asarray([x[13] for x in results])
    
    #### Guest
    query = "select pgcID,inc,flag,note,email,not_sure,better_image,bad_TF,ambiguous,disturbed,HI,face_on,not_spiral,multiple from Output_Guest;"
    
    cur.execute(query)
    results=cur.fetchall()

    pgc_incout_    = np.asarray([int(x[0]) for x in results])
    inc_incout_    = np.asarray([float(x[1]) for x in results])
    flag_incout_   = np.asarray([int(x[2]) for x in results])
    note_          = np.asarray([x[3] for x in results])
    email_         = np.asarray([x[4] for x in results])
    NS_ = np.asarray([x[5] for x in results])
    BI_ = np.asarray([x[6] for x in results])
    TF_ = np.asarray([x[7] for x in results])
    AM_ = np.asarray([x[8] for x in results])
    DI_ = np.asarray([x[9] for x in results])
    HI_ = np.asarray([x[10] for x in results])
    FO_ = np.asarray([x[11] for x in results])
    NP_ = np.asarray([x[12] for x in results])
    MU_ = np.asarray([x[13] for x in results])
    
    cur.close()
    
    #eMails = ['rbtully1@gmail.com','ekourkchi@gmail.com','s.eftekharzadeh@gmail.com']

    PGC = []
    for i in range(len(pgc_incout)):
        if not pgc_incout[i] in PGC:
            PGC.append(pgc_incout[i])
    for i in range(len(pgc_incout_)):
        if not pgc_incout_[i] in PGC:
            PGC.append(pgc_incout_[i])        
            
            
    incDict = {}
    for i in range(len(PGC)):   
        
        data = {}
        
        indx = np.where(PGC[i] == pgc_incout)
        for j in indx[0]:
            if not email[j] in data.keys() and not email[j] in exclude_Email:
                data[email[j]] = [inc_incout[j],flag_incout[j],note[j], [NS[j], BI[j], TF[j], AM[j], DI[j], HI[j], FO[j], NP[j], MU[j]]]

        indx = np.where(PGC[i] == pgc_incout_)
        for j in indx[0]:
            if not email_[j] in data.keys() and not email_[j] in exclude_Email:
                data[email_[j]] = [inc_incout_[j],flag_incout_[j],note_[j], [NS_[j], BI_[j], TF_[j], AM_[j], DI_[j], HI_[j], FO_[j], NP_[j], MU_[j]]]

        incDict[PGC[i]] = data
        
        
    return incDict   
###########################################################          
######################################
def incMedian(incDic):
    
    boss = 'rbtully1@gmail.com'
    #boss = 'ekourkchi@gmail.com'
    
    flag = 0
    inc  = 0
    note = ''
    stdev = 0
    n = 0   # number of good measurments
    concerns = np.zeros(9)
    
    if boss in incDic.keys():
        
        if incDic[boss][1] != 0:  # boss has flagged it
            
            flag = 1
            for email in incDic:
                if incDic[email][1]==1:
                   note =  addNote(note, incDic[email][2])
                   concerns+=np.asarray(incDic[email][3])
                   n+=1
        
        else:  # boss has NOT flagged it
            
            flag = 0
            incs = []
            for email in incDic:
                if incDic[email][1]==0:
                    incs.append(incDic[email][0])
                    note = addNote(note, incDic[email][2])
                    n+=1

            inc = np.median(incs)
            stdev = np.std(incs)
        
    else:
        flag = []
        for email in incDic:
            flag.append(incDic[email][1])
        flag = np.median(flag)
        if flag > 0: flag =1
        
        incs = []
        for email in incDic:
            if incDic[email][1]==flag:
               incs.append(incDic[email][0])
               note = addNote(note, incDic[email][2])
               concerns+=np.asarray(incDic[email][3])
               n+=1
        inc = np.median(incs)
        stdev = np.std(incs)
    
    note = addConcern(note, concerns)
    
    return inc, stdev, flag, note, n

#######################################


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

def get_ellipse(filename):
          
          ra_cen = -1
          dec_cen = -1
          semimajor = -1
          semiminor = -1
          PA = -1
          with open(filename) as f:
            counter = 1
            for line in f:
              if counter == 14:
                line_split = line.split(" ")
                not_void = 0 
                set_param = False
                for thing in line_split:
                  if thing != '': 
                      not_void+=1
                      set_param = True
                  if not_void==1 and set_param: 
                      set_param = False
                      ra_cen=np.float(thing) 
                  if not_void==2 and set_param: 
                      dec_cen=np.float(thing) 
                      set_param = False
                  if not_void==3 and set_param: 
                      semimajor=np.float(thing) 
                      set_param = False
                  if not_void==4 and set_param: 
                      semiminor=np.float(thing)
                      set_param = False
                  if not_void==5 and set_param: 
                      PA=np.float(thing) 
                      break
                return ra_cen, dec_cen, semimajor, semiminor, PA
              counter+=1   
#################################
def ra_db(ra):   # returns a string
  
     ra_id = str(int(np.floor(ra)))
     if ra < 10:
       ra_id = '00'+ra_id+'D'
     elif ra < 100:
       ra_id = '0'+ra_id+'D'
     else:
       ra_id = ra_id+'D'
  
     return ra_id
#################################
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
#################################



db=mdb.connect(INC_config.host,user=INC_config.user,passwd=INC_config.passwd,db=INC_config.database)
cur=db.cursor()

query = "select id, email, created, prj_group, first_name from users;"
cur.execute(query)
results=cur.fetchall()
ids = np.asarray([x[0] for x in results])
emails = np.asarray([x[1] for x in results])
created = np.asarray([x[2] for x in results])
prj_group = np.asarray([x[3] for x in results])
first_name = np.asarray([x[4] for x in results])
#######################################################

for pp in range(len(ids)):

    myEmail = emails[pp]
    print myEmail
    
    try:
        emailID = myEmail.split('@')[0]
    except:
        emailID = myEmail

    fname=str(ids[pp])+'_'+emailID+'_'+created[pp].strftime("%Y%m%d")+'_scatter.png'
    
    fname_bokeh=str(ids[pp])+'_'+emailID+'_'+created[pp].strftime("%Y%m%d")+'_scatter.plot.txt'


    query = "select pgcID,inc,flag,email from Output_Manoa;"
    cur.execute(query)
    results=cur.fetchall()

    pgc_incout_    = np.asarray([int(x[0]) for x in results])
    inc_incout_    = np.asarray([float(x[1]) for x in results])
    flag_incout_   = np.asarray([int(x[2]) for x in results])
    email_   = np.asarray([x[3] for x in results])


    pgc_incout = []
    inc_incout = []
    flag_incout = []

    pgc_incout_eval = []
    inc_incout_eval = []
    flag_incout_eval = []

    for i in range(len(pgc_incout_)):
        email_[i] = ' '.join(email_[i].split())
        if email_[i]== myEmail:
            
            pgc_incout.append(pgc_incout_[i])
            inc_incout.append(inc_incout_[i])
            flag_incout.append(flag_incout_[i])
            
            
    query = "select pgcID,inc,flag,email,inputTable from Output_Guest;"
    cur.execute(query)
    results=cur.fetchall()

    pgc_incout_    = np.asarray([int(x[0]) for x in results])
    inc_incout_    = np.asarray([float(x[1]) for x in results])
    flag_incout_   = np.asarray([int(x[2]) for x in results])
    email_   = np.asarray([x[3] for x in results])
    inputTable   = np.asarray([x[4] for x in results])

    pq = 0
    for i in range(len(pgc_incout_)):
        email_[i] = ' '.join(email_[i].split())
        if email_[i]== myEmail:
            
            pgc_incout.append(pgc_incout_[i])
            inc_incout.append(inc_incout_[i])
            flag_incout.append(flag_incout_[i])  
            
            if  ' '.join(inputTable[i].split()) == 'Input_Guest_test_calib':
                pgc_incout_eval.append(pgc_incout_[i])
                inc_incout_eval.append(inc_incout_[i])
                flag_incout_eval.append(flag_incout_[i])             
                
            if  ' '.join(inputTable[i].split()) == 'Input_Guest':
                pq+=1
            
            


    pgc_incout = np.asarray(pgc_incout)
    inc_incout = np.asarray(inc_incout)
    flag_incout = np.asarray(flag_incout)

    pgc_incout_eval = np.asarray(pgc_incout_eval)
    inc_incout_eval = np.asarray(inc_incout_eval)
    flag_incout_eval = np.asarray(flag_incout_eval)


    incDic = getINC(exclude_Email=myEmail)


    pgc_common = []
    my_inc     = []
    th_inc     = []  # median

    pgc_common_eval = []
    my_inc_eval     = []
    th_inc_eval    = []  # median


    for i in range(len(pgc_incout)):
        
        inc, stdev, flag, note, n = incMedian(incDic[pgc_incout[i]])        
        if flag_incout[i]==0 and flag==0 and n>=1:

            my_inc.append(inc_incout[i])
            pgc_common.append(pgc_incout[i])
            th_inc.append(inc)
            
            if pgc_incout[i] in pgc_incout_eval:
                my_inc_eval.append(inc_incout[i])
                pgc_common_eval.append(pgc_incout[i])
                th_inc_eval.append(inc)               
            

    fig, ax = plt.subplots()  

    if (prj_group[pp]=="Manoa" or len(th_inc)>100):
        ax.plot(th_inc, my_inc, 'g.', alpha=0.3)
    else:
        ax.plot(th_inc, my_inc, 'o', mfc='white', alpha=1.0, color='green')
        ax.plot(th_inc_eval, my_inc_eval, 'g.', alpha=1.0,  markersize=10)

    p1, = ax.plot([0,100], [0,100], color='black', linestyle='-', label="equality")
    p2, = ax.plot([0,100], [5,105], color='b', linestyle=':', label=r'$\pm5^o$')
    ax.plot([0,100], [-5,95], color='b', linestyle=':')
    p3, = ax.plot([0,100], [10,110], color='r', linestyle='--', label=r'$\pm10^o$')
    ax.plot([0,100], [-10,90], color='r', linestyle='--')



    pgc_common = np.asarray(pgc_common)
    th_inc_ = np.asarray(th_inc)
    my_inc_ = np.asarray(my_inc)

    N = len(th_inc_)
    a1 = np.zeros(N)
    a2 = np.zeros(N)


    a1[np.where(th_inc_<80)] = 1
    a2[np.where(th_inc_>60)] = 1
    a = a1 + a2

    index = np.where(a==2)
    th_inc_ = th_inc_[index]
    my_inc_ = my_inc_[index]

    delta = th_inc_-my_inc_
    std = np.std(delta)
    rms = np.sqrt(np.mean(delta**2))

    ax.set_xlim([20,100])
    ax.set_ylim([20,100])
    ax.text(23,80, r'$RMS: $'+"%.1f" % (rms)+r'$^o$')

    ax.set_xlabel('Inclination [deg]', fontsize=14)
    ax.set_ylabel('Inclination [deg]', fontsize=14)
    ax.text(70,30, first_name[pp], size=11, color='green')

    ax.tick_params(which='major', length=5, width=2.0, direction='in')
    ax.tick_params(which='minor', length=2, color='#000033', width=1.0, direction='in')
    ax.minorticks_on()

    # Legend
    lns = [p1, p2, p3]
    ax.legend(handles=lns, loc='best')

    date = datetime.date.today().strftime("%B")+" "+datetime.date.today().strftime("%d")+", "+datetime.date.today().strftime("%Y")

    hstTime =  time.strftime("%H")

    ax.set_title("Last update: "+date+' '+hstTime+ ':00 HST')
    

    plt.savefig(fname)
    plt.close(fig)    # close the figure
    
    #################################
    ### Bokeh 
    #################################
    

    hover = HoverTool(tooltips=[ 
        ("inc_x", "@inc_x"),
        ("inc_y", "@inc_y"),
        ("PGC", "@PGC"),
        ])

    hover.point_policy='snap_to_data'
    hover.line_policy='nearest'#'prev'

    TOOLS = [hover, 'pan', 'tap', 'wheel_zoom', 'box_zoom', 'reset', 'save']

    p = figure(tools=TOOLS, toolbar_location="below", plot_width=450, plot_height=350, title="Last update: "+date+' '+hstTime+ ':00 HST')

    p.grid.grid_line_color="gainsboro"
        
    p.line([0,100], [0,100], line_width=2, color="black", legend="equality")
    p.line([0,100], [5,105], line_width=1, color="blue", legend='-/+5 deg', line_dash='dotted')
    p.line([0,100], [-5,95], line_width=1, color="blue", line_dash='dotted')
    p.line([0,100], [10,110], line_width=1, color="red", legend='-/+10 deg', line_dash='dashed')
    p.line([0,100], [-10,90], line_width=1, color="red", line_dash='dashed')

    source = ColumnDataSource({'inc_x': th_inc, 'inc_y': my_inc, 'PGC': pgc_common})
    render = p.circle('inc_x', 'inc_y', source=source, size=5, color="green", alpha=0.3, hover_color="orange", hover_alpha=1, hover_line_color='red',
                    
                    # set visual properties for selected glyphs
                    selection_fill_color="pink",

                    # set visual properties for non-selected glyphs
                    nonselection_fill_alpha=0.2,
                    nonselection_fill_color="green",
                    
                    )

    mytext = Label(x=70, y=45, text='RMS: '+"%.1f" % (rms)+' deg')
    p.add_layout(mytext)

    mytext = Label(x=70, y=40, text='User: ' + first_name[pp], text_color='green')
    p.add_layout(mytext)


    p.legend.location = "top_left"
    p.x_range = Range1d(35, 95)
    p.y_range = Range1d(35, 95)

    p.xaxis.axis_label = 'Inclination [deg]'
    p.yaxis.axis_label = 'Inclination [deg]'


    #url = "http://edd.ifa.hawaii.edu/cf4_photometry/get_sdss_cf4.php?pgc=@PGC"
    #taptool = p.select(type=TapTool)
    #taptool.callback = OpenURL(url=url)

    render.selection_glyph.line_width = 5


    code = """
        
        var index_selected = source.selected['1d']['indices'][0];
        var win = window.open("http://edd.ifa.hawaii.edu/cf4_photometry/get_sdss_cf4.php?pgc="+source.data['PGC'][index_selected]+"#t01", "EDDesn", "width=800, height=700");
        try {win.focus();} catch (e){}

    """

    taptool = p.select(type=TapTool)
    taptool.callback = CustomJS(args=dict(source=source), code=code)
    
    script, div = components(p)
    script = '\n'.join(['' + line for line in script.split('\n')])
    
    
    with open(fname_bokeh, "w") as text_file:
        text_file.write(div)
        text_file.write(script)    

    


