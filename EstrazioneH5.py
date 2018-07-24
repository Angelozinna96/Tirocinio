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
    dir_finale_xml=""
    dir_finale_h5=""
    dir_finale_goodh5=""
    range_orario=20
    ftp=None
    tar_salvati={}
    gz_buoni=[]
    h5_buoni=[]
    
    
    def __init__(self,data,rang=0,tip='VIIRS-Day-Night-Band-SDR-Ellipsoid-Geo',dir_base="./",lat=37.755,lon=15,ip='ftp-npp.bou.class.noaa.gov',data_type):
        self.data_search=data
        self.ftp_ip=ip
        self.range_utile=rang
        self.latitudine=lat
        self.longitudine=lon
        self.tipologia_file=tip
        self.dir_base=dir_base
        if(data_type=="SDR"):
            self.dir_ftp=data+'/VIIRS-SDR/'+tip+'/NPP/'
        else:
            self.dir_ftp=data+'/VIIRSI-EDR/'+tip+'/NPP/'
        self.createDirs()
        self.connectFTP()
        self.downloadXMLs()

        
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



    #-----PROCEDURE PRIVATE-----
    
    def __calculateShift(self,length):
      shift=int(length*self.range_utile) +1
      return shift
        
    def __checkH5File(self,gz):
        import h5py
        try:
            f = h5py.File(self.dir_finale_h5+gz[:-3], 'r') 
        except:
            print "file h5 non trovato o dannegiato!"
            return None
        #si seleziona all_data tra le key
        all_data= list(f.keys())[0]
        #si seleziona la prima voce tra le key
        data = list(f[all_data])[0]
        #si seleziona la latitudine
        matrice_lat=f[all_data][data]['Latitude']
        matrice_long=[[]]
        
        #calcolo range utile della mat da guardare
        shift=self.__calculateShift(matrice_lat.shape[1])        
        print "\nshift dal quale cominciare a prendere i dati:",shift
        print "lat1=",matrice_lat[0][shift]," lat2=",matrice_lat[-1][-shift]
        #da mettere dentro l if dopo il debug
        matrice_long=f[all_data][data]['Longitude']
        print "long1=",matrice_long[0][shift]," long2=",matrice_long[0][-shift]
        #controlla se la latitudine è compresa tra i valori di inizio e fine della mat
        if(matrice_lat[0][shift] < matrice_lat[-1][-shift]):
            if(matrice_lat[0][shift] < self.latitudine < matrice_lat[-1][-shift]): 
                print "latitudine corrisponde"
                #controlla se la longitudine è compresa tra i valori 
                if(matrice_long[0][shift] < matrice_long[0][-shift]):
                    if(matrice_long[0][shift] < self.longitudine < matrice_long[0][-shift]):
                        print "longitudine corrisponde"
                        return gz[:-3]
                else:
                    if(matrice_long[0][-shift] < self.longitudine < matrice_long[0][shift]):
                        print "longitudine corrisponde"
                        return gz[:-3]
                print "longitudine non corrisponde"
                    
            else:
                print "lat non corrisponde"
                print "longitudine nemmeno controllata"
        else:
            if(matrice_lat[-1][-shift] < self.latitudine < matrice_lat[0][shift]):
                print "latitudine corrisponde"
                #controlla se la longitudine è compresa tra i valori 
                if(matrice_long[0][shift] < matrice_long[0][-shift]):
                    if(matrice_long[0][shift] < self.longitudine < matrice_long[0][-shift]):
                        print "longitudine corrisponde"
                        return gz[:-3]
                else:
                    if(matrice_long[0][-shift] < self.longitudine < matrice_long[0][shift]):
                        print "longitudine corrisponde"
                        return gz[:-3]
                print "longitudine non corrisponde"
            else:
                print "lat non corrisponde"
                print "longitudine nemmeno controllata"
                
        return None
                
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
        print "CONNESSIONE AL SERVER FTP RIUSCITA!"
        res_ftp=res_ftp.split(' ')
        #calcolo file xml da scaricare
        
    def createDirs(self):
        import os
        #creazione cartelle della data , xml e h5
        self.dir_finale_xml=self.dir_base+self.data_search+'/'+self.tipologia_file+"/xml"
        self.dir_finale_h5=self.dir_base+self.data_search+'/'+self.tipologia_file+"/h5"
        self.dir_finale_goodh5=self.dir_base+self.data_search+'/'+self.tipologia_file+"/GoodH5"
        if not os.path.exists(self.dir_finale_xml):
            os.makedirs(self.dir_finale_xml)
        if not os.path.exists(self.dir_finale_h5):
            os.makedirs(self.dir_finale_h5)
        if not os.path.exists(self.dir_finale_goodh5):
            os.makedirs(self.dir_finale_goodh5)
        self.dir_finale_xml=self.dir_finale_xml+'/'
        self.dir_finale_h5+='/'
        self.dir_finale_goodh5+='/'
        
    def downloadXMLs(self):
        import os
        try:
            for name in self.all_file:
                if name.find("xml")!=-1 and not os.path.exists(self.dir_finale_xml+name):
                    new_file=open(self.dir_finale_xml+name, 'wb')
                    self.ftp.retrbinary('RETR '+name, new_file.write)
                    new_file.close()
                    print 'download complete:'+name
                    
            self.ftp.quit()
        except:
            print('Error during download xml from FTP server')
        
    def extractTarAndGzInfoFromXMLByHour(self,orario):
        tar_creato=False
        if len(orario)>4 or len(orario)<3:
            print "formato della data troppo corto o lungo, esempio di orario 12:40 = 1240(orario preciso) oppure 124(orario non preciso, prenderà tutti quelli compresi dalle 12:40 alle 12:49)"
            return
        #prelevamento info dall'xml
        import xml.etree.ElementTree as ET 
        i_buoni=[]     
        print "Scansioni fatte dal satellite:"
        for i,name in enumerate(self.all_file):
            if name.find("xml")!=-1:
                tree = ET.parse(self.dir_finale_xml+name)
                root = tree.getroot()
                tar_creato=False
                for dataset in root.findall('Dataset'):
                    nomefile=(dataset.find('FileName').text)
                    #visualizzazione orario
                    ore_inizio=nomefile.split('_')[3][1:5]
                    ore_fine=nomefile.split('_')[4][1:5]
                    #ricerca per orario dei granuli
                    if ore_inizio[:len(orario)]==orario or ore_fine[:len(orario)]==orario:
                        if tar_creato==False and name.split(".manifest")[0] not in self.tar_salvati.keys():
                            self.tar_salvati[name.split(".manifest")[0]]={}
                            tar_creato=True
                        #salvataggio degli id buoni da utilizzare per scaricare i rispettivi file tar (non dovrebbe servire, basta il nome)
                        #id_buoni.append(name.split('.')[0].split('_')[3])                
                        self.tar_salvati[name.split(".manifest")[0]][nomefile+".gz"]="Not yet"
                        i_buoni.append(i)
                        print "ora inizio:",ore_inizio,"- ora fine:",ore_fine          
        #eliminazione degli id ripetuti
        i_buoni=list(set(i_buoni))
        print"\n"
        
    #download di un singolo tar
    def downloadTar(self,tar):
        from pyftpclient import PyFTPclient
        from silence_stdout import nostdout
        print "download in corso..."
        with nostdout():
            client_ftp=PyFTPclient(self.ftp_ip,21,'','')
        with nostdout():
            client_ftp.DownloadFile(self.dir_ftp+tar,self.dir_finale_h5+tar)
        print "download completato del tar "
    def downloadTars(self): # da rendere paralleli il download dei tar
        import os
        from pyftpclient import PyFTPclient
        from silence_stdout import nostdout
        print "download in corso..."
        if self.tar_salvati.keys() ==[]:
            print "nessun tar da scaricare , eseguire prima la funzione extractTarAndGzInfoFromXMLByHour per trovare dei tar"
            return
        try:
            with nostdout():
                client_ftp=PyFTPclient(self.ftp_ip,21,'','')
            for i,tar in enumerate(self.tar_salvati.keys()):
                if not os.path.exists(self.dir_finale_h5+tar):
                    with nostdout():
                        client_ftp.DownloadFile(self.dir_ftp+tar,self.dir_finale_h5+tar)
                        print "download  del tar completato"
            print "download di tutti i tar completato"
        except:
            print "errore nel download del tar"

    def checkAllPotGoodGZFromTars(self,orario):
        import tarfile as t
        for tar in self.tar_salvati.keys():    
            try:
                open(self.dir_finale_h5+tar, 'r')
                tar_file=t.open(name=self.dir_finale_h5+tar, mode='r', fileobj=None, bufsize=10240)
                for gz in self.tar_salvati[tar].keys():
                    if self.tar_salvati[tar][gz]=="Not yet": 
                        tar_file.extract(tar_file.getmember(gz),self.dir_finale_h5)
                        #print "estrazione file gz dal file tar completata"
                        import subprocess
                        #estrazione gz da bash 
                        bash="gunzip "+self.dir_finale_h5+gz
                        process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
                        #output, error = process.communicate()
                        #print "estrazione file gz completata"
                        
                        #delay impostato per permettere di estrarre tutto il file h5 prima di usarlo
                        import time
                        time.sleep(2.5)                        
                        #apertura e ricerca dei gz che corrispondono a quelli dell'etna
                        res=self.__checkH5File(gz)
                        if type(res)==str:
                            self.tar_salvati[tar][gz]="Good"
                            return res
                        else:
                            self.tar_salvati[tar][gz]="Not Good"
                            
                         
            except:
                print "\ntar file=",tar," non disponibile in ",self.dir_finale_h5, " o corrotto,scaricarlo di nuovo!"
                continue
        return None
  
  
    #formato data AAAA-MM-GG
    def downloadInfoNPPFile(self,_data):        
        import subprocess
        import os
          
        data=_data[:4]+"-"+_data[4:6]+"-"+_data[6:8]
        anno=data.split("-")[0] 
        nomefile="VNP03MOD_"+data+".txt"
        if not os.path.exists(self.dir_base+self.data_search+"/"+nomefile):
          #download del file da bash con wget
          URL="https://ladsweb.modaps.eosdis.nasa.gov/archive/geoMetaJPSS/5110/NPP/"+anno+"/"+nomefile
          print URL
          bash="wget  "+URL+" -P "+self.dir_base+self.data_search+'/'
          process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
          output, error = process.communicate() 
          print "download del file txt contenente tutte le info su dove si trova il satellite completato!"
        
    #formato data AAAA-MM-GG
    def extractInfoNPPFile(self,_data):
        data=_data[:4]+"-"+_data[4:6]+"-"+_data[6:8]
        dati_file=open(self.dir_base+self.data_search+'/'+"VNP03MOD_"+data+".txt","r")
        ore=list()
        for line in dati_file:
            est=line.split(",")[5]
            ovest=line.split(",")[8]
            nord=line.split(",")[6]
            sud=line.split(",")[7]
            try:
                if float(est)>15 and float(ovest)<14 and float(nord)>38 and float(sud)<37 :
                    '''
                    print "-----------trovato---------"
                    print " north="+line.split(",")[7]+" south="+line.split(",")[8]+" east="+line.split(",")[6]+" west="+line.split(",")[9]
                    print "all'ora="+line.split(",")[1].split(" ")[1]
                    '''
                    ore.append(line.split(",")[1].split(" ")[1])
            except ValueError:
                continue
        dati_file.close()
        print "orari in cui il satellite è passato dall'Etna:",ore
        return ore

    def secureFind(self,_data):
        import subprocess
        import os
        self.downloadInfoNPPFile(_data)
        ore=self.extractInfoNPPFile(_data)
        orari_trovati=list()
        for i in ore:
            ora_mod=i.split(":")[0]+i.split(":")[1]
            ora_mod=ora_mod[:3]
            print "----------SCANSIONE ORARIO =",ora_mod[:2]+":"+ora_mod[2]+"0----------\n"
            self.extractTarAndGzInfoFromXMLByHour(ora_mod)
            self.downloadTars()
            res=self.checkAllPotGoodGZFromTars(ora_mod)
            if type(res)==str:
              orario_trovato=res.split("_")[3][1:5]+"-"+res.split("_")[4][1:5]
              print "########## TROVATO ALL'ORARIO:",orario_trovato,"\n"
              orari_trovati.append(orario_trovato)
              #copia dell'h5 dalla cartella h5 alla cartella GoodH5
              if not os.path.exists(self.dir_finale_goodh5+res):
                bash="mv "+self.dir_finale_h5+res+"  "+self.dir_finale_goodh5
                process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
            print "-------------------------------------------\n\n\n"
            
        print "########## ORARI TROVATI ##########"
        orari_trovati=list(set(orari_trovati))
        for i in orari_trovati:
          print i  
        print "tutti gli h5 buoni sono stati spostati nella cartella:\n",self.dir_finale_goodh5           
            
        
                    
                    
                    
                
        
    
    
    
        