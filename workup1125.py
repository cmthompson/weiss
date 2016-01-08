# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:13:48 2014

@author: chris
"""

import os
import RamanTools
from scipy import optimize
import pdb
from numpy import fft
import pandas


def takeout(a,centers = (452,479),demo = False):
    def function(x,A1,w1,G1,b): return b - A1*exp(-(x-w1)**2/G1)
    for center in centers:
        x = array(a.index[center-7:center+7])
        y = a.values[center-7:center+7]
        
        guess= [a.iloc[center]-a.iloc[center+7],float(a.index[center]),20,float(a.iloc[center+7])]
      
        try:
            result = optimize.curve_fit(function,x,y,guess)
        except RuntimeError:
            tkMessageBox.showerror('Fit Failed')
            return 0
        z = list(result[0])
        if demo:
       
            print z
            plot(x,function(x,*z))
        
        if abs(z[2]<100):
            a.iloc[center-7:center+7]-=function(x,*z)-z[-1]

    return 0



def Fig1():   ##### View,filter, and average spectra of PbS dots with Methoxythiophenol in the 800-1600 cm-1 range
    a = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/5_.txt')
    takeout(a)
    
    b = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/6_.txt')
    takeout(b)
    
    c = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/8_.txt')
    takeout(c)
    
    d = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/6_.txt')
    takeout(d)
    
    e = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/3_.txt')
    
    
    for l in [a,b,c,d,e]:
        noise = l.calc_noise((1100,1200))
        signal = l.values[argmin(abs(array(l.index)-1596))] - l.values[argmin(abs(array(l.index)-1650))]
        print 'S/N:', signal/noise
    
    l = RamanTools.add_RamanSpectra(a,b)
    
    m = RamanTools.add_RamanSpectra(l,c)
    
    
    o = RamanTools.add_RamanSpectra(m,d)
    #o = RamanTools.add_RamanSpectra(o,e)
    
    
    noise = l.calc_noise((1100,1200))
    signal = l.iloc[argmin(abs(array(l.index)-1596))] - l.iloc[argmin(abs(array(l.index)-1650))]
    print 'S/N:', signal/noise
    
    noise = m.calc_noise((1100,1200))
    signal = m.iloc[argmin(abs(array(m.index)-1596))] - m.iloc[argmin(abs(array(m.index)-1650))]
    print 'S/N:', signal/noise
    
    noise = o.calc_noise((1100,1200))
    signal = o.iloc[argmin(abs(array(m.index)-1596))] - o.iloc[argmin(abs(array(o.index)-1650))]
    print 'S/N:', signal/noise
    
    
    
    
    figure()
    subplot(311)
    a.plot(color='r')
    b.plot(color='k')
    c.plot(color='b')
    d.plot(color='g')
    legend(['a','b','c','d'])
    
    
    #n = FourierFilter(n, width = 400)
    subplot(312)
    o.plot()
    
    
    
    subplot(313)
    
    n=RamanTools.FourierFilter(o,width = 170)
    
    n.autobaseline((700,1700))
    
    n.plot(color = 'k')
    
    
    ####  Reference Spectrum of MTP on Cd
    
    MTP = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141014/4_methoxythiophenol_1.csv')
    MTP-=min(MTP[0:1000])
    MTP/=(max(MTP[0:1000]))
    MTP*=1000
    MTP.plot(color = 'b',linewidth = 3)
    
    
    a = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/10_control pbs.txt')
    b = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/11_control.txt')
    c = RamanTools.add_RamanSpectra(a,b)
    control = RamanTools.FourierFilter(c,width = 170)
    control.autobaseline((700,1700))
    
    control.plot(color = 'r')
    
    
    xlim(700,1700)
    ylim(-500,1500)
    return 0
    
def Fig2(): ##### View,filter, and average spectra of PbS dots with Methoxythiophenol in the 2300-3400 cm-1 range
    subplot(121)
    a = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/7_.txt')
    
    takeout(a)
    a.plot()
    b = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/7_.txt')
    b = RamanTools.FourierFilter(b,width = 380)

    takeout(b,centers = (456,483),demo = True)
    b.plot()
    c = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/8_.txt')
    takeout(c)
    c.plot()
    m = RamanTools.add_RamanSpectra(a,b)
    n = RamanTools.add_RamanSpectra(m,c)
    
    
    legend(['1','2','3'])
    subplot(122)
    
    MTP = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141014/4_methoxythiophenol_1.csv')
    MTP-=min(MTP[0:1000])
    MTP/=(max(MTP[0:1000]))
    MTP*=1000
    MTP.plot(color = 'b',linewidth = 3)
    n.autobaseline((2300,3400))
    n/=10
    n.plot()
    xlim(2300,3400)
    ylim(-500,1500)
    
    
    
    return 0
    
def Fig3():  ### Combine final spectra from fig1 and fig2.  Display side by side.  Showing no SH stretch but some modes for phenyl ring in MTP.  
    subplot(121)
    a = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/5_.txt')
    takeout(a)
    
    b = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/6_.txt')
    takeout(b)
    
    c = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/8_.txt')
    takeout(c)
    
    d = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/6_.txt')
    takeout(d)
    
    e = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/3_.txt')

    ##### total of 4500 s measurement for a-e, for a-d total is 2500 s
    l = RamanTools.add_RamanSpectra(a,b)
    
    m = RamanTools.add_RamanSpectra(l,c)
    
    
    o = RamanTools.add_RamanSpectra(m,d)
    n=RamanTools.FourierFilter(o,width = 170)
    
    n.autobaseline((700,1700))
    n/=2500
    
    
    
    MTP = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141014/4_methoxythiophenol_1.csv')
    MTP-=min(MTP[0:1000])
    MTP/=(max(MTP[0:1000]))
    MTP+=1
    
    
    
    a = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/10_control pbs.txt')
    b = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/11_control.txt')
    c = RamanTools.add_RamanSpectra(a,b)
    ####total colection time for a and b is 1700
    control = RamanTools.FourierFilter(c,width = 170)
    control.autobaseline((700,1700))
    control[:]/=1700
    control +=0.5
    
    
    MTP.plot(color = 'b',linewidth = 3,label  ='MTP reference')
    control.plot(color = 'r',label = 'PbS-oleate only')
    n.plot(color = 'k',label = 'PbS-oleate + MTP')
    annotate('C-S-H bend',(910,1.25),xytext = (910,2.0),arrowprops = {'width':1,'headwidth':3,'frac':0.05,'color':'k'} )
    annotate('Ring expansion',(804,2.1),xytext = (804,2.6),arrowprops = {'width':1,'headwidth':3,'frac':0.05,'color':'k'} )
    annotate('Ring expansion',(1095,1.85),xytext = (1140,1.9),arrowprops = {'width':1,'headwidth':3,'frac':0.05,'color':'k'} )
    annotate('Ring asymmetric rocking',(1600,1.7),xytext = (1300,1.8),arrowprops = {'width':1,'headwidth':3,'frac':0.05,'color':'k'} )
   
   
   
    legend()
    xlim(700,1700)
    ylim(-0.5,3)
    ylabel('Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')
    
    
    
    subplot(122)
        
    a = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141125/7_.txt')
    
    takeout(a)
  
    b = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/7_.txt')
    b = RamanTools.FourierFilter(b,width = 380)

    takeout(b,centers = (456,483))
 
    c = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141126/8_.txt')
    takeout(c)
    #### Total collection time is 2500 s
    
    m = RamanTools.add_RamanSpectra(a,b)
    g = RamanTools.add_RamanSpectra(m,c)
    g.autobaseline((2300,3400))

    g[:]/=2500
    
    
    
    MTP.plot(color = 'b', label = 'MTP reference',linewidth = 3)
    g.plot(color = 'k', label='PbS-oleate + MTP')
    annotate('S-H stretch',(2556,1.4),xytext = (2556,1.6),arrowprops = {'width':1,'headwidth':3,'frac':0.05,'color':'k'} )
    
    
    

    legend()
    xlim(2300,3400)
    ylim(-0.5,3.0)
    xlabel('Raman Shift (cm$^{-1}$)')
    return 0
    
def Fig4():  ### Combine final spectra from fig1 and fig2.  Display side by side.  Showing no SH stretch but some modes for phenyl ring in MTP.  
    import os
    os.chdir('/home/chris/Documents/DataWeiss/141113')
    
    for i in os.listdir('.'):
        if '.txt' in i:
            print i
  
            try:
                a = RamanTools.RamanSpectrum(i)
                a.autobaseline((800,1680),order = 4)
                
                
            except:
               
                continue
            figure()
            title(i[-8:])
            a.plot()
            xlim(800,1700)
            gca().autoscale(axis = 'y')
            

    return 0    

def Fig5():  ### showing SERS on gold.

    green = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141202/15_.txt')
    red = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141202/14.txt')
    green*=100
    green[:]-=167000
    red[:]-=red.iloc[0]
    green.plot(color = 'g',label = '514.5 nm x 100')
    red.plot(color = 'r',label = '647.1 nm (SERS enhanced)')
    legend()
    title('Raman of gold nanoparticles ($\lambda_{max}$ = 535 nm)')
    ylabel('Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')
    return 0
    
def Fig6():
    from RamanTools2 import autobaseline
    r = loadtxt('/home/chris/Documents/DataWeiss/141203/Nanoparticles after dispersion in methanol Dec3.csv',
            unpack = True,
            delimiter = ',',
            usecols= (2,3,4,5),
            skiprows = 2)
    largeAu = pandas.Series(r[1],r[0])
    largeAu[:]*=2

    smallAu = pandas.Series(r[3],r[2])
            
    subplot(121)
    
    smallAu.plot(color = 'green',label = '525 nm sample')
    largeAu.plot(color= 'r',label = '535 nm sample')
    legend()
    
    r = loadtxt('/home/chris/Documents/DataWeiss/141203/Nanoparticles after deposition onto glass Dec3.csv',
            unpack = True,
            delimiter = ',',
            usecols= (2,3,4,5,6,7,8,9,10,11),
            skiprows = 2)
    smallAu1 = pandas.Series(r[1],r[0])

    smallAu2 = pandas.Series(r[3],r[2])
    
    glass = pandas.Series(r[5],r[4])
    largeAu1 = pandas.Series(r[7],r[6])
    largeAu2 = pandas.Series(r[9],r[8])
    
    
    subplot(122)
    rnge = (600,492)
    autobaseline(smallAu1,rnge,order = 0)
    smallAu1.plot(color = 'k',label = '525 sample1')
    autobaseline(smallAu2,rnge,order = 0)
    smallAu2.plot(color = 'k',label = '525 sample2')
    
    autobaseline(glass,rnge,order = 2)
    glass.plot(label = 'glass')
    autobaseline(largeAu1,rnge,order = 0)
    largeAu1.plot(color = 'r',label = '535 sample1')
    autobaseline(largeAu2,rnge,order = 0)
    largeAu2.plot(color = 'r',label = '535 sample2')
    
    xlim(rnge[1],rnge[0])
    ylim(-0.001,0.005)
    
    legend()
    
    
    #### took a wider view of exactly those particles used for SERS experiment.\ in Fig7
    figure()
    r = loadtxt('/home/chris/Documents/DataWeiss/141203/Gold nanoparticles wider view.csv',
            unpack = True,
            delimiter = ',',
            skiprows = 2)
    largeAu = pandas.Series(r[5],r[4])
    largeAu[:]*=2

    smallAu = pandas.Series(r[7],r[6])
    
    
    
    
    correctionpoint1 = argmin(abs(array(smallAu.index)-800))
    correctionpoint2 = argmin(abs(array(smallAu.index)-350))
    
    
    smallAu.iloc[correctionpoint2:]-= diff(smallAu)[correctionpoint2]
    smallAu.iloc[:correctionpoint1]+= diff(smallAu)[correctionpoint1]
    largeAu.iloc[:correctionpoint1]+= diff(largeAu)[correctionpoint1]
    largeAu.iloc[correctionpoint2:]-= diff(largeAu)[correctionpoint2]
    
    smallAu[:]-=smallAu.iloc[0]
    largeAu[:]-=largeAu.iloc[0]
    
    peaklarge = argmin(abs(array(largeAu.index)-535))
    peaksmall = argmin(abs(array(smallAu.index)-525))
    
    smallAu[:]/=smallAu.iloc[peaksmall]
    largeAu[:]/=largeAu.iloc[peaklarge]
    #smallAu.plot(color = 'green',label = '525 nm sample')
    largeAu.plot(color= 'r',label = '535 nm sample')
    legend()
    ylabel('Absorbance (a.u.)')
    xlabel('Frequency (nm)')
    
    return 0
    
def Fig7():  ### show raman enhancmenet of MTP coated gold NPs
    green = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141203/4_.txt')
    red = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141203/7_.txt')
    MTP = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141014/4_methoxythiophenol_1.csv')
    MTP-=min(MTP[0:1000])
    MTP/=(max(MTP[0:1000]))/10000
    MTP+=3000
    
    green[:]*=10
    green._smooth()
    green[:]-=14100
    
    red[:]-=red.iloc[0]-1000
    
    MTP.plot(color = 'b',label = 'MTP reference')
    green.plot(color = 'g',label = '514.5 nm x 10')
    red.plot(color = 'r',label = '647.1 nm (SERS enhanced)')
    legend()
   
    annotate('C-S-H bend',(910,5000),xytext = (950,12000),arrowprops = {'width':1,'headwidth':10,'frac':0.05,'color':'k'} )
    title('Raman of MTP-functionalized gold nanoparticles ($\lambda_{max}$ = 535 nm)')
    ylabel('Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')
    return 0
    
def Fig8():  ### show raman enhancmenet of CdSe phonon mode
    ongold = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141203/15_.txt')
    offgold = RamanTools.RamanSpectrum('/home/chris/Documents/DataWeiss/141203/16.txt')

    
    #title('SERS of CdSe (ODPA-capped) on Gold NPs ($\lambda_{max}$ = 576 nm)')
    
    
    
    ongold.plot(color = 'r',label = 'CdSe QDs on gold NPs (SERS enhanced)')
    offgold.plot(color = 'k',label = 'CdSe QDs')
    legend()
    annotate('2nd-LO CdSe', (393,5340))
    annotate('3rd-LO CdSe', (610,5500))
    
    ylabel('Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')
    xlim(300,700)
    ylim(3200,6500)
    
   
    #annotate('C-S-H bend',(910,5000),xytext = (950,12000),arrowprops = {'width':1,'headwidth':10,'frac':0.05,'color':'k'} )
    
    return 0

    
    
    
    