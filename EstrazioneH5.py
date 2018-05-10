#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 09:56:26 2018

@author: angelozinna
"""

class EstrazioneH5:
    ftp_ip=""
    dir_ftp=""
    latitudine=0.0
    longitudine=0.0
    range_utile=0.0
    data_search=""
    tipologia_file=""
    dir_ftp=""
    all_file=[]
    dir_base=""
    dir_finale=""
    dir_finale_h5=""
    ftp=None
    tar_buoni={}
    gz_buoni=[]
    h5_buoni=[]
    
    
    def __init__(self,data,rang=1/float(3),tip='VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo',ip='ftp-npp.class.ngdc.noaa.gov',dir_base="~/Desktop/",lat=37.755,lon=15):
        self.data_search=data
        self.ftp_ip=ip
        self.range_utile=rang
        self.latitudine=lat
        self.longitudine=lon
        self.tipologia_file=tip
        self.dir_base=dir_base
        self.dir_ftp=data+'/VIIRS-SDR/'+tip+'/NPP/'
        
    #-----FUNZIONI SET-----
    
    def setTipologiaH5(self,tip):
        self.tipologia_file=tip
    def setRangeH5(self,rang):
        self.range_utile=rang
    def setIpFTP(self,ip):
        self.ftp_ip=ip
    def setDirFTP(self,dir_ftp):
        self.dir_ftp=dir_ftp
    def setData(self,data):
        self.data_search=data
    def setLatLong(self,lat,lon):
        self.latitudine=lat
        self.longitudine=lon
    def setDirBase(self,dir_base):
        self.dir_base=dir_base
        
    #-----FUNZIONI GET-----
    
    def getTarsPotenzialmenteBuoni(self):
        return self.tar_buoni
    def getGZPotenzialmenteBuoni(self):
        return self.gz_buoni
    
    #-----PROCEDURE PRIVATE-----
    
   
    def __checkH5File(self,gz):
        import h5py
        try:
            f = h5py.File(self.dir_finale_h5+gz[:-3], 'r') 
        except:
            print "file h5 non trovato o dannegiato"
            return
        #si seleziona all_data tra le key
        all_data= list(f.keys())[0]
        #si seleziona la prima voce tra le key
        data = list(f[all_data])[0]
        #si seleziona la latitudine
        matrice_lat=f[all_data][data]['Latitude']
        matrice_long=[[]]
        
        #calcolo range utile della mat da guardare
        shift=int(matrice_lat.shape[1]*self.range_utile)
        print "shift dal quale cominciare a prendere i dati:",shift
        print "lat1=",matrice_lat[0][shift]," lat2=",matrice_lat[-1][-shift]
        #controlla se la latitudine è compresa tra i valori di inizio e fine della mat
        if(matrice_lat[0][shift] < self.latitudine < matrice_lat[-1][-shift] or matrice_lat[-1][-shift] < self.latitudine < matrice_lat[0][shift]):
            matrice_long=f[all_data][data]['Longitude']
            print "latitudine corrisponde"
            #controlla se la longitudine è compresa tra i valori 
            if(matrice_long[0][shift] < self.longitudine < matrice_long[-1][-shift] or matrice_long[-1][-shift] < self.longitudine < matrice_long[0][shift]):
                print "longitudine corrisponde"
                self.h5_buoni=gz[:-3]
            else:
                print "long non corrisponde"
        else:
            print "lat non corrisponde"
                
    #-----PROCEDURE PUBBLICHE-----
    def connectFTP(self):
        from ftplib import FTP
        #connessione ftp
        self.ftp=FTP(self.ftp_ip)
        self.ftp.login()
        self.ftp.cwd(self.dir_ftp)
        #download della lista dei file nella directory dir_ftp
        res_ftp=self.ftp.retrlines('NLST',self.all_file.append)
        #print res_ftp
        print "connessione al server ftp riuscita!"
        res_ftp=res_ftp.split(' ')
        #calcolo file xml da scaricare
        num_el_xml=int(res_ftp[1])/2
        print "num_file xml=%d"% num_el_xml
        
    def createDirs(self):
        import os
        #creazione cartelle della data , xml e h5
        self.dir_finale=self.dir_base+self.data_search+'/'+self.tipologia_file+"/xml"
        self.dir_finale_h5=self.dir_base+self.data_search+'/'+self.tipologia_file+"/h5"
        if not os.path.exists(self.dir_finale):
            os.makedirs(self.dir_finale)
        if not os.path.exists(self.dir_finale_h5):
            os.makedirs(self.dir_finale_h5)
        self.dir_finale=self.dir_finale+'/'
        self.dir_finale_h5+='/'
        
    def downloadXMLs(self):
        try:
            for name in self.all_file:
                if name.find("xml")!=-1:
                    new_file=open(self.dir_finale+name, 'wb')
                    self.ftp.retrbinary('RETR '+name, new_file.write)
                    new_file.close()
                    print 'download complete:'+name
                    
            self.ftp.quit()
        except:
            print('Error during download xml from FTP server')
        print "download dei file xml completata"
        
    def downloadTars(self): # da rendere paralleli il download dei tar
        from pyftpclient import PyFTPclient
        from silence_stdout import nostdout
        if self.tar_buoni.keys() ==[]:
            print "nessun tar da scaricare , eseguire prima la funzione extractTarAndGzFromXMLByHour per trovare dei tar"
            return
        with nostdout():
            client_ftp=PyFTPclient(self.ftp_ip,21,'','')
        for i,tar in enumerate(self.tar_buoni.keys()):
            with nostdout():
                client_ftp.DownloadFile(self.dir_ftp+tar,self.dir_finale_h5+tar)
        print "download completato del tar numero:",i+1

    def extractTarAndGzFromXMLByHour(self,data):
        tar_creato=0
        if len(data)>4 or len(data)<3:
            print "formato della data troppo corto o lungo, esempio di orario 12:40 = 1240(orario preciso) oppure 124(orario non preciso)"
            return
        #prelevamento info dall'xml
        import xml.etree.ElementTree as ET 
        i_buoni=[]     
        print "date utili:"
        for i,name in enumerate(self.all_file):
            if name.find("xml")!=-1:
                tree = ET.parse(self.dir_finale+name)
                root = tree.getroot()
                #num di granuli presenti nel tar
                num_granuli=int(root.findall('TarFileCount')[0].text)
                tar_creato=0
                for dataset in root.findall('Dataset'):
                    nomefile=(dataset.find('FileName').text)
                    #visualizzazione orario
                    ore_inizio=nomefile.split('_')[3][1:5]
                    ore_fine=nomefile.split('_')[4][1:5]
                    #ricerca per orario dei granuli
                    if ore_inizio[:len(data)]==data:
                        if tar_creato==0:
                            self.tar_buoni[name.split(".manifest")[0]]=[]
                            tar_creato=1
                        #salvataggio degli id buoni da utilizzare per scaricare i rispettivi file tar
                        #id_buoni.append(name.split('.')[0].split('_')[3])                
                        self.tar_buoni[name.split(".manifest")[0]].append(nomefile+".gz")
                        i_buoni.append(i)
                        print "ora inizio:",ore_inizio,"- ora fine:",ore_fine          
        #eliminazione degli id ripetuti
        i_buoni=list(set(i_buoni))
        
    
    
    
        