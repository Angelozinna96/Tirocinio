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
    all_file_xml =[]
    dir_base=""
    dir_finale=""
    dir_finale_h5=""
    ftp=None
    
    def __init__(self,data,rang=1/float(3),tip='VIIRS-Image-Bands-SDR-Ellipsoid-Terrain-Corrected-Geo',ip='ftp-npp.class.ngdc.noaa.gov',dir_base="~/Desktop/",dir_ftp=data_search+'/VIIRS-SDR/'+tipologia_file+'/NPP/',lat=37.755,lon=15):
        self.data_search=data
        self.ftp_ip=ip
        self.range_utile=rang
        self.latitudine=lat
        self.longitudine=lon
        self.tipologia_file=tip
        self.dir_ftp=dir_ftp
        self.dir_base=dir_base
        
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
        
    def __connectFTP(self):
        from ftplib import FTP
        #connessione ftp
        self.ftp=FTP(self.ftp_ip)
        self.ftp.login()
        self.ftp.cwd(self.dir_ftp)
        #download della lista dei file nella directory dir_ftp
        res_ftp=self.ftp.retrlines('NLST',self.all_file_xml.append)
        #print res_ftp
        print "connessione al server ftp riuscita!"
        res_ftp=res_ftp.split(' ')
        #calcolo file xml da scaricare
        num_el_xml=int(res_ftp[1])/2
        print "num_file xml=%d"% num_el_xml
    
    def downloadXMLs(self):
        self.__connectFTP()
        try:
            for name in self.all_file:
                if name.find("xml")!=-1:
                    new_file=open(self.dir_finale+name, 'wb')
                    self.ftp.retrbinary('RETR '+name, new_file.write)
                    new_file.close()
                    print 'download complete:'+name
                    
            self.ftp.quit()
        except:
            print('Error during download from FTP')
        print "download dei file xml completata"
        
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
    
        