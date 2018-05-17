#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:03:06 2018

@author: angelozinna
"""
import funzioni_utili as util
from ftplib import FTP
import os
latitudine=37.755
longitudine=15
ftp_ip='ftp-npp.class.ngdc.noaa.gov'
range_utile=1/float(3)
data_search="20180420"
tipologia_file='VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo'
dir_ftp=data_search+'/VIIRS-SDR/'+tipologia_file+'/NPP/'
all_file =[]


#connessione ftp
ftp=FTP(ftp_ip)
ftp.login()
ftp.cwd(dir_ftp)
#download della lista dei file nella directory dir_ftp
res_ftp=ftp.retrlines('NLST',all_file.append)
#print res_ftp
print "connessione al server ftp riuscita!"
res_ftp=res_ftp.split(' ')
#calcolo file xml da scaricare
num_el_xml=int(res_ftp[1])/2
print "num_file xml=%d"% num_el_xml

#dir di base dove salvare i file
dir_base='/Users/angelozinna/Desktop/university/3anno/tirocinio/dati/'

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

#util.downloadXMLs(all_file,dir_finale,ftp)


#prelevamento info dall'xml
    
import xml.etree.ElementTree as ET 
tar_buoni=[]
i_buoni=[]
gz_buoni=[]
print "date utili:"
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
            if ore_inizio[:3]=="120":
                #salvataggio degli id buoni da utilizzare per scaricare i rispettivi file tar
                #id_buoni.append(name.split('.')[0].split('_')[3])
                tar_buoni.append(name.split(".manifest")[0])
                i_buoni.append(i)
                gz_buoni.append(nomefile+".gz")
                print "ora inizio:",ore_inizio,"- ora fine:",ore_fine   
                
#eliminazione degli id ripetuti
tar_buoni=list(set(tar_buoni))
i_buoni=list(set(i_buoni))
#download file tar(non funziona su mac e windows credo)

#util.downloadTars(ftp_ip,tar_buoni,dir_ftp,dir_finale_h5)

#apertura tar file e ricerca dei gz da usare
import tarfile
import sys
h5_buoni=[]
for itar in tar_buoni:
    try:
        tar=tarfile.open(name=dir_finale_h5+itar, mode='r', fileobj=None, bufsize=10240)
        lista=tar.getnames()
    except:
        print "tar file non disponibile o corrotto,scaricarlo di nuovo!"
        sys.exit(0)
    #print lista
    
    for gz in gz_buoni:
        if gz in lista:
            print "gz:",gz, "\n è presente nel tar:",itar
            tar.extract(tar.getmember(gz),dir_finale_h5)
            print "estrazione file gz dal file tar completata"
            import subprocess
            #estrazione gz da bash 
            print dir_finale_h5+gz
            bash="gunzip "+dir_finale_h5+gz
            process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
            #output, error = process.communicate()
            print "estrazione file gz completata"
            
            #delay impostato per permettere di estrarre tutto il file h5 prima di usarlo
            import time
            time.sleep(2.5) 
            
            #apertura e ricerca dei gz che corrispondono a quelli dell'etna
            h5_buoni.append(util.checkH5File(dir_finale_h5,range_utile,latitudine,longitudine,gz,h5_buoni))
           
print h5_buoni
        
        


          