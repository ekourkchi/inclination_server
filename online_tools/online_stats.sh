#!/bin/bash

## Using Anaconda 2
export PATH=/home/opik/distance/yes/bin:$PATH


while true; do
    
    python geoscatter.py
    python personal_time.py
    python personal_progress.py
    python personal_scatter.py
    python donwload_db.py

    cp *.png /home/huchra/distance/public_html/inclination/stats/.
    cp *.plot.txt /home/huchra/distance/public_html/inclination/stats/.

	sleep 1h



done


