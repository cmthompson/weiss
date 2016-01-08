# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:08:39 2015

@author: chris
"""
from ramanTools.RamanSpectrum import *
from UVVistools import *
def Dec15():
    cla()
    ODPARef.plot()
    OPARef.plot()
    
    ax = subplot(111)
    a = RamanSpectrum('/home/chris/Dropbox/DataWeiss/151215/151215_04.txt')#,name='DMF 65 mM')
    a.autobaseline((295,350,473,580,755,988,1188,1317,1756,1853,2296,2400,2600),join='end',order = 8,specialoption='points')    
    a.plot()
    b=RamanSpectrum('/home/chris/Dropbox/DataWeiss/151215/151215_02.txt')#,name='7uM PPAcapped dots in water/DMF')
    b[:]/=3
    b.autobaseline((295,350,473,580,755,961,1317,1756,1853,2296,2400,2600),join='end',order = 8,specialoption='points')    
    b.plot()
    c=RamanSpectrum('/home/chris/Dropbox/DataWeiss/151215/151215_05.txt')#,name = 'PPA')
   
    c.autobaseline((295,350,473,580,755,961,1317,1756,1853,2296,2400,2600),join='end',order = 8,specialoption='points')    
    c.plot()
    
    
    quickoffset(ax,rnge=(200,1600))
    return 0 
    
def Dec18_CdSePPAFluorescence():
    rhodaminefluorescencefile = '/home/chris/Dropbox/DataWeiss/151218/151218fluor/RhodamineB.dat'
    
    print "finding concentration of stock solution of dots in hexanes"
    
    a = loadtxt('/home/chris/Dropbox/DataWeiss/151218/KedysOleateDots.csv',unpack=True,skiprows = 1,delimiter=',')
    x617=argmin(abs(a[0]-617))
    
    i=a[1]   
    i-=i[x617]
    r = findpeak(a[0],i,(570,590))
    B2=r[0]
    d=0.0000000016122*B2**4-0.0000026575*B2**3+0.0016242*B2**2-0.4277*B2+41.57
    eps=5857*d**2.65
    conc = r[1]/eps
    absorbancestockdots = r[1]*1875/58
    print "concentraiton of dots in oleate, diluted 58:1875 :", conc
    print "absorbance at peak of stock dots would be",absorbancestockdots
    print "concentraiton of stock solution dots in oleate:", conc*1875/58
    
    ax1 = subplot(111)
    fluorescencerange = (545,660)
    
    a = loadtxt('/home/chris/Dropbox/DataWeiss/151218/OleateDotsCdSeTransferedToWaterForFluorescence.csv',unpack=True,skiprows = 1,delimiter=',')
    x617=argmin(abs(a[0]-617))
    for x in range(1,6):
        massofdotsfinal=[]
        i = a[x]
        i-=i[x617]
        r = findpeak(a[0],i,(570,590))
        B2=r[0]
        d=0.0000000016122*B2**4-0.0000026575*B2**3+0.0016242*B2**2-0.4277*B2+41.57
        eps=5857*d**2.65
        conc = r[1]/eps
        print "concentration of dots, absorbance of dots:", conc, r[1]
        
    
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/OleateDotsCdSeTransferedToWaterForFluorescence.csv', 'b', 'g', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/OleateCdSe.dat', rhodaminefluorescencefile,
            UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
            fluorescencerange = (530,660) ,baselineabsorbanceat=617,
            nliq=1.359,
            day=0, label=None,color = 'k')
            
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/OleateDotsCdSeTransferedToWaterForFluorescence.csv', 'c', 'g', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/PPACdSeVial1.dat', rhodaminefluorescencefile,
            UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
            fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
            nliq=1.333,
            day=0, label=None,color = 'k')
            
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/OleateDotsCdSeTransferedToWaterForFluorescence.csv', 'd', 'g', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/PPACdSeVial2.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
        
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/OleateDotsCdSeTransferedToWaterForFluorescence.csv', 'e', 'g', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/PPACdSeVial3.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
        
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/OleateDotsCdSeTransferedToWaterForFluorescence.csv', 'f', 'g', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/PPACdSeVial4.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
       ######################### 
        
        
    ##### samples after I changed pH to near 7
    fig = figure()
    ax1 = fig.add_subplot(111)
    
    rhodaminefluorescencefile = '/home/chris/Dropbox/DataWeiss/151218/151218fluor/pH7RhodamineB.dat'
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/PPADotsCdSepH7.csv', 'c', 'b', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/pH7CdSeVial1.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/PPADotsCdSepH7.csv', 'd', 'b', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/pH7CdSeVial2.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
        
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/PPADotsCdSepH7.csv', 'e', 'b', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/pH7CdSeVial3.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
    indivCdSeQY('/home/chris/Dropbox/DataWeiss/151218/PPADotsCdSepH7.csv', 'f', 'b', '/home/chris/Dropbox/DataWeiss/151218/151218fluor/pH7CdSeVial4.dat', rhodaminefluorescencefile,
        UVVisplot=ax1, fluorplot=ax1,excitationwavelength=520,standardfluorescencerange=(450,600),
        fluorescencerange = fluorescencerange,baselineabsorbanceat=617,
        nliq=1.333,
        day=0, label=None,color = 'k')
    return 0
    