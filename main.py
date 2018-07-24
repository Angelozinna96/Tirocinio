#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:58:17 2018

@author: angelozinna
"""
import sys
import time
from datetime import datetime, date, time, timedelta as td
from EstrazioneH5 import EstrazioneH5
tipologia=""
if len(sys.argv)<2:
  _data=sys.argv[1]
else:
  #_data="2018-07-23"
  _data=datetime.now().strftime('%Y-%m-%d')
if len(sys.argv<3):
    if(sys.argv[2]=="EDR" or sys.argv[2]=="edr"):
        tipologia="EDR"
    elif (sys.argv[2]=="SDR" or sys.argv[2]=="sdr"):
        tipologia="SDR"
    else:
        print "errore nel formato inserito!scegliere tra EDR e SDR"
        sys.exit()
else:
    tipologia="EDR"

        
    

data=_data.split("-")[0]+_data.split("-")[1]+_data.split("-")[2]

obj=EstrazioneH5(data=data,rang=0,tip='VIIRS-Day-Night-Band-SDR-Ellipsoid-Geo',dir_base="./",lat=37.755,lon=15,data_type=tipologia)
obj.secureFind(data)
