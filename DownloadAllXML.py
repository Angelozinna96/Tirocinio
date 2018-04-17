#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:03:06 2018

@author: angelozinna
"""

from ftplib import FTP
import xml.etree.ElementTree as ET
import os
data_search="20180416"
all_file =[]
tipologia_file='VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo'
dir_ftp=data_search+'/VIIRS-SDR/'+tipologia_file+'/NPP/'

#connessione ftp
ftp=FTP('ftp-npp.class.ngdc.noaa.gov')
ftp.login()
ftp.cwd(dir_ftp)
#download della lista dei file nella directory dir_ftp
res=ftp.retrlines('NLST',all_file.append)
print res
#dir di base dove salvare i file
directory_base='/Users/angelozinna/Desktop/università/3anno/tirocinio/dati/python/'
#creazione cartella della data
dir_finale=directory_base+data_search+'/'+tipologia_file+"/xml"
if not os.path.exists(dir_finale):
    os.makedirs(dir_finale)
dir_finale=dir_finale+'/'
#ricerca e download dei file xml
for name in all_file:
    if name.find("xml")!=-1:
        new_file=open(dir_finale+name, 'wb')
        ftp.retrbinary('RETR '+name, new_file.write)
        new_file.close()

ftp.quit()