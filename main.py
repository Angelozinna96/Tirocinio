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

if len(sys.argv)>1:
  _data=sys.argv[1]
else:
  #_data="2018-07-23"
  _data=datetime.now().strftime('%Y-%m-%d')
data=_data.split("-")[0]+_data.split("-")[1]+_data.split("-")[2]

obj=EstrazioneH5(data=data,rang=0,tip='VIIRS-Day-Night-Band-SDR-Ellipsoid-Geo',dir_base="./",lat=37.755,lon=15)
obj.secureFind(data)
