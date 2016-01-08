# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:05:06 2015

@author: chris
"""
from scipy.optimize import curve_fit
from ramanTools.RamanSpectrum import *
from numpy import *
from matplotlib.pyplot import *
from UVVistools import indivQY,findpeak
from copy import deepcopy
import copy

from scipy.optimize import minimize
from matplotlib import gridspec
import os


    
def anthracenespectra():
     figure()
     ax1 = subplot(121)
     ax2 = subplot(122)
     
     a = loadtxt('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv',delimiter = ',', unpack = True, skiprows = 1,usecols=(0,8))
     b = loadtxt('/home/chris/Dropbox/DataWeiss/150929/150929UVVis.csv',delimiter = ',', unpack = True, skiprows = 1,usecols=(0,8))
     c = loadtxt('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv',delimiter = ',', unpack = True, skiprows = 1,usecols=(0,13))
     d = loadtxt('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', delimiter = ',', unpack = True, skiprows = 1,usecols=(0,7))
     e = loadtxt('/home/chris/Dropbox/DataWeiss/151002/151002UVVis.csv', delimiter = ',', unpack = True, skiprows = 1,usecols=(0,20))
     f = loadtxt('/home/chris/Dropbox/DataWeiss/151003/151003UVVis.csv', delimiter = ',', unpack = True, skiprows = 1,usecols=(0,19))
     g = loadtxt('/home/chris/Dropbox/DataWeiss/151005/151005UVVis.csv', delimiter = ',', unpack = True, skiprows = 1,usecols=(0,19))
     a = RamanSpectrum(pandas.Series(a[1][::-1],a[0][::-1]))
     b = RamanSpectrum(pandas.Series(b[1][::-1],b[0][::-1]))
     c = RamanSpectrum(pandas.Series(c[1][::-1],c[0][::-1]))
     d = RamanSpectrum(pandas.Series(d[1][::-1],d[0][::-1]))
     e = RamanSpectrum(pandas.Series(e[1][::-1],e[0][::-1]))
     f = RamanSpectrum(pandas.Series(f[1][::-1],f[0][::-1]))
     g = RamanSpectrum(pandas.Series(g[1][::-1],g[0][::-1]))
     
     
     afluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/150928/150928fluor/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     bfluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/150929/150929fluor/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     cfluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/150930/150930fluor/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     dfluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     efluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/151002/151002fluor/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     ffluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/151003/151003fluor/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     gfluor = RamanSpectrum(pandas.Series(*loadtxt('/home/chris/Dropbox/DataWeiss/151005/151005fluor/anthracene.dat',unpack = True, skiprows = 1,usecols=(3,0))))
     
     absorbance = array([])
     fluorescence= array([])
     for i in (a,b,c,d,e,f,g,):
        # i.autobaseline((314,390),order= 0)
         #i.plot(ax=ax1)
         i.smoothbaseline((290,300),(390,400),_plot=False,ax=ax1)
         
         print i[350]/i[400]
         print i[350]
         i.plot(ax=ax1)
         absorbance=numpy.append(absorbance,i[350])
     ax1.legend(['0','1','2','3','4','5','7'])
     ax1.set_ylim(0,0.1)
     
     
     fluorlist = (afluor,bfluor,cfluor,dfluor,efluor,ffluor,gfluor,)
#     for i in range(len(fluorlist)):
#         fluorlist[i][:]/=absorbance[i]
     for i in fluorlist:
         fluorescence=numpy.append(fluorescence,i[420]*78.2032212661)
         i.plot(ax=ax2)
     ax2.legend(['0','1','2','3','4'])
     figure()
     plot((1-10**(-absorbance))/fluorescence)
     
     
     return 0
#
#def fluorescenceyielddetermination():
#    f = loadtxt('/home/chris/Dropbox/DataWeiss/150930/150930fluor/anthracene.dat',delimiter='\t', unpack = True,skiprows=1, usecols = (0,3))
#    c = loadtxt('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv',delimiter = ',', unpack = True, skiprows = 1,usecols=(0,13))
#    c[1]-=c[1,0]
#    f = RamanSpectrum(pandas.Series(f[1]/10**12,f[0]))
#    fluarea = sum(f[350:550])
#    l= fluarea/f[420] 
#    
#    a = RamanSpectrum(pandas.Series(c[1][::-1],c[0][::-1]))
#    k =  0.27*(1+158*0.00145)*(1-10**-a[350])/fluarea
#    print l, '*fluorsecence at 420 = area of fluorescence'
#    print k, '*10^-12*areafluorescence/abs = quantum yield'
#    print k*l, '*10^-12*fluorescence(420)/abs(350nm) = quantum yield'
#    #Iant = l*Iant_420
#    #QYdot = (Idot*/Iant)*(1-10**-Adot)/(1-10**-Aant)*0.270*(1+158*0.00145)
#    return l

    
    
   
    
def trial3():
 
    sample1=list()
    sample2=list()
    sample3=list()
    sample4=list()
    sample5=list()
    sample6=list()
    PPAbuff=list()
    
    figure()
    Aax1 = subplot(231)
    Aax2 = subplot(232)
    Aax3 = subplot(233)
    Aax4 = subplot(234)
    Aax5 = subplot(235)
    Aax6 = subplot(236)
    
    figure()
    ax1 = subplot(231)
    ax2 = subplot(232)
    ax3 = subplot(233)
    ax4 = subplot(234)
    ax5 = subplot(235)
    ax6 = subplot(236)
   
    #day0 
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'b','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0N2pH7.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7'))
    sample2.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'c','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0N2pH9.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9'))
    sample3.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'd','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0N2pH11.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11'))
    sample4.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'e','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0airpH7.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7'))
    sample5.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'f','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0airpH9.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9'))
    sample6.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'g','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0airpH11.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11'))
    #PPAbuff.append(indivQY('/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv', 'u','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0PPAbuff.dat', '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/anthracene.dat',UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'PPAbuffer'))
    
    #day1
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151002/151002UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'n','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/t3d1N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'o','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/t3d1N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'p','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/t3d1N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'q','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/t3d1airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'r','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/t3d1airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 's','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial3/t3d1airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    #PPAbuff.append(indivQY('/home/chris/Dropbox/DataWeiss/151002/PPAbuffdots151002.csv', 'b','c','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial3/t3day0PPAbuff.dat', anthracenefile,UVVisplot = Aax1,fluorplot=ax1,day = 0,label = 'PPAbuffer'))
    ##day2
    day=2
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151003/151003fluor/anthracene.dat'
 
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151003/151003UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151003/151003fluor/trial3/'
    sample1.append(indivQY(uvvisfile, 'n','t',fluorfolder+'t3N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'o','t',fluorfolder+'t3N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'p','t',fluorfolder+'t3N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(0)#indivQY(uvvisfile, 'q','t',fluorfolder+'t3airpH7.dat', anthracenefile,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'q','t',fluorfolder+'t3airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'r','t',fluorfolder+'t3airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    #PPAbuff.append(indivQY(uvvisfile, 's','t',fluorfolder +'PPABuffDots.dat', anthracenefile,UVVisplot = Aax1,fluorplot=ax1,day = 0,label = 'PPAbuffer'))
    
    day=4
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151005/151005fluor/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151005/151005UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151005/151005fluor/trial3/'
    sample1.append(indivQY(uvvisfile, 'n','t',fluorfolder+'t3N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'o','t',fluorfolder+'t3N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'p','t',fluorfolder+'t3N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(0)#indivQY(uvvisfile, 'q','t',fluorfolder+'t3airpH7.dat', anthracenefile,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'q','t',fluorfolder+'t3airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'r','t',fluorfolder+'t3airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
  #  PPAbuff.append(indivQY(uvvisfile, 's','u',fluorfolder +'PPABuffDots.dat', anthracenefile,UVVisplot = Aax1,fluorplot=ax1,day = 0,label = 'PPAbuffer'))
  
  
    for p in (Aax1,Aax2,Aax3,Aax4,Aax5,Aax6,ax1,ax2,ax3,ax4,ax5,ax6): 
        p.legend(['0','1','2','3','4','5'])
    figure()
    days = [0,1,2,4]
    plot(days,sample1,'s-',label = 'N2pH7')
    plot(days,sample2,'s-',label = 'N2pH9')
    plot(days,sample3,'s-',label = 'N2pH11')
    plot(days,sample4,'s-',label = 'airpH7')
    plot(days,sample5,'s-',label = 'airpH9')
    plot(days,sample6,'s-',label = 'airpH11')
    plot(PPAbuff,'s-', label = 'PPAbuffered')
    legend()
    ylabel('band edge QY')
    xlabel('day')
    return 0
    
def trial1():
    ## day 0
    sample1=list()
    sample2=list()
    sample3=list()
    sample4=list()
    sample5=list()
    sample6=list()
    
    figure()
    Aax1 = subplot(231)
    Aax2 = subplot(232)
    Aax3 = subplot(233)
    Aax4 = subplot(234)
    Aax5 = subplot(235)
    Aax6 = subplot(236)
    
    figure()
    ax1 = subplot(231)
    ax2 = subplot(232)
    ax3 = subplot(233)
    ax4 = subplot(234)
    ax5 = subplot(235)
    ax6 = subplot(236)
    ##day0
    anthracenefile = '/home/chris/Dropbox/DataWeiss/150928/150928fluor/anthracene.dat'
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv', 'b','i','/home/chris/Dropbox/DataWeiss/150928/150928fluor/day0N2pH7.dat',  anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv', 'c','i','/home/chris/Dropbox/DataWeiss/150928/150928fluor/day0N2pH9.dat',  anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv', 'd','i','/home/chris/Dropbox/DataWeiss/150928/150928fluor/day0N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv', 'e','i','/home/chris/Dropbox/DataWeiss/150928/150928fluor/day0airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv', 'f','i','/home/chris/Dropbox/DataWeiss/150928/150928fluor/day0airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY('/home/chris/Dropbox/DataWeiss/150928/150928UVVis.csv', 'g','i','/home/chris/Dropbox/DataWeiss/150928/150928fluor/day0airpH11.dat',anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day1
    anthracenefile = '/home/chris/Dropbox/DataWeiss/150929/150929fluor/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/150929/150929UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'b','i','/home/chris/Dropbox/DataWeiss/150929/150929fluor/day1N2pH7.dat',  anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'c','i','/home/chris/Dropbox/DataWeiss/150929/150929fluor/day1N2pH9.dat',  anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'd','i','/home/chris/Dropbox/DataWeiss/150929/150929fluor/day1N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'e','i','/home/chris/Dropbox/DataWeiss/150929/150929fluor/day1airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'f','i','/home/chris/Dropbox/DataWeiss/150929/150929fluor/day1airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'g','i','/home/chris/Dropbox/DataWeiss/150929/150929fluor/day1airpH11.dat',anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day2
    anthracenefile = '/home/chris/Dropbox/DataWeiss/150930/150930fluor/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'b','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/day2N2pH7.dat',  anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'c','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/day2N2pH9.dat',  anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'd','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/day2N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'e','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/day2airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'f','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/day2airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'g','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/day2airpH11.dat',anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    
    ##day3
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'i','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/t1day3N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'j','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/t1day3N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'k','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/t1day3N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'l','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/t1day3airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'm','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/t1day3airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'n','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial1/t1day3airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day4
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/anthracene.dat'
 
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151002/151002UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'b','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/t1d4N2pH7.dat', anthracenefile,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'c','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/t1d4N2pH9.dat', anthracenefile,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'd','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/t1d4N2pH11.dat', anthracenefile,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'e','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/t1d4airpH7.dat', anthracenefile,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'f','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/t1d4airpH9.dat', anthracenefile,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'g','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial1/t1d4airpH11.dat', anthracenefile,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day5
    day=5
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151003/151003fluor/anthracene.dat'
 
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151003/151003UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151003/151003fluor/trial1/'
    sample1.append(indivQY(uvvisfile, 'b','t',fluorfolder+'t1N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'c','t',fluorfolder+'t1N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'd','t',fluorfolder+'t1N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'e','t',fluorfolder+'t1airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'f','t',fluorfolder+'t1airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'g','t',fluorfolder+'t1airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
     
      ##day7
    day=7
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151005/151005fluor/anthracene.dat'
 
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151005/151005UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151005/151005fluor/trial1/'
    sample1.append(indivQY(uvvisfile, 'b','t',fluorfolder+'t1N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'c','t',fluorfolder+'t1N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'd','t',fluorfolder+'t1N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'e','t',fluorfolder+'t1airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'f','t',fluorfolder+'t1airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'g','t',fluorfolder+'t1airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
        
    Aax1.legend(list((str(i) for i in range(6))))
    figure()
    days = [0,1,2,3,4,5,7]
    plot(days,sample1,'bs-',label = 'N2pH7')
    plot(days,sample2,'rs-',label = 'N2pH9')
    plot(days,sample3,'ks-',label = 'N2pH11')
    plot(days,sample4,'bo-',label = 'airpH7')
    plot(days,sample5,'ro-',label = 'airpH9')
    plot(days,sample6,'ko-',label = 'airpH11')
    legend()
    ylabel('band edge QY')
    xlabel('day')
    return 0
    
    
def trial2():
    ## day 0
    sample1=list()
    sample2=list()
    sample3=list()
    sample4=list()
    sample5=list()
    sample6=list()
    
    figure()
    Aax1 = subplot(231)
    Aax2 = subplot(232)
    Aax3 = subplot(233)
    Aax4 = subplot(234)
    Aax5 = subplot(235)
    Aax6 = subplot(236)
    
    figure()
    ax1 = subplot(231)
    ax2 = subplot(232)
    ax3 = subplot(233)
    ax4 = subplot(234)
    ax5 = subplot(235)
    ax6 = subplot(236)
    ##day0
    anthracenefile = '/home/chris/Dropbox/DataWeiss/150930/150930fluor/anthracene.dat'
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv', 'h','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/tri2N2pH7.dat',  anthracenefile,UVVisplot = Aax1, fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv', 'i','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/tri2N2pH9.dat',  anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv', 'j','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/tri2N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv', 'k','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/tri2airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv', 'l','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/tri2airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY('/home/chris/Dropbox/DataWeiss/150930/150930UVVis.csv', 'm','n','/home/chris/Dropbox/DataWeiss/150930/150930fluor/tri2airpH11.dat',anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day1
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151001/151001UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'o','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/t2day1N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'p','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/t2day1N2pH9.dat', anthracenefile,UVVisplot = Aax2, fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'q','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/t2day1N2pH11.dat',anthracenefile,UVVisplot = Aax3, fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'r','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/t2day1airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 's','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/t2day1airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 't','h','/home/chris/Dropbox/DataWeiss/151001/151001fluor/trial2/t2day1airpH11.dat',anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
     #day2
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/anthracene.dat'
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151002/151002UVVis.csv'
    sample1.append(indivQY(uvvisfile, 'h','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/t2d2N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'i','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/t2d2N2pH9.dat', anthracenefile,UVVisplot = Aax2, fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'j','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/t2d2N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'k','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/t2d2airpH7.dat',anthracenefile,UVVisplot = Aax4, fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'l','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/t2d2airpH9.dat',anthracenefile,UVVisplot = Aax5, fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'm','u','/home/chris/Dropbox/DataWeiss/151002/151002fluor/trial2/t2d2airpH11.dat',anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day3
    day=3
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151003/151003fluor/anthracene.dat'
 
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151003/151003UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151003/151003fluor/trial2/'
    sample1.append(indivQY(uvvisfile, 'h','t',fluorfolder+'t2N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'i','t',fluorfolder+'t2N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'j','t',fluorfolder+'t2N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'k','t',fluorfolder+'t2airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'l','t',fluorfolder+'t2airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'm','t',fluorfolder+'t2airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    
    ##day3
    day=5
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151005/151005fluor/anthracene.dat'
 
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151005/151005UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151005/151005fluor/trial2/'
    sample1.append(indivQY(uvvisfile, 'h','t',fluorfolder+'t2N2pH7.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r'))
    sample2.append(indivQY(uvvisfile, 'i','t',fluorfolder+'t2N2pH9.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r'))
    sample3.append(indivQY(uvvisfile, 'j','t',fluorfolder+'t2N2pH11.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r'))
    sample4.append(indivQY(uvvisfile, 'k','t',fluorfolder+'t2airpH7.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r'))
    sample5.append(indivQY(uvvisfile, 'l','t',fluorfolder+'t2airpH9.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r'))
    sample6.append(indivQY(uvvisfile, 'm','t',fluorfolder+'t2airpH11.dat', anthracenefile,UVVisplot = Aax6,fluorplot = ax6,day = 0,label = 'airpH11',color = 'r'))
    Aax1.legend(list((str(i) for i in range(6))))
    figure()
    plot(sample1,'o-',label = 'N2pH7')
    plot(sample2,'o-',label = 'N2pH9')
    plot(sample3,'o-',label = 'N2pH11')
    plot(sample4,'s-',label = 'airpH7')
    plot(sample5,'s-',label = 'airpH9')
    plot(sample6,'s-',label = 'airpH11')
    legend()
    ylabel('band edge QY')
    xlabel('day')
    
    return 0
    
    
def brandnewdotsOct6():
    sample1 = list()
    figure()
    ax1 = subplot(211)
    ax2 = subplot(212)
    
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151006/151006fluor/anthracene.dat'
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151006/fluorescenceyields.csv', 'f','i','/home/chris/Dropbox/DataWeiss/151006/151006fluor/oleate capped in hexanes.dat', anthracenefile,UVVisplot = ax1,fluorplot = ax2,day = 0,label = 'oleate capped',fluorescencerange = (400,470),nliq=1.37))
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151006/fluorescenceyields.csv', 'd','i','/home/chris/Dropbox/DataWeiss/151006/151006fluor/PPA-capped in water.dat', anthracenefile,UVVisplot = ax1,fluorplot = ax2,day = 0,label = 'PPAcapped',color = 'r',fluorescencerange = (400,470)))
    ax2.legend(['oleate capped', 'PPA-capped'])
    ax2.set_ylabel('differential QY')
    ax1.set_xlabel('wavelength (nm)')
    return 0
    
def brandnewdotsOct7():
    
    sample1 = list()
    figure()
    ax1 = subplot(211)
    ax2 = subplot(212)
    
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151006/fluorescenceyields.csv', 'f','i','/home/chris/Dropbox/DataWeiss/151006/151006fluor/oleate capped in hexanes.dat',  '/home/chris/Dropbox/DataWeiss/151006/151006fluor/anthracene.dat',UVVisplot = ax1,fluorplot = ax2,day = 0,label = 'oleate capped',fluorescencerange = (400,470),nliq=1.37))
    
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151007/151007fluor/anthracene.dat'
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151007/151007.csv', 'b','e','/home/chris/Dropbox/DataWeiss/151007/151007fluor/PPAcappedH2O.dat', anthracenefile,UVVisplot = ax1,fluorplot = ax2,day = 0,label = 'oleate capped',fluorescencerange = (406,470)))
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151007/151007.csv', 'c','e','/home/chris/Dropbox/DataWeiss/151007/151007fluor/PPAcapKOHHCl.dat', anthracenefile,UVVisplot = ax1,fluorplot = ax2,day = 0,label = 'PPAcapped',color = 'r',fluorescencerange = (406,470)))
    sample1.append(indivQY('/home/chris/Dropbox/DataWeiss/151007/151007.csv', 'd','e','/home/chris/Dropbox/DataWeiss/151007/151007fluor/MPAcappeddots.dat', anthracenefile,UVVisplot = ax1,fluorplot = ax2,day = 0,label = 'PPAcapped',color = 'r',fluorescencerange = (409,455)))
    
    
    for z in range(4):
        i = ax1.lines[z]
        r = findpeak(i.get_xdata(),i.get_ydata(),(410,420))
        print r
        i.set_ydata(i.get_ydata()/r[1])
        if z!=2:
            savetxt('/home/chris/Desktop/UVVisExchangedDots'+i.get_label()+str(z)+'.csv', transpose([i.get_xdata(),i.get_ydata()]),delimiter = ',')

    ax1.legend([',PPAhexanes', 'PPA H2O', 'PPA salt','MPA'])
    ax2.legend([',PPAhexanes', 'PPA H2O', 'PPA salt','MPA'])
    ax2.set_ylabel('differential QY')
    ax1.set_xlabel('wavelength (nm)')
    
    print 'PPA fluorescence to MPA fluorescence', sample1[1]/sample1[3]
    figure()
    plot(sample1, 's')
  
    return 0

def Oct12throughx():
    day=5
    
     ## day 0
    sample1=list()
    sample2=list()
    sample3=list()
    sample4=list()
    sample5=list()
    sample6=list()
    
    midgapemission = list()
    mg2=list()
    mg3=list()
    mg4=list()
    
    figure()
    Aax1 = subplot(231)
    Aax2 = subplot(232)
    Aax3 = subplot(233)
    Aax4 = subplot(234)
    Aax5 = subplot(235)
    Aax6 = subplot(236)
    
    figure()
    ax1 = subplot(231)
    ax2 = subplot(232)
    ax3 = subplot(233)
    ax4 = subplot(234)
    ax5 = subplot(235)
    ax6 = subplot(236)
    
    ax1.set_title('dot1N2')
    ax2.set_title('dot2N2')
    ax3.set_title('dot1air')
    ax4.set_title('dot2air')
    
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151012/151012fluor/anthracene.dat'
    
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151012/151012UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151012/151012fluor/'
    sample1.append(indivQY(uvvisfile, 'g','l',fluorfolder+'dot1N2.dat', anthracenefile,UVVisplot = Aax1, fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))
    sample2.append(indivQY(uvvisfile, 'h','l',fluorfolder+'dot2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = (406,474)))
    sample3.append(indivQY(uvvisfile, 'i','l',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = (406,474)))
    sample4.append(indivQY(uvvisfile, 'j','l',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = (406,474)))
    sample5.append(indivQY(uvvisfile, 'm','l',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (412,470)))
    
    
    fr = (474,680)
    midgapemission.append(indivQY(uvvisfile, 'g','l',fluorfolder+'dot1N2.dat', anthracenefile,UVVisplot = Aax1, fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange =fr))
    mg2.append(indivQY(uvvisfile, 'h','l',fluorfolder+'dot2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = fr))
    mg3.append(indivQY(uvvisfile, 'i','l',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = fr))
    mg4.append(indivQY(uvvisfile, 'j','l',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange =fr))
    #sample5.append(indivQY(uvvisfile, 'm','l',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (412,470)))
  
    
    
    
    ############################################################
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151013/151013fluor/anthracene.dat'
    
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151013/151013UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151013/151013fluor/'
    sample1.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dots1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))    
    sample2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dots2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = (406,474)))
    sample3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = (406,474)))
    sample4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = (406,474)))
    sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dot2swithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
    fr = (474,680)
    midgapemission.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dots1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = fr))
    mg2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dots2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = fr))
    mg3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = fr))
    mg4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = fr))
    #sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dot2swithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
        
    ###################################################
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151014/151014fluor/anthracene.dat'
    
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151014/151014UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151014/151014fluor/'
    sample1.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dot1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))
    sample2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dot2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = (406,474)))
    sample3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = (406,474)))
    sample4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = (406,474)))
    sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
    fr = (474,680)
    midgapemission.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dot1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = fr))
    mg2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dot2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = fr))
    mg3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = fr))
    mg4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = fr))
    #sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
     ###################################################
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151015/151015fluor/anthracene.dat'
    
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151015/151015UVvis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151015/151015fluor/'
    sample1.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dot1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))
    sample2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dot2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = (406,474)))
    sample3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = (406,474)))
    sample4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = (406,474)))
    sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
    fr = (474,680)
    midgapemission.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dot1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = fr))
    mg2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dot2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = fr))
    mg3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = fr))
    mg4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = fr))
    #sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
       ###################################################
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151016/151016fluor/anthracene.dat'
    
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151016/151016UVVis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151016/151016fluor/'
    sample1.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dots1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))
    sample2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dots2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = (406,474)))
    sample3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dots1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = (406,474)))
    sample4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = (406,474)))
    sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    fr = (474,680)
    #sample1.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dots1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))
    midgapemission.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dots1N2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = fr))
    mg2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dots2N2.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = fr))
    mg3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dots1air.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = fr))
    mg4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = fr))
    #sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
          
     
     ###################################################
    anthracenefile = '/home/chris/Dropbox/DataWeiss/151017/151017fluor/anthracene.dat'
    
    uvvisfile = '/home/chris/Dropbox/DataWeiss/151017/151017UVvis.csv'
    fluorfolder = '/home/chris/Dropbox/DataWeiss/151017/151017fluor/'
    sample1.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dot1n2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = (406,474)))
    sample2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dot2n22.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = (406,474)))
    sample3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air2.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = (406,474)))
    sample4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = (406,474)))
    sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
    fr= (474,680)
    
    midgapemission.append(indivQY(uvvisfile, 'b','g',fluorfolder+'dot1n2.dat', anthracenefile,UVVisplot = Aax1,fluorplot = ax1,day = 0,label = 'N2pH7',color = 'r',fluorescencerange = fr))
    mg2.append(indivQY(uvvisfile, 'c','g',fluorfolder+'dot2n22.dat', anthracenefile,UVVisplot = Aax2,fluorplot = ax2,day = 0,label = 'N2pH9',color = 'r',fluorescencerange = fr))
    mg3.append(indivQY(uvvisfile, 'd','g',fluorfolder+'dot1air2.dat', anthracenefile,UVVisplot = Aax3,fluorplot = ax3,day = 0,label = 'N2pH11',color = 'r',fluorescencerange = fr))
    mg4.append(indivQY(uvvisfile, 'e','g',fluorfolder+'dot2air.dat', anthracenefile,UVVisplot = Aax4,fluorplot = ax4,day = 0,label = 'airpH7',color = 'r',fluorescencerange = fr))
    #sample5.append(indivQY(uvvisfile, 'f','g',fluorfolder+'dotswithKCl.dat', anthracenefile,UVVisplot = Aax5,fluorplot = ax5,day = 0,label = 'airpH9',color = 'r',fluorescencerange = (406,474)))
    
    
    n2samples = mean([array(sample1)/sample1[0],array(sample2)/sample2[0]],axis = 0)
    airsamples = mean([array(sample3)/sample3[0],array(sample4)/sample4[0]],axis = 0)
    
    figure()
    plot(sample1,'ko-',label = 'dot1N2')
    plot(midgapemission,'k--',label='midgap')
    plot(sample2,'ks-',label = 'dot2N2')
    plot(sample3,'ro-',label = 'dot1air')
    plot(mg3,'r--',label='mg3')
    plot(sample4,'rs-',label = 'dot2air')
    plot(sample5,'bs-',label = 'dots with KCl')
    plot(mg2,'k--',label='mg2')
    plot(mg4,'r--',label='mg4')
       
    legend()
    ylabel('band edge QY')
    xlabel('day')
    ylim(0,0.0009)
    
    fig4 = figure()
    plot(n2samples,label='N$_2')
    plot(airsamples,label='air')
    def exponentialdecay(x,r,A0,Ainf):return (A0-Ainf)*exp(r*x)+Ainf
    fit = curve_fit(exponentialdecay,arange(0,6),n2samples,[-1,0.7,0.3])
    plot(arange(0,6,0.1),exponentialdecay(arange(0,6,0.1),*fit[0]),'r--')
    print 'n2',fit[0],np.sqrt(np.diag(fit[1]))
    
    fit = curve_fit(exponentialdecay,arange(0,6),airsamples,[-1,0.7,0.3])
    plot(arange(0,6,0.1),exponentialdecay(arange(0,6,0.1),*fit[0]),'k--')
    print 'air',fit,np.sqrt(np.diag(fit[1]))
    legend()
    ylabel('Normalized band edge QY')
    xlabel('day')
    ylim(0,1.1)
    Aax1.legend(list((str(i) for i in range(6))))
    i = 1
    for l in fig4.axes[0].lines:
        
        name = 'stabilityfigure'+str(i)+'.txt'
        savetxt('/home/chris/Desktop/'+name,transpose([l.get_xdata(),l.get_ydata()]))
        i+=1
    
    for l in ax2.lines:
        name = 'stabilityfigurefluorescence'+str(i)+'.txt'
        savetxt('/home/chris/Desktop/'+name,transpose([l.get_xdata(),l.get_ydata()]))
        i+=1
    for l in Aax4.lines:
        xx = l.get_xdata()
        x1 = argmin(abs(xx-480))
        
        yy=l.get_ydata()
        yy[:]-=yy[x1]
        x = findpeak(xx,yy,(400,420))
        B=x[0]
        d=-0.000000066521*B**3+0.00019557*B**2-0.092352*B+13.29
        eps =21536*d**2.3
        print 'conc', x[1]/eps
        name = 'stabilityfigureabsorbance'+str(i)+'.txt'
        savetxt('/home/chris/Desktop/'+name,transpose([l.get_xdata(),l.get_ydata()]))
        i+=1
   
    

    


    return 0