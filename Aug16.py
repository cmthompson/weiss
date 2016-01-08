# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:51:17 2015

@author: chris
"""

from scipy.optimize import curve_fit
from ramanTools.RamanSpectrum import *
from numpy import *
from matplotlib.pyplot import *
from copy import deepcopy
import copy
from matplotlib.font_manager import FontProperties
from scipy.optimize import minimize
from matplotlib import gridspec
from UVVistools import *


def Aug16():  ## CdS dots synthesized August 16 UVVis and fluorescence
     a =   loadtxt('/home/chris/Dropbox/DataWeiss/150816/dotsaug16UVVis.csv',delimiter = ',',skiprows=1,unpack=True)
    
     plot(a[0],a[1])
     
     b =   loadtxt('/home/chris/Dropbox/DataWeiss/150816/Aug16_synthCdS_Fluorescence.csv',unpack = True,delimiter = ',',skiprows=0)
     fluor = RamanSpectrum(pandas.Series(b[3],b[0]))
     fluor[:]-=min(fluor)
     fluor[:]/=max(fluor)
     fluor.plot()
     r = fitspectrum(fluor,(400,484),'xGaussian',[1,0.2,433,450,50,15,0,0])
     plot(r.x,r.y)
     for i in r.peaks:
         plot(r.x,i)
     print 'fluorescence lambda max =',r.params[0][2] 

     print 'width=', 2*sqrt(-r.params[0][4]*log(0.5)),'nm'
     
     return 0
     
def Aug17():  ## CdS dots synthesized August 17 UVVis and fluorescence
     a =   loadtxt('/home/chris/Dropbox/DataWeiss/150817/UVVisAug17CdSdots.csv',delimiter = ',',skiprows=1,unpack=True)
    
     plot(a[0],a[1])
     
     b =   loadtxt('/home/chris/Dropbox/DataWeiss/150817/CdSeAug17d1.csv',unpack = True,delimiter = ',',skiprows=1)
     fluor = RamanSpectrum(pandas.Series(b[3],b[0]))
     fluor[:]-=min(fluor)
     fluor[:]/=max(fluor)
     fluor.plot()
     r = fitspectrum(fluor,(400,484),'xGaussian',[1,0.2,433,450,50,15,0,0])
     plot(r.x,r.y)
     for i in r.peaks:
         plot(r.x,i)
     print 'fluorescence lambda max =',r.params[0][2] 

     print 'width=', 2*sqrt(-r.params[0][4]*log(0.5)),'nm'
     
     return 0

def Aug18():  ## CdS dots capped with phosphonopropionic acid and mercaptopropionic acid.  UVVis and fluorescence
     clf()
     font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 20}

     matplotlib.rc('font', **font)
     

     a =   loadtxt('/home/chris/Dropbox/DataWeiss/150818/CdSdotsinwaterforfluorescence.csv',delimiter = ',',skiprows=1,unpack=True)
     nm400 = argmin(abs(a[0]-400))
     a[1]-=a[1][0]
     
     a[3]-=a[3][0]
     PPAtoMPAratio = a[1][nm400]/a[3][nm400]
     plot(a[0],a[1])
     plot(a[0],a[3])
     legend(['PPA for fluorescence', 'MPA for fluorescence'])
     vlines(400,0,1)
     figure()
     font0 = FontProperties()
     font0.set_size('large')
     font0.set_family('fantasy')
     
  
     alignment = {'horizontalalignment':'center', 'verticalalignment':'baseline'}
###  Show family options
     
     b =   loadtxt('/home/chris/Dropbox/DataWeiss/150818/FluorescenceData.csv',unpack = True,delimiter = ',',skiprows=1)
     b[1]-=b[3]
     
     b[2]-=b[3]
     b[4]-=b[6]
     b[5]-=b[6]
     
     for i in [1,2,4,5]:
         b[i]-=b[i][-1]
     b[1]*=PPAtoMPAratio
     b[4]*=PPAtoMPAratio
    
#     for i in [1,2,4,5]:
#         plot(b[0],b[i])
#     xlabel('wavelength')
#     ylabel('intensity')
#     legend(['MPA1','PPA1','MPA2','PPA2'])
     
         
     plot(b[0],b[2],linewidth = 2,color = 'k')
     plot(b[0],b[1],linewidth = 2,color = 'r')
     xlabel('Wavelength (nm)',fontsize = 20)
     ylabel('Intensity (a.u)',fontsize = 20)
     yticks([])
    
     legend(['PPA-capped QDs','MPA-capped QDs'],fontsize = 20)
     ylim(0,700000)
     
    
     
     return 0

def pHdepfluorescence(): ### August 20
    water = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/water1waterd1.dat','\t', unpack=True)
    pH13 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH131pH13d1.dat','\t', unpack=True)
    pH12 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH121pH12d1.dat', delimiter ='\t', unpack=True)
    pH11 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH111pH11d1.dat', delimiter ='\t', unpack=True)
    pH10 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH101pH10d1.dat', delimiter ='\t', unpack=True)
    pH85 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH8pt51pH8pt5d1.dat', delimiter ='\t', unpack=True)
    pH7 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH71pH7d1.dat', delimiter ='\t', unpack=True)
    pH5 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH51pH5d1.dat', delimiter ='\t', unpack=True)
    pH4 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1Fluorescence/pH4d1.csv', delimiter =',', unpack=True)
    UVVis = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial1UVVis/pH dependence of UVVis.csv',delimiter=',',skiprows = 1, unpack=True)
    
    
    
    xpeaks = list()
    ypeaks = list()
    absxpeaks =list()
    absypeaks=list()
    normalizationvalues = list()
    
       
    
   
    figure()
    ax1=subplot(111)
    title('UVVis')
    x2 = argmin(abs(UVVis[0]-415))
    x1= argmin(abs(UVVis[0]-430))
    x400 = argmin(abs(UVVis[0]-400))

    for z in UVVis[1:]:
        z-=z[0]
        
        normalizationvalues.append(z[x400])
        r   = polyfit(UVVis[0][x1:x2],z[x1:x2],2)
        xs = arange(415,435,0.1)
       
        absxpeaks.append(xs[argmax(polyeval(r,xs))])
        absypeaks.append(max(polyeval(r,xs)))
       
        plot(UVVis[0],z)
    

    legend(['13','12','11','10','8.5','7','5','4'])
    
    figure()
    title('fluorescence spectra')
    slist = [pH13,pH12,pH11,pH10,pH85,pH7,pH5,pH4]
    f = array(list(i[3] for i in slist))
    f[:]-=water[3]
    print f.shape
    print array([pH13[0]]).shape
    f = append(array([pH13[0]]),f,axis=0)
    for i in range(len(slist)):
        z=slist[i]
        z[3] = SGsmooth(z[0],z[3])
        z[3]-=water[3]
        
        z[3]/=normalizationvalues[i]
        plot(z[0],z[3])
        if i<6:
            r   = polyfit(z[0][23:33],z[3][23:33],3)
            xs = arange(420,450,0.1)
            #plot(xs,polyeval(r,xs))
            xpeaks.append(xs[argmax(polyeval(r,xs))])
            ypeaks.append(max(polyeval(r,xs)))
    legend(['13','12','11','10','8.5','7','5','4'])
    plot(xpeaks,ypeaks,'s-')
    savetxt('/home/chris/Desktop/UVVis.txt', transpose(UVVis), header='pH13 pH12 pH11 pH10 pH8.5 pH7 pH5 pH4' )
    savetxt('/home/chris/Desktop/Fluor.txt', transpose(f), header='pH13 pH12 pH11 pH10 pH8.5 pH7 pH5 pH4' )
        
        
#    
    figure()
    title('peak positions')
    plot([13,12,11,10,8.5,7],xpeaks,'s-')
    plot([13,12,11,10,8.5,7],absxpeaks[:-2],'s-')
    xlabel('pH')
    ylabel('peak position (nm)')
    legend(['fluorescence', 'absorption'])
    return (xpeaks,absxpeaks[:-2])
    
def pHdepfluorescenceTrial2(): ### August 20
    water = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/water.dat','\t', unpack=True)
    pH13 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH13.dat','\t', unpack=True)
    pH12 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH12.dat', delimiter ='\t', unpack=True)
    pH11 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH11.dat', delimiter ='\t', unpack=True)
    pH10 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH10.dat', delimiter ='\t', unpack=True)
    pH85 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH8pt5.dat', delimiter ='\t', unpack=True)
    pH7 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH7.dat', delimiter ='\t', unpack=True)
    pH5 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH5.dat', delimiter ='\t', unpack=True)
    pH4 = loadtxt('/home/chris/Dropbox/DataWeiss/150820/Trial2Fluorescence/pH4.dat', delimiter ='\t', unpack=True)
    UVVis = loadtxt('/home/chris/Dropbox/DataWeiss/150820/trial2uvvis/pH dependence trial2.csv',delimiter=',',skiprows = 1, unpack=True)
    
    xpeaks = list()
    ypeaks = list()
    absxpeaks =list()
    absypeaks=list()
    normalizationvalues = list()
    
       
    
   
    figure()
    title('UVVis')
    x2 = argmin(abs(UVVis[0]-415))
    x1= argmin(abs(UVVis[0]-430))
    x400 = argmin(abs(UVVis[0]-400))
    

    for z in UVVis[1:]:
        #z-=z[0]
        peak = findpeak(UVVis[0], z,(390,420))
        print peak
        normalizationvalues.append(z[x400])
        r   = polyfit(UVVis[0][x1:x2],z[x1:x2],2)
        xs = arange(415,435,0.1)
       
        absxpeaks.append(xs[argmax(polyeval(r,xs))])
        absypeaks.append(max(polyeval(r,xs)))
       
        plot(UVVis[0],z)
  

    legend(['13','12','11','10','8.5','7','5','4'])
    
    figure()
    title('fluorescence spectra')
    slist = [pH13,pH12,pH11,pH10,pH85,pH7,pH5,pH4]
    for i in range(len(slist)):
        z=slist[i]
        z[3] = SGsmooth(z[0],z[3])
        z[3]-=water[3]
        
        z[3]/=normalizationvalues[i]
        plot(z[0],z[3])
        if i<6:
            r   = polyfit(z[0][23:33],z[3][23:33],3)
            xs = arange(420,450,0.1)
            #plot(xs,polyeval(r,xs))
            xpeaks.append(xs[argmax(polyeval(r,xs))])
            ypeaks.append(max(polyeval(r,xs)))
    legend(['13','12','11','10','8.5','7','5','4'])
    plot(xpeaks,ypeaks,'s-')
    
    figure()
    title('peak positions')
    plot([13,12,11,10,8.5,7],xpeaks,'s-')
    plot([13,12,11,10,8.5,7],absxpeaks[:-2],'s-')
    xlabel('pH')
    ylabel('peak position (nm)')
    legend(['fluorescence', 'absorption'])
    return (xpeaks,absxpeaks[:-2])
        

    return (xpeaks,absxpeaks[:-2])
    
def nmtomeV():  ### August 20 data converted to meV
    
    a = [13,12,11,10,8.5,7]
    b= array(pHdepfluorescenceTrial2())
    c = array(pHdepfluorescence())
    d = array(MPAdots_pHdep())
   
    average_fluorshift = (1240000/b[0]+ 1240000/c[0]-1240000/b[0][0]-1240000/c[0][0])/2
    average_absshift = (1240000/b[1]+ 1240000/c[1]-1240000/b[1][0]-1240000/c[1][0])/2

    
    b[0] = 1240000/b[0]-1240000/d[1][0]
    b[1] = 1240000/b[1]-1240000/d[1][0]
    c[0] = 1240000/c[0]-1240000/d[1][0]
    c[1] = 1240000/c[1]-1240000/d[1][0]
    d[1] = 1240000/d[1]-1240000/d[1][0]
    
    figure()
    print c[1]
    plot(a,c[0],'s-')
    plot(a,c[1],'s-')
    plot(a,b[0],'s-')
    plot(a,b[1],'s-')
    plot([13,12,11,10,8.5,7,5,4,3],d[1],'s-')
    
    savetxt('/home/chris/Desktop/nmtoeV.txt', transpose([a,average_absshift,average_fluorshift ]),header = 'pH absorbance_peak_(nm) fluorescence_peak_(nm)') 
    
    legend(['fluorPPA1','absPPA1','fluorPPA2','absPPA2','absMPA'])
    xlabel('pH')
    ylabel('shift in band gap (meV)')
    return 0
    
def reversibilityAug20():
    UVVis=loadtxt('/home/chris/Dropbox/DataWeiss/150820/pH Reversibility.csv',delimiter=',', unpack =True, skiprows = 1)
    figure()
    title('UVVis')
    absxpeaks = list()
    absypeaks=list()
    x2 = argmin(abs(UVVis[0]-415))
    x1= argmin(abs(UVVis[0]-430))
    x400 = argmin(abs(UVVis[0]-400))
    subplot(121)
    for z in UVVis[1:]:
        
        r   = polyfit(UVVis[0][x1:x2],z[x1:x2],2)
        xs = arange(415,435,0.1)
       
        absxpeaks.append(xs[argmax(polyeval(r,xs))])
        absypeaks.append(max(polyeval(r,xs)))
       
        plot(UVVis[0],z)
    pHs = [12,5,11,7,12,7,11,4,3,12]
    subplot(122)
    plot(absxpeaks)
    savetxt('/home/chris/Desktop/reversibility.txt',transpose([array(pHs),array(absxpeaks)]),header = 'pH, lambda_max')
    for i in range(len(pHs)):
        annotate(str(pHs[i]), (i,absxpeaks[i]), fontsize = 20)
    return 0
    
def MPAdots_pHdep(): ### August 20
    os.chdir('/home/chris/Dropbox/DataWeiss/150824/MPAdotsfluorescence')
    water = loadtxt('water.dat','\t', unpack=True)
    pH13 = loadtxt('pH13.dat','\t', unpack=True)
    pH12 = loadtxt('pH12.dat', delimiter ='\t', unpack=True)
    pH11 = loadtxt('pH11.dat', delimiter ='\t', unpack=True)
    pH10 = loadtxt('pH10.dat', delimiter ='\t', unpack=True)
    pH85 = loadtxt('pH8.dat', delimiter ='\t', unpack=True)
    pH7 = loadtxt('pH7.dat', delimiter ='\t', unpack=True)
    pH5 = loadtxt('pH5.dat', delimiter ='\t', unpack=True)
    pH4 = loadtxt('pH4.dat', delimiter ='\t', unpack=True)
    pH3 = loadtxt('pH4.dat', delimiter ='\t', unpack=True)
    UVVis = loadtxt('/home/chris/Dropbox/DataWeiss/150824/MPAdotsUVVis/MPA capped dots pH dependence.csv',delimiter=',',skiprows = 1, usecols = [0,1,2,3,4,5,6,7,9,10],unpack=True)
    
    xpeaks = list()
    ypeaks = list()
    absxpeaks =list()
    absypeaks=list()
    normalizationvalues = list()
    
       
    
   
    figure()
    title('UVVis')
    x2 = argmin(abs(UVVis[0]-415))
    x1= argmin(abs(UVVis[0]-430))
    x400 = argmin(abs(UVVis[0]-400))

    for z in UVVis[1:]:
        z-=z[0]
        normalizationvalues.append(z[x400])
        z/=z[x400]
        r   = polyfit(UVVis[0][x1:x2],z[x1:x2],2)
        xs = arange(415,435,0.1)
       
        absxpeaks.append(xs[argmax(polyeval(r,xs))])
        absypeaks.append(max(polyeval(r,xs)))
       
        plot(UVVis[0],z)
  

    legend(['13','12','11','10','8.5','7','5','4','3'])
    
    figure()
    title('fluorescence spectra')
    slist = [pH13,pH12,pH11,pH10,pH85,pH7,pH5,pH4,pH3]
    for i in range(len(slist)):
        z=slist[i]
        z[3] = SGsmooth(z[0],z[3])
        z[3]-=water[3]
        
        z[3]/=normalizationvalues[i]
        plot(z[0],z[3])
        if i<16:
            r   = polyfit(z[0][23:33],z[3][23:33],3)
            xs = arange(427,450,0.1)
            #plot(xs,polyeval(r,xs))
            xpeaks.append(xs[argmax(polyeval(r,xs))])
            ypeaks.append(max(polyeval(r,xs)))
    legend(['13','12','11','10','8.5','7','5','4','3'])
    plot(xpeaks[4:7],ypeaks[4:7],'s-')
    
    figure()
    title('peak positions')
    plot([10,8,7],xpeaks[4:7],'s-')
    plot([13,12,11,10,8,7,5,4,3],absxpeaks,'s-')
    xlabel('pH')
    ylabel('peak position (nm)')
    legend(['fluorescence', 'absorption'])
        

    return (xpeaks,absxpeaks)