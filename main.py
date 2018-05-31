#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:58:17 2018

@author: angelozinna
"""

from EstrazioneH5 import EstrazioneH5
_data="20180527"
orario="111"
obj=EstrazioneH5(data=_data,rang=1/float(3),dir_base='/Users/angelozinna/Desktop/university/3anno/tirocinio/dati/')
obj.createDirs()
obj.connectFTP()
obj.downloadXMLs()
obj.extractTarAndGzInfoFromXMLByHour(orario)
print "tar potenzialmente buoni:", obj.getTarsPotenzialmenteBuoni()
print "gz potenzialmente buoni:", obj.getGZPotenzialmenteBuoni()
#obj.downloadTars() 
obj.checkAllPotGoodGZFromTars()
print "gz potenzialmente buoni:", obj.getGZPotenzialmenteBuoni()
h5=obj.findGoodH5InDict();
if(h5):
    obj.writeInFileGoodH5(h5)