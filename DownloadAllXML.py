#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:03:06 2018

@author: angelozinna
"""
from ftplib import FTP
import os
latitudine=37.755
longitudine=15
range_utile=1/float(3)
data_search="20180420"
tipologia_file='VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo'
dir_ftp=data_search+'/VIIRS-SDR/'+tipologia_file+'/NPP/'
all_file =[]


#connessione ftp
ftp=FTP('ftp-npp.class.ngdc.noaa.gov')
ftp.login()
ftp.cwd(dir_ftp)
#download della lista dei file nella directory dir_ftp
res_ftp=ftp.retrlines('NLST',all_file.append)
#print res_ftp
print "connessione al server ftp riuscita!"

res_ftp=res_ftp.split(' ')
num_el_xml=int(res_ftp[1])/2
#print "num_file xml=%d"% num_el_xml

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

'''

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
print "download dei file xml completata"
'''


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
            if ore_inizio[:4]=="1200":
                #salvataggio degli id buoni da utilizzare per scaricare i rispettivi file tar
                #id_buoni.append(name.split('.')[0].split('_')[3])
                tar_buoni.append(name.split(".manifest")[0])
                i_buoni.append(i)
                gz_buoni.append(nomefile+".gz")
                print ore_inizio, ore_fine   
                
#eliminazione degli id ripetuti
tar_buoni=list(set(tar_buoni))
i_buoni=list(set(i_buoni))
#download file tar(non funziona su mac e windows credo)
'''
from pyftpclient import PyFTPclient
from silence_stdout import nostdout
with nostdout():
    client_ftp=PyFTPclient('ftp-npp.class.ngdc.noaa.gov',21,'','')
for tar in tar_buoni:
    with nostdout():
        client_ftp.DownloadFile(dir_ftp+tar,dir_finale_h5+tar)
    print "download completato"
'''
#apertura tar file e ricerca dei gz da scaricare
import tarfile
tar=tarfile.open(name=dir_finale_h5+tar_buoni[0], mode='r', fileobj=None, bufsize=10240)
lista=tar.getnames()
for gz in gz_buoni:
    if gz in lista:
        print "ce"
        tar.extract(tar.getmember(gz),dir_finale_h5)
        print "estrazione file gz dal file tar completata"
        import subprocess
        #estrazione gz da bash (non funziona)
        bash="gunzip "+dir_finale_h5+gz
        process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        print "estrazione file gz completata"
       
        
        #apertura e ricerca dei gz che corrispondono a quelli dell'etna
        import h5py
        f = h5py.File(dir_finale_h5+gz[:-3], 'r') 
        #si seleziona all_data tra le key
        all_data= list(f.keys())[0]
        #si seleziona la prima voce tra le key
        data = list(f[all_data])[0]
        #si seleziona la latitudine
        matrice_lat=f[all_data][data]['Latitude']
        matrice_long=[[]]
        
        #calcolo range utile della mat da guardare
        shift=int(matrice_lat.shape[1]*range_utile)
        print "shift dal quale cominciare a prendere i dati:",shift

        
        #se la latitudine è compresa tra i valori di inizio e fine della mat
        if(matrice_lat[0][shift] < latitudine < matrice_lat[-1][-shift] or matrice_lat[-1][-shift] < latitudine < matrice_lat[0][shift]):
            matrice_long=f[all_data][data]['Longitude']
            print "latitudine corrisponde"
            if(matrice_long[0][0] < longitudine < matrice_long[-1][-1] or matrice_long[-1][-1] < longitudine < matrice_long[0][0]):
                print "longitudine corrisponde"
            else:
                print "long non corrisponde"
        else:
            print "lat non corrisponde"
        


          