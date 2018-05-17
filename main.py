#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:58:17 2018

@author: angelozinna
"""

from EstrazioneH5 import EstrazioneH5
_data="20180420"
orario="120"
obj=EstrazioneH5(data=_data,rang=1/float(3),dir_base='/Users/angelozinna/Desktop/university/3anno/tirocinio/dati/')
obj.createDirs()
obj.connectFTP()
#obj.downloadXMLs()
obj.extractTarAndGzFromXMLByHour(orario)
print "tar potenzialmente buoni:", obj.getTarsPotenzialmenteBuoni()
print "gz potenzialmente buoni:", obj.getGZPotenzialmenteBuoni()
#obj.downloadTars() 
obj.checkAllGZGoodOfTars()