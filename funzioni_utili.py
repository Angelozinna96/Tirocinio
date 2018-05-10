#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:07:05 2018

@author: angelozinna
"""

def downloadXMLs(all_file,dir_finale,ftp):
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

def downloadTars(ftp_ip,tar_buoni,dir_ftp,dir_finale_h5):
    from pyftpclient import PyFTPclient
    from silence_stdout import nostdout
    with nostdout():
        client_ftp=PyFTPclient(ftp_ip,21,'','')
    for i,tar in enumerate(tar_buoni):
        with nostdout():
            client_ftp.DownloadFile(dir_ftp+tar,dir_finale_h5+tar)
    print "download completato del tar numero:",i+1

def checkH5File(dir_finale_h5,range_utile,latitudine,longitudine,gz,h5_buoni):
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

    
    #controlla se la latitudine è compresa tra i valori di inizio e fine della mat
    if(matrice_lat[0][shift] < latitudine < matrice_lat[-1][-shift] or matrice_lat[-1][-shift] < latitudine < matrice_lat[0][shift]):
        matrice_long=f[all_data][data]['Longitude']
        print "latitudine corrisponde"
        #controlla se la longitudine è compresa tra i valori 
        if(matrice_long[0][shift] < longitudine < matrice_long[-1][-shift] or matrice_long[-1][-shift] < longitudine < matrice_long[0][shift]):
            print "longitudine corrisponde"
            h5_buoni=gz[:-3]
        else:
            print "long non corrisponde"
    else:
        print "lat non corrisponde"
        
    return h5_buoni
