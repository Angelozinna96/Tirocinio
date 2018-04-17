#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:03:06 2018

@author: angelozinna
"""

from ftplib import FTP
import xml.etree.ElementTree as ET
data_search="20180417"
ftp=FTP('ftp-npp.class.ngdc.noaa.gov')
ftp.login()
all_file =[]

ftp.cwd(data_search+'/VIIRS-SDR/VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo/NPP/')
res=ftp.retrlines('NLST',all_file.append)
print res
for name in all_file:
    if name.find("xml"):
        ftp.retrbinary('RETR README', open('/Users/angelozinna/Desktop/università/3anno/tirocinio/dati/python', 'wb').write)

ftp.quit()