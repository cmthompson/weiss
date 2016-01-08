# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:42:41 2015

@author: chris
"""
from ramanTools.RamanSpectrum import *
import numpy
from numpy import *
from matplotlib.pyplot import *


def findpeak(x,y,rnge,_plot=False,precision=0.01):
    x1 = numpy.argmin(abs(x-rnge[0]))
    x2 = numpy.argmin(abs(x-rnge[1]))
    if x1>x2:
        xtemp = x1
        x1=x2
        x2=xtemp
    yfit = numpy.polyfit(x[x1:x2],y[x1:x2],5)
    
    xs_fit = numpy.arange(rnge[0],rnge[1],precision)
    ys_fit = polyeval(yfit,xs_fit)
   
    if _plot:
        plot(xs_fit,ys_fit)
   
    xmax = xs_fit[argmax(ys_fit)]

    ymax=max(ys_fit)
    
    return (xmax,ymax)

def CdSconc(peak):
    diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
    print 'diam', diameter
    epsilon = 21536*diameter**2.3
    print 'eps', epsilon    
    print 'conc for 1 mm cuvette', peak[1]/epsilon 
    return peak[1]/epsilon 
    
def indivQY(UVVisfile, UVViscolumn, anthracenecolumn, fluorescencefile, anthracenefluorescencefile,
            UVVisplot=None, fluorplot=None,
            fluorescencerange = (410,473),
            nliq=1.333,
            day=0, label=None,color = 'k'):
    print '-------------------------------------'
    print 'calculating fluorescence yield for', label,'file', fluorescencefile
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    if len(UVViscolumn)==1:
        numuvviscolumn = alphabet.find(UVViscolumn)
    elif len(UVViscolumn)==2:
        numuvviscolumn = alphabet.find(UVViscolumn[0])*26+alphabet.find(UVViscolumn[1])
    
        
    
    a = loadtxt(UVVisfile, delimiter = ',', unpack = True, skiprows = 1,usecols=(0,numuvviscolumn,alphabet.find(anthracenecolumn)))
    
    a[1:]-=transpose([a[1:,0]])
    
   
    anthracene=RamanSpectrum(pandas.Series(a[2][::-1],a[0][::-1]))
    dot=RamanSpectrum(pandas.Series(a[1][::-1],a[0][::-1]))
    anthracene.smoothbaseline((290,300),(390,400))#anthracene.autobaseline((300,390),order=0)
    
    anthracene[:]-=anthracene[389]
    print 'ratio of anthracene absorbance at 350 to its absorbance at 374', anthracene[350]/anthracene[374], '0.6735'
   
    anthraceneabsorbance350= anthracene[350]#(anthracene[374]-anthracene[389])*0.6735# 
    absvalues = dot[350]
    
    nE = 1.359
    nQ = 1.44
    nW = 1.333  ## refractive index water    
 
    
    
    a = loadtxt(anthracenefluorescencefile,delimiter='\t', unpack = True,skiprows=1, usecols = (0,3))
    a[1]-=a[1,-1]
    anthracenefluorescence=RamanSpectrum(pandas.Series(a[1],a[0]))
    
     ###Normalizing to value of anthracene at 420 nm The area for the anthracene fluorescence is related to this value by 78.203    
    anthracenefluorescencearea = anthracenefluorescence[420]*78.2032212661
    print 'anthracene fluorescence area=', '%.2E' % anthracenefluorescencearea
    print anthracenefluorescence.calc_area((355,500))/anthracenefluorescence[420], 'ratio of total anthracene fluorescence area to value at 420' 
    
    oneminusTdot = 1-10**(-absvalues)   ##### gives the fraction of photons absorbed by dots
    
    oneminusT_anthracene350 =1-10**(-anthraceneabsorbance350)
    print 'anthracene absorbance at 350 nm:', anthraceneabsorbance350,'. Fraction photons absorbed:', oneminusT_anthracene350
    print 'dot absorbance at 350 nm:', absvalues, '. Fraction photons absorbed:', oneminusTdot

    
    a = loadtxt(fluorescencefile,delimiter='\t', unpack = True,skiprows=1, usecols = (0,3))
    hi = RamanSpectrum(pandas.Series(a[1],a[0]))
    hi[:]-=min(hi[400:500])
    hi[:]*=0.27/(1+0.00145*158)*oneminusT_anthracene350*nliq**2/nE**2 /anthracenefluorescencearea/ oneminusTdot 
    
    
    dotfluorescencearea = hi.calc_area(fluorescencerange,fill=False)
    
    
    ## quantum yield of dots using 0.27 as QY for anthracene with o2 quenching corrrection
    print  'fluorescence (bande edg) yield of dot', dotfluorescencearea
    
    if UVVisplot is not None:
       # anthracene.plot(ax=UVVisplot)#plot(a[0],anthracene)
        dot.plot(ax=UVVisplot,label=label)
    if fluorplot is not None:
        hi.plot(ax = fluorplot,label=label)
        #anthracenefluorescence.plot(ax = fluorplot,label=label)
        
        
    return  dotfluorescencearea
    
def indivCdSeQY(UVVisfile, UVViscolumn, rhodaminecolumn, fluorescencefile, rhodaminefluorescencefile,
                excitationwavelength = None,standardfluorescencerange=None, baselineabsorbanceat = None,
            UVVisplot=None, fluorplot=None,
            fluorescencerange = (410,473),
            nliq=1.333,
            day=0, label=None,color = 'k'):
    print '-------------------------------------'
    print 'calculating fluorescence yield for', label,'file', fluorescencefile
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    if len(UVViscolumn)==1:
        numuvviscolumn = alphabet.find(UVViscolumn)
    elif len(UVViscolumn)==2:
        numuvviscolumn = alphabet.find(UVViscolumn[0])*26+alphabet.find(UVViscolumn[1])
    
        
    
    a = loadtxt(UVVisfile, delimiter = ',', unpack = True, skiprows = 1,usecols=(0,numuvviscolumn,alphabet.find(rhodaminecolumn)))
    
    a[1:]-=transpose([a[1:,0]])
    
   
    anthracene=RamanSpectrum(pandas.Series(a[2][::-1],a[0][::-1]))
    dot=RamanSpectrum(pandas.Series(a[1][::-1],a[0][::-1]))
    
    if baselineabsorbanceat != None:
        dot-=dot[baselineabsorbanceat]
    
    anthracene[:]-=anthracene[600]
    
   
    anthraceneabsorbance350= anthracene[excitationwavelength]#(anthracene[374]-anthracene[389])*0.6735# 
    absvalues = dot[excitationwavelength]
    
    nE = 1.359
    nQ = 1.44
    nW = 1.333  ## refractive index water    
 
    
    
    a = loadtxt(rhodaminefluorescencefile,delimiter='\t', unpack = True,skiprows=1, usecols = (0,3))
    a[1]-=a[1,-1]
    standardfluorescence=RamanSpectrum(pandas.Series(a[1],a[0]))
    
     ###Normalizing to area of rhodamine B   
    standardfluorescencearea = standardfluorescence.calc_area(standardfluorescencerange)
    print 'standard fluorescence area=', '%.2E' % standardfluorescencearea
    
    oneminusTdot = 1-10**(-absvalues)   ##### gives the fraction of photons absorbed by dots
    
    oneminusT_anthracene350 =1-10**(-anthraceneabsorbance350)  ##### gives the fraction of photons absorbed by standard
    print 'anthracene absorbance at 520 nm:', anthraceneabsorbance350,'. Fraction photons absorbed:', oneminusT_anthracene350
    print 'dot absorbance at 520 nm:', absvalues, '. Fraction photons absorbed:', oneminusTdot

    
    a = loadtxt(fluorescencefile,delimiter='\t', unpack = True,skiprows=1, usecols = (0,3))
    hi = RamanSpectrum(pandas.Series(a[1],a[0]))
    hi[:]-=min(hi)
    hi[:]*=0.65*oneminusT_anthracene350*nliq**2/nE**2 /standardfluorescencearea/ oneminusTdot 
    
    
    dotfluorescencearea = hi.calc_area(fluorescencerange,fill=False)
    
    
    ## quantum yield of dots using 0.27 as QY for anthracene with o2 quenching corrrection
    print  'fluorescence (bande edg) yield of dot', dotfluorescencearea
    
    if UVVisplot is not None:
        #anthracene.plot(ax=UVVisplot))
        dot.plot(ax=UVVisplot,label=label)
    if fluorplot is not None:
        hi.plot(ax = fluorplot,label=label)
       # standardfluorescence.plot(ax = fluorplot,label=label)
        
        
    return  dotfluorescencearea