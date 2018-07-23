#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:58:17 2018

@author: angelozinna
"""

from EstrazioneH5 import EstrazioneH5
_data="2018-07-18"
data=_data.split("-")[0]+_data.split("-")[1]+_data.split("-")[2]
orario="110"
obj=EstrazioneH5(data=data,rang=0,tip='VIIRS-Day-Night-Band-SDR-Ellipsoid-Geo',dir_base='/home/angelozinna/Scrivania/dati/')
obj.createDirs()
obj.connectFTP()
obj.downloadXMLs()
'''
obj.extractTarAndGzInfoFromXMLByHour(orario)
print "tar potenzialmente buoni:", obj.getTarsPotenzialmenteBuoni()
print "gz potenzialmente buoni:", obj.getGZPotenzialmenteBuoni()
obj.downloadTars() 
obj.checkAllPotGoodGZFromTars()
'''
#obj.smartFindH5(_data,orario,3)
obj.secureFind(data)
h5=obj.findGoodH5InDict();
if(h5):
    obj.writeInFileGoodH5(h5)
