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
    range_orario=20
    ftp=None
    tar_salvati={}
    gz_buoni=[]
    h5_buoni=[]
    
    
    def __init__(self,data,rang=0,tip='VIIRS-Day-Night-Band-SDR-Ellipsoid-Geo',ip='ftp-npp.bou.class.noaa.gov',dir_base="~/Desktop/",lat=37.755,lon=15):
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
        return self.tar_salvati.keys()
    def getGZPotenzialmenteBuoni(self):
        return self.tar_salvati.values()
    
    #-----PROCEDURE PRIVATE-----
    
   
    def __checkH5File(self,gz):
        import h5py
        try:
            f = h5py.File(self.dir_finale_h5+gz[:-3], 'r') 
        except:
            print "file h5 non trovato o dannegiato"
            return None
        #si seleziona all_data tra le key
        all_data= list(f.keys())[0]
        #si seleziona la prima voce tra le key
        data = list(f[all_data])[0]
        #si seleziona la latitudine
        matrice_lat=f[all_data][data]['Latitude']
        matrice_long=[[]]
        
        #calcolo range utile della mat da guardare
        shift=int(matrice_lat.shape[1]*self.range_utile) +1
        
        print "shift dal quale cominciare a prendere i dati:",shift
        print "lat1=",matrice_lat[0][shift]," lat2=",matrice_lat[-1][-shift]
        #da mettere dentro l if dopo il debug
        matrice_long=f[all_data][data]['Longitude']
        print "long1=",matrice_long[0][shift]," long2=",matrice_long[0][-shift]
        #controlla se la latitudine è compresa tra i valori di inizio e fine della mat
        if(matrice_lat[0][shift] < self.latitudine < matrice_lat[-1][-shift] or matrice_lat[-1][-shift] < self.latitudine < matrice_lat[0][shift]):
            
            print "latitudine corrisponde"
            #controlla se la longitudine è compresa tra i valori 
            if(matrice_long[0][shift] < self.longitudine < matrice_long[0][-shift] or matrice_long[0][-shift] < self.longitudine < matrice_long[0][shift]):
                print "longitudine corrisponde"
                return gz[:-3]
        else:
            print "lat non corrisponde"
        return ((matrice_lat[0][shift],matrice_lat[-1][-shift]),(matrice_long[0][shift],matrice_long[0][-shift]))
                
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
        import os
        try:
            for name in self.all_file:
                if name.find("xml")!=-1 and not os.path.exists(self.dir_finale+name):
                    new_file=open(self.dir_finale+name, 'wb')
                    self.ftp.retrbinary('RETR '+name, new_file.write)
                    new_file.close()
                    print 'download complete:'+name
                    
            self.ftp.quit()
        except:
            print('Error during download xml from FTP server')
        print "download dei file xml completata"
    def extractTarAndGzInfoFromXMLByHour(self,orario):
        tar_creato=False
        if len(orario)>4 or len(orario)<3:
            print "formato della data troppo corto o lungo, esempio di orario 12:40 = 1240(orario preciso) oppure 124(orario non preciso, prenderà tutti quelli compresi dalle 12:40 alle 12:49)"
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
                tar_creato=False
                for dataset in root.findall('Dataset'):
                    nomefile=(dataset.find('FileName').text)
                    #visualizzazione orario
                    ore_inizio=nomefile.split('_')[3][1:5]
                    ore_fine=nomefile.split('_')[4][1:5]
                    #ricerca per orario dei granuli
                    if ore_inizio[:len(orario)]==orario:
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
            print "download completato del tar numero:",i+1
        except:
            print "errore nel download del tar"

    def checkAllPotGoodGZFromTars(self):
        import tarfile as t
        import sys
        for tar in self.tar_salvati.keys():
            
            try:

                open(self.dir_finale_h5+tar, 'r')
                tar_file=t.open(name=self.dir_finale_h5+tar, mode='r', fileobj=None, bufsize=10240)
                
                #riga seguente inutile
                #lista=tar_file.getnames()
                #print lista
           
                
                for gz in self.tar_salvati[tar].keys():
                    if self.tar_salvati[tar][gz]=="Not yet": 
                        tar_file.extract(tar_file.getmember(gz),self.dir_finale_h5)
                        print "estrazione file gz dal file tar completata"
                        import subprocess
                        #estrazione gz da bash 
                        print self.dir_finale_h5+gz
                        bash="gunzip "+self.dir_finale_h5+gz
                        process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
                        #output, error = process.communicate()
                        print "estrazione file gz completata"
                        
                        #delay impostato per permettere di estrarre tutto il file h5 prima di usarlo
                        import time
                        time.sleep(2.5) 
                        
                        #apertura e ricerca dei gz che corrispondono a quelli dell'etna
                        res=self.__checkH5File(gz)
                        if type(res)==str:
                            self.tar_salvati[tar][gz]="Good"
                            res=None
                            return res
                        else:
                            self.tar_salvati[tar][gz]="Not Good"
                        
            except:
                print "\ntar file=",tar," non disponibile in ",self.dir_finale_h5, " o corrotto,scaricarlo di nuovo!"
                continue
        return None
    
    def checkAllPotGoodGZFromTars2(self,orario):
        import tarfile as t
        import sys
        gz_list=list()
        differenza_lat=list()
        differenza_long=list()
        direzione=list()
        for tar in self.tar_salvati.keys():    
            try:
                open(self.dir_finale_h5+tar, 'r')
                tar_file=t.open(name=self.dir_finale_h5+tar, mode='r', fileobj=None, bufsize=10240)
                for gz in self.tar_salvati[tar].keys():
                    if self.tar_salvati[tar][gz]=="Not yet": 
                        tar_file.extract(tar_file.getmember(gz),self.dir_finale_h5)
                        print "estrazione file gz dal file tar completata"
                        import subprocess
                        #estrazione gz da bash 
                        print self.dir_finale_h5+gz
                        bash="gunzip "+self.dir_finale_h5+gz
                        process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
                        #output, error = process.communicate()
                        print "estrazione file gz completata"
                        
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
                            #si fa un controllo su quanto è distante dall'Etna e lo si salva in una lista
                         
                            #il primo controllo viene fatto sulla latitudine
                            
                            #controllo se la latitudine è positiva e maggiore della latitudine dell' etna
                            if(res[0][0]>self.latitudine):
                                if(res[0][1]>self.latitudine):
                                    differenza_lat.append(res[0][1]-self.latitudine)
                                    direzione.append("sopra")
                                else:
                                    #controllo longitudine
                                    
                                    if(res[1][0]>self.longitudine):                                  
                                        differenza_long.append(self.longitudine - res[1][0])
                                        direzione.append("destra")
                                    elif(res[1][0]<0):
                                        differenza_long.append(self.longitudine + ((-1)*res[1][0]))
                                        direzione.append("sinistra")
                                    else:
                                        differenza_long.append(self.longitudine - res[1][0])
                                        direzione.append("sinistra")
                            #stesso controllo ma su altri possibili valori della latitudine
                            elif res[0][0]<0:
                                differenza_lat.append(self.latitudine + ((-1)*res[0][0]))
                                direzione.append("sotto")
                            else:
                                differenza_lat.append(self.latitudine - res[0][0])
                                direzione.append("sotto")
                            gz_list.append(gz)
                         
            except:
                print "\ntar file=",tar," non disponibile in ",self.dir_finale_h5, " o corrotto,scaricarlo di nuovo!"
                continue
        '''
        print "lat:",differenza_lat
        print "long:",differenza_long
        print "gz:",gz_list
        print "direzioni:",direzione
        '''
        if len(differenza_lat)==0:
            print "Errore nel download di qualche tar!"
            return None
        i_min=differenza_lat.index(min(differenza_lat))
        
        #se già la latitudine non va bene non ha senso vedere la longitudine!
        if direzione[i_min]=="sopra" or direzione[i_min]=="sotto":
            info_distanza_minima=(differenza_lat[i_min],0,gz_list[i_min],direzione[i_min])
        else:
            info_distanza_minima=(differenza_lat[i_min],differenza_long[i_min],gz_list[i_min],direzione[i_min])
        return info_distanza_minima
    def findGoodH5InDict(self):
        goodH5=[];
        for tar in self.tar_salvati.keys():
            for gz in  self.tar_salvati[tar]:
                if self.tar_salvati[tar][gz]=="Good":
                    goodH5.append(gz[:-3])
        if len(goodH5) > 0:
            return goodH5
        else:
            return None
        
    def writeInFileGoodH5(self,h5):
        import os
        
        str=""
        if not os.path.exists(self.dir_finale_h5+"goodH5"): 
            f=open(self.dir_finale_h5+"goodH5",'w')
            for i in h5:
                str+=i+"\n"
            f.write(str)
            f.close()
        else: 
            f=open(self.dir_finale_h5+"goodH5",'r')
            contenuto=f.read()
            f.close()
            for i in h5:
                if contenuto.find(i)==-1:
                    str+=i+"\n"
            if len(str)>0:
                f=open(self.dir_finale_h5+"goodH5",'a')            
                f.write(str)
                f.close()
    '''
    def findRecursiveGoodGZ(self,orario):
        self.extractTarAndGzInfoFromXMLByHour(orario)
        self.downloadTars() 
        for tar in self.tar_salvati.keys():
            gz=None
            for gzi in self.tar_salvati[tar].keys():
                    if gzi == "Not yet":
                        gz=gzi
                        break
            res=self.checkPotGoodGZFromTars(tar,gz)
            if type(res)==str:
                print "trovato"
                h5=self.findGoodH5InDict();
                self.writeInFileGoodH5(h5)
                return res
            ora_inizio=gz.split('_')[3][1:5]
            ora_fine=gz.split('_')[4][1:5]
            if(ora_fine):
                self.findRecursiveGoodGZ()
    ''' 
    #converte sempre l'orario  con l'orario non preciso(3 cifre)
    def smartFindH5(self,_data,orario,num_tent):
        import time
        from datetime import datetime, date, time, timedelta as td
        #se l'orario è nel formato non preciso bisogna aggiungere uno zero alla fine prima di trasformarlo in data      
        direzione=None
        passo=False #controlla se si è entrati almeno in una condizione all'interno del ciclo
        salto=False #bool che indica se è stato trovato un gz dove non corrisponde solamente la longitudine ed è quindi stato fatto un salto di orbita(1 ora e 40 min), se si farà il salto non si potrà usufruire del range dei 30 minuti dal massimo 
        for i in range(num_tent):
            passo=False 
            print "\n--------Tentativo n°",i+1 ,"-----------"
            self.extractTarAndGzInfoFromXMLByHour(orario)
            self.downloadTars()
            res=self.checkAllPotGoodGZFromTars2(orario)
            if type(res)==str:
                print "--------------TROVATO-----------\nfile gz=",res,"\n---------------------------------"
                return self.dir_finale_h5+res
            if res==None:
                print "errore all'interno della funzione di check!"
                break
            data=datetime.strptime(_data+" "+orario[:3]+"0", '%Y%m%d %H%M')
            print "Non trovato!Questo e' il gz più vicino(diff lat ed etna,eventuale diff longitudine,nome_gz,direzione):",res 
            #condizione iniziale di entrata oppure successiva ad un salto
            if direzione==None and res[3] in ["sopra","sotto"]:
                direzione=res[3]
                
            #condizione in cui salendo o scendendo con la latitudine si è superata l'Etna, per non causare ulteriori cicli inutili chiude subito
            if (res=="sotto" and direzione=="sopra") or (res=="sopra" and direzione=="sotto"):
                print "si è superata l'Etna, vuol dire che si è troppo lontani da essa!"
                break;
        
            #controlla se l'orario sta nel range massimo diurno(tra le 11:10 e le 13:00)
            if datetime.strptime(_data+" 1110", '%Y%m%d %H%M') <= data <=datetime.strptime(_data+" 1300", '%Y%m%d %H%M'):
                salto=False
                passo=True
                if res[3]=="sotto":
                    data = data + td(minutes=10)
                elif res[3]=="sopra":

                    data = data - td(minutes=10)
                    
                elif res[3]=="destra":
                    if(self.range_utile!=0):
                        print "[consiglio]provare ad allargare il range possibile!"
                    print "si prova a cercare all' orbita successiva"
                    data = data + td(minutes=100)
                    direzione=None
                    salto=True
                else:
                    if(self.range_utile!=0):
                        print "[consiglio]provare ad allargare il range possibile!"
                    print "si prova a cercare all' orbita precedente"
                    data = data - td(minutes=100)
                    direzione=None
                    salto=True
                
        
            #altrimenti controlla se la data è vicina al range massimo diurno(11:10) di 30 minuti
            elif abs(((datetime.strptime(_data+" 1110", '%Y%m%d %H%M')-data).seconds)/60)<30:
                if(salto):
                    break
                else:
                    passo=True
                    salto=False
                    diff=abs(((data-datetime.strptime(_data+" 1110", '%Y%m%d %H%M')).seconds)/60)<30
                    #si va a cercare a partire da= 13:00 - minuti_di_diff
                    data=datetime.strptime(_data+" 1300", '%Y%m%d %H%M')-td(minutes=diff)
                    direzione=None
                    
            #altrimenti controlla se la data è vicina al range massimo diurno(13:00) di 30 minuti
            elif abs(((data-datetime.strptime(_data+" 1300", '%Y%m%d %H%M')).seconds)/60)<30:
                if(salto):
                    break
                else:
                    passo=True
                    salto=False
                    diff=abs(((data-datetime.strptime(_data+" 1300", '%Y%m%d %H%M')).seconds)/60)<30
                    #si va a cercare a partire da= 11:10 + minuti_di_diff
                    data=datetime.strptime(_data+" 1110", '%Y%m%d %H%M')+td(minutes=diff)
                    direzione=None
                    
                
                
                
            #controlla se l'orario sta nel range massimo notturno(tra le 00:10 e le 02:00)
            if datetime.strptime(_data+" 0010", '%Y%m%d %H%M') <= data <=datetime.strptime(_data+" 0200", '%Y%m%d %H%M'):
                passo=True
                salto=False
                if res[3]=="sotto":
                    data = data - td(minutes=10)
                elif res[3]=="sopra":
                    data = data + td(minutes=10)
                    
                elif res[3]=="destra":
                    if(self.range_utile!=0):
                        print "[consiglio]provare ad allargare il range possibile!"
                    print "si prova a cercare all' orbita successiva"
                    data = data + td(minutes=100)
                    direzione=None
                    salto=True
                else:
                    if(self.range_utile!=0):
                        print "[consiglio]provare ad allargare il range possibile!"
                    print "si prova a cercare all' orbita precedente"
                    data = data - td(minutes=100)
                    direzione=None
                    salto=True
            #altrimenti controlla se la data è vicina al range massimo diurno(00:10) di 30 minuti    
            elif abs(((datetime.strptime(_data+" 0010", '%Y%m%d %H%M')-data).seconds)/60)<30:
                if(salto):
                    break
                else:
                    passo=True
                    salto=False
                    diff=abs(((data-datetime.strptime(_data+" 0010", '%Y%m%d %H%M')).seconds)/60)<30
                    #si va a cercare a partire da= 02:00 - minuti_di_diff
                    data=datetime.strptime(_data+" 0200", '%Y%m%d %H%M')-td(minutes=diff)
                    direzione=None
                    
            #altrimenti controlla se la data è vicina al range massimo diurno(02:00) di 30 minuti    
            elif abs(((data-datetime.strptime(_data+" 0200", '%Y%m%d %H%M')).seconds)/60)<30:
                if(salto):
                    break
                else:
                    passo=True
                    salto=False
                    diff=abs(((data-datetime.strptime(_data+" 0200", '%Y%m%d %H%M')).seconds)/60)<30
                    #si va a cercare a partire da= 00:10 + minuti_di_diff
                    data=datetime.strptime(_data+" 0010", '%Y%m%d %H%M')+td(minutes=diff)
                    direzione=None
                    
            if(not passo):
                break
            orario=data.strftime("%H%M")[:3]
            print "Si prova a cercarne un altro all'ora "+data.strftime("%H:%M")
            
            
            
            
            
            
    
        
        
            
        
        
        
 
       

        
                    
                    
                    
                
        
    
    
    
        