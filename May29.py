# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:56:45 2015

@author: chris
"""
from ramanTools.RamanSpectrum import *

def May20():  ### UVvis of stoichiometric CdSe
    a =  loadtxt('/home/chris/Documents/DataWeiss/150520/stoichiometric dots.csv', skiprows = 2, unpack = True,delimiter=',')
    a[1]-=a[1,0]
    a[1]/=0.132
    plot(a[0],a[1])
    title('stoichiometric dots 513nm 150520')
    return 0
    

def May28():  ##########UVVis of CdS dots
    a =  loadtxt('/home/chris/Documents/DataWeiss/150528/CdS dots.csv', skiprows = 2, unpack = True,delimiter=',')
    a[1]-=a[1,0]
    a[1]/=0.132
    plot(a[0],a[1])
    title('CdS dots 150527')
    return 0

def May29():
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150529/150529_05.txt')  ### exchanged CdS dots with phosphonic acid (octadecyl)
    r.autobaseline((147,1678), order =3)
    r.autobaseline((147,356), order = 1)
    r.autobaseline((356,389), order = 1, join = 'start')
    r.autobaseline((389,892), order = 1, join = 'start')
    r.autobaseline((892,923), order = 1, join = 'start')
    r.autobaseline((923,1185), order = 1, join = 'start')
    r.autobaseline((1185,1211), order = 1, join = 'start')
    r.autobaseline((1211,1678), order = 1, join = 'start')
    r.smooth()
    r.plot()
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150527/150527_06.txt')  ### native ligands CdS dots
   
    r.autobaseline((98,764), order = 1)
    r.autobaseline((764,839), order = 1, join = 'start')
    r.autobaseline((839,1700), order = 2, join = 'start')
    r.smooth()
    
    r.plot()
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150521/150521_05.txt')  ## stoichiometric ODPA capped CdSe
    r = removespikes(r)
    
    r.autobaseline((119,286), order = 0)
    r.autobaseline((286,1151), order = 4, join = 'start')
    r.autobaseline((1151,1489), order = 3, join = 'start')
    r.smooth()
    
    r.plot()
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150408/150408_02.txt')   # Cd enriched CdSe
    r = removespikes(r)
    r.autobaseline((272,1746), order = 2)
    #r.autobaseline((1151,1489), order = 3, join = 'start')
    r.plot()
    legend(['exchanged', 'oleate', 'stoich','rich'])
    ylim(-100,2000)
    

    return 0
    
def May29b():
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150521/150521_05.txt') ## stoichiometric ODPA capped CdSe
    r = removespikes(r)
    
    r.autobaseline((119,286), order = 0)
    r.autobaseline((286,1151), order = 4, join = 'start')
    r.autobaseline((1151,1489), order = 3, join = 'start')
    r.smooth()
    
    r.plot()
    
    
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150408/150408_02.txt')  # Cd enriched CdSe
    r = removespikes(r)
    r.autobaseline((272,1746), order = 2)
    #r.autobaseline((1151,1489), order = 3, join = 'start')
    r.plot()
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150516/150516_08.txt')  
    r = removespikes(r)
    
    r.autobaseline((272,1746), order = 2)
    
    r.smooth()
    
    r.plot()
    

    
    
    
    legend(['stoic', 'rich apr8', 'rich may16'])
    return 0
    
def June1():
    clf()
    subplot(122)
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150601/150601_07.txt')
    c = RamanSpectrum('/home/chris/Documents/DataWeiss/150601/150601_08.txt')
    
    r = add_RamanSpectra(r,c)
    r = SPIDcorrect633(r)
    r = removespikes(r)
    r.autobaseline((145,1148), order = 3)
    r.autobaseline((1148,1253), order = 1,join='start')
    r.autobaseline((1253,2000), order = 3,join='start')
    r.autobaseline((2000,3600), order = 3,join='start')
    r.values[:] = r.values[:]*5
    #r.smooth()
    
    r.plot()
    
    r= RamanSpectrum('/home/chris/Documents/DataWeiss/150601/150601_09.txt')
    c = RamanSpectrum('/home/chris/Documents/DataWeiss/150601/150601_10.txt')
    
    r = add_RamanSpectra(r,c)
    r = SPIDcorrect633(r)
    #r = removespikes(r)
    r.autobaseline((145,1148), order = 2)
    r.autobaseline((1148,1253), order = 1,join='start')
    r.autobaseline((1253,1700), order = 3,join='start')
    r.autobaseline((1700,3600), order = 3,join='start')
    r.values[:] = r.values[:]*5
    #r.smooth()
    r.plot()
    legend(['oleate', 'exchanged'])
    
    subplot(121)
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150529/150529_05.txt')
   
    r.autobaseline((147,2000), order =3)
    r.autobaseline((147,356), order = 1)
    r.autobaseline((356,389), order = 1, join = 'start')
    r.autobaseline((389,892), order = 1, join = 'start')
    r.autobaseline((892,923), order = 1, join = 'start')
    r.autobaseline((923,1185), order = 1, join = 'start')
    r.autobaseline((1185,1211), order = 1, join = 'start')
    r.autobaseline((1211,1679), order = 2, join = 'start')
    r.autobaseline((1679,1702), order = 2, join = 'start')
    r.autobaseline((1702,1900), order = 3, join = 'start')
    
    r.smooth()
    r.plot()
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150527/150527_06.txt')
    
    r = SPIDcorrect633(r)
    r.autobaseline((98,765), order = 4)
    r.autobaseline((765,839), order = 2, join = 'start')
    r.autobaseline((839,1456), order = 4, join = 'start')
    r.autobaseline((1456,1470), order = 2, join = 'start')
    r.autobaseline((1470,1900), order = 4, join = 'start')
    r.smooth()
    r.plot()
    
   
    legend(['exchanged', 'oleate'])
    return 0
    
def CdSvsCdSe():
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150521/150521_05.txt')
    r = removespikes(r)
    
    r.autobaseline((119,286), order = 0)
    r.autobaseline((286,1151), order = 4, join = 'start')
    r.autobaseline((1151,1560), order = 3, join = 'start')
    r.smooth()
    
    r.plot(label = 'CdSe')
    
    r = RamanSpectrum('/home/chris/Documents/DataWeiss/150601/150601_07.txt')
    c = RamanSpectrum('/home/chris/Documents/DataWeiss/150601/150601_08.txt')
    
    r = add_RamanSpectra(r,c)
    r = SPIDcorrect633(r)
    r = removespikes(r)
    r.autobaseline((145,1148), order = 3)
    r.autobaseline((1148,1253), order = 1,join='start')
    r.autobaseline((1253,2000), order = 3,join='start')
    r.autobaseline((2000,3600), order = 3,join='start')
    r.values[:] = r.values[:]*5
    #r.smooth()
    
    r.plot(label='CdS')
    legend(['CdSe','CdS'])
    return 0