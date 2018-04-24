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
print all_file_descr

res_ftp=res_ftp.split(' ')
num_el_xml=int(res_ftp[1])/2
print "num_file xml=%d"% num_el_xml

#dir di base dove salvare i file
dir_base='/Users/angelozinna/Desktop/università/3anno/tirocinio/dati/python/'
#creazione cartelle della data , xml e h5
dir_finale=dir_base+data_search+'/'+tipologia_file+"/xml"
dir_finale_h5=dir_base+data_search+'/'+tipologia_file+"/h5"
if not os.path.exists(dir_finale):
    os.makedirs(dir_finale)
if not os.path.exists(dir_finale_h5):
    os.makedirs(dir_finale_h5)
dir_finale=dir_finale+'/'
dir_finale_h5+='/'



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
tar_buoni=[]
i_buoni=[]
for i,name in enumerate(all_file):
    if name.find("xml")!=-1:
        tree = ET.parse(dir_finale+name)
        root = tree.getroot()
        #num di granuli presenti nel tar
        num_granuli=int(root.findall('TarFileCount')[0].text)
        for dataset in root.findall('Dataset'):
            nomefile=(dataset.find('FileName').text)
            #visualizzazione orario
            ore_inizio=nomefile.split('_')[3][1:5]
            ore_fine=nomefile.split('_')[4][1:5]
            #ricerca per orario dei granuli
            if ore_inizio[:4]=="1200":
                #salvataggio degli id buoni da utilizzare per scaricare i rispettivi file tar
                #id_buoni.append(name.split('.')[0].split('_')[3])
                tar_buoni.append(name.split(".manifest")[0])
                i_buoni.append(i)
                print ore_inizio, ore_fine   
#eliminazione degli id ripetuti
tar_buoni=list(set(tar_buoni))
i_buoni=list(set(i_buoni))
#ricerca dei file tar da scaricare e li scarica, si puo semplificare il processo unendo questa parte a quella di sopra
from pyftpclient import PyFTPclient
client_ftp=PyFTPclient('ftp-npp.class.ngdc.noaa.gov',21,'','')
client_ftp.DownloadFile(dir_ftp+tar_buoni[0],dir_finale_h5+tar_buoni[0])
'''
for tar in tar_buoni:
    new_fileh5=open(dir_finale_h5+tar,'wb')
    #ftp.retrbinary('RETR '+name,new_fileh5.write)
    new_fileh5.close()
    print "download completato"
 '''
          