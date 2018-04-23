#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:03:06 2018

@author: angelozinna
"""

from ftplib import FTP
import os
data_search="20180420"
tipologia_file='VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo'
dir_ftp=data_search+'/VIIRS-SDR/'+tipologia_file+'/NPP/'
all_file =[]
all_file_descr=[]


#connessione ftp
ftp=FTP('ftp-npp.class.ngdc.noaa.gov')
ftp.login()
ftp.cwd(dir_ftp)
#download della lista dei file nella directory dir_ftp
res_ftp=ftp.retrlines('NLST',all_file.append)
ftp.retrlines('MLSD',all_file_descr.append)
print res_ftp
print all_file

res_ftp=res_ftp.split(' ')
num_el_xml=int(res_ftp[1])/2
print "num_file xml=%d"% num_el_xml

#dir di base dove salvare i file
dir_base='/Users/angelozinna/Desktop/università/3anno/tirocinio/dati/python/'
#creazione cartella della data
dir_finale=dir_base+data_search+'/'+tipologia_file+"/xml"
if not os.path.exists(dir_finale):
    os.makedirs(dir_finale)
dir_finale=dir_finale+'/'



#ricerca e download dei file xml
import os       

try:
    for name in all_file:
        if name.find("xml")!=-1:
            new_file=open(dir_finale+name, 'wb')
            ftp.retrbinary('RETR '+name, new_file.write)
            new_file.close()
            print 'download complete:'+name
            
    ftp.quit()
except:
    print('Error during download from FTP')


#prelevamento info dall'xml
    
import xml.etree.ElementTree as ET 
id_buoni=[]
for name in all_file:
    if name.find("xml")!=-1:
        tree = ET.parse(dir_finale+name)
        root = tree.getroot()
        #num di granuli presenti nel tar
        num_granuli=int(root.findall('TarFileCount')[0].text)
        for i,dataset in enumerate(root.findall('Dataset')):
            nomefile=(dataset.find('FileName').text)
            #visualizzazione orario
            ore_inizio=nomefile[i].split('_')[3][1:5]
            ore_fine=nomefile[i].split('_')[4][1:5]
            #ricerca per orario dei granuli
            if ore_inizio[:2]=="12":
                #salvataggio degli id buoni da utilizzare per scaricare i rispettivi file tar
                id_buoni.append(name.split('.')[0].split('_')[3])
                print ore_inizio, ore_fine   
id_buoni=list(set(id_buoni))


                
                
                
