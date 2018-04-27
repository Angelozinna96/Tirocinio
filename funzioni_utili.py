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

