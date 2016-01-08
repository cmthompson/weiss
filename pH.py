# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 13:49:57 2015

@author: chris
"""

added  = linspace(0,0.002,100)

#L_KOH =0.000008# 0.000015


def calcpH(L_KOH): 
    conc_KOH = 1

    molPPA = 0.1*0.000075
    dotbase = 0.000500*0.000020*200
    freebase = dotbase+added*0.01+ L_KOH*conc_KOH-2*molPPA
    subplot(121)
    plot(added,freebase)
    pH = ndarray(added.shape)
    pH[:] = 12
    pH[where(freebase<0)[0]] = 5 + log10(molPPA+freebase/-freebase)
    pH[where(molPPA-freebase>0)[0]] = 8.5 + log10(freebase/(molPPA-freebase))
    pH[where(freebase<0)[0]] = 5 + log10(molPPA+freebase/-freebase)
    subplot(122)
    plot(added/(0.002+added),pH,'s-')
    return 0
    
def calcpH_11(L_KOH): 
    conc_KOH = 1

    molPPA = 0.1*0.000075
    dotbase = 0.000500*0.000020*200
    freebase = dotbase+added*0.001+ L_KOH*conc_KOH-2*molPPA
    subplot(121)
    plot(added,freebase)
    pH = ndarray(added.shape)
    pH[:] = 12
    pH[where(freebase<0)[0]] = 5 + log10(molPPA+freebase/-freebase)
    pH[where(molPPA-freebase>0)[0]] = 8.5 + log10(freebase/(molPPA-freebase))
    pH[where(freebase<0)[0]] = 5 + log10(molPPA+freebase/-freebase)
    subplot(122)
    plot(added/(0.002+added),pH,'s-')
    return 0

#for i in [0.000030,0.000015,0.000008,0]:
#    calcpH(i)
#    legend(['30','15','8','0'])
#show()
clf()
concPPAinbuffer = 0.001
mLPPAsolinbuffer = 0.001
plot(added, 8.5+log10(added*0.001/(concPPAinbuffer*mLPPAsolinbuffer -added*0.001)))
show()