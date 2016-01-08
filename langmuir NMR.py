# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:54:57 2015

@author: chris
"""
from ramanTools.RamanSpectrum import *
from numpy import *
from matplotlib.pyplot import *
from Nov6 import *
from numpy.polynomial.polynomial import polyder
from numpy.polynomial.polynomial import polyfit as pf

import ramanTools.RamanSpectrum as rs
import UVVistools as uv

def Oct13():
    a= loadtxt('/home/chris/Dropbox/DataWeiss/151013/NMR samples.csv', delimiter = ',', unpack = True, skiprows=1)
    
    for i in range(1,6):
        r = polyfit(a[0,0:100],a[i,0:100],1)
        a[i]-=rs.polyeval(r,a[0])
        peak = uv.findpeak(a[0],a[i],(410,420))
        print peak 
        diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
        print 'diam', diameter
        epsilon = 21536*diameter**2.3
        print 'eps', epsilon    
        print 'conc', 5*peak[1]/epsilon 
        plot(a[0],a[i])
    legend(['10.5','9.5','9.3','8.6','6.8'])
        
    return 0
    
def Oct17():
    a= loadtxt('/home/chris/Dropbox/DataWeiss/151017/thioldots.csv', delimiter = ',', unpack = True, skiprows=1, usecols = (0,6,3,1,2,4,5))
        
    for i in range(1,7):
        r = polyfit(a[0,0:100],a[i,0:100],1)
        a[i]-=rs.polyeval(r,a[0])
        peak = uv.findpeak(a[0],a[i],(410,420))
       #print peak 
        diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
        #print 'diam', diameter
        epsilon = 21536*diameter**2.3
       # print 'eps', epsilon
        print 'CONC', 5*peak[1]/epsilon 
        plot(a[0],a[i])
    legend(['4.2','6.0',',6.4','7.7','9.7','11.5'])
    
    print 'THIOL EXCHANGE'  
    a= loadtxt('/home/chris/Dropbox/DataWeiss/151017/thiolcapped doits.csv', delimiter = ',', unpack = True, skiprows=1, usecols = (0,1))
    r = polyfit(a[0,0:100],a[1,0:100],1)
    a[1]-=rs.polyeval(r,a[0])
    peak = uv.findpeak(a[0],a[1],(410,420))
   #print peak 
    diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
    #print 'diam', diameter
    epsilon = 21536*diameter**2.3
   # print 'eps', epsilon
    print 'CONC', 5*peak[1]/epsilon
    
    a= loadtxt('/home/chris/Dropbox/DataWeiss/151017/thioldots.csv', delimiter = ',', unpack = True, skiprows=1, usecols = (0,3,1,2,4,5,6))
        
    for i in range(1,7):
        r = polyfit(a[0,0:100],a[i,0:100],1)
        a[i]-=rs.polyeval(r,a[0])
        peak = uv.findpeak(a[0],a[i],(410,420))
       #print peak 
        diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
        #print 'diam', diameter
        epsilon = 21536*diameter**2.3
       # print 'eps', epsilon
        print 'CONC', 5*peak[1]/epsilon 
        plot(a[0],a[i])
    legend(['200','400',',800','2000','3200','4000'])
        
    return 0
    
def Oct17NMRfitting():
#    a = loadtxt('/home/chris/Dropbox/DataWeiss/151020/MPAexchange on HCN_1000eq.csv',skiprows = 1, usecols = (0,1), delimiter = ',', unpack = True)
#   `r = RamanSpectrum(pandas.Series(a[1],a[0]))
#    w=1E-5
#    g = [0.05,0.03,0.05,.03,.1,.03,.05,.03,.05,1.38,1.39,1.395,1.405,1.41,1.42,1.425,1.43,1.44,w,w,w,w,w,w,w,w,w,0,0]
#    s = fitspectrum(r,(1.34,1.46), 'xGaussian', g)
#    clf()
#    r.plot()
#    for i in s.peaks: plot(s.x,i)
#    plot(s.x,s.y)
#    print s.areas
#    xlim(1.34,1.49)
#    ylim(-0.01,0.1)
    
 
#    a = loadtxt('/home/chris/Dropbox/DataWeiss/151020/MPAexchange on HCN_100eq.csv',skiprows = 1, usecols = (0,1), delimiter = ',', unpack = True)
#    r = RamanSpectrum(pandas.Series(a[1],a[0]))
#    r.name = ''
#    w=1E-5
#    a = 0.04
#    g = [a,a,a,a,a,a,a,a,a,a,a,1.38,1.385,1.392,1.398,1.405,1.41,1.412,1.42,1.43,1.435,1.44,w,w,w,w,w,w,w,w,w,w,w,0,0]
#   # s =  fitspectrum(r,(1.34,1.46), 'xGaussian', g)
#    
#    r.plot()
#    for i in s.peaks: plot(s.x,i)
#    plot(s.x,s.y)
#    print s.areas
#    xlim(1.34,1.49)
#    ylim(-0.01,0.1)
    
    a = loadtxt('/home/chris/Dropbox/DataWeiss/151020/MPAexchange on HCN_100eq.csv',skiprows = 1, usecols = (0,1), delimiter = ',', unpack = True)
    r = RamanSpectrum(pandas.Series(a[1],a[0]))
    r.name = ''
    w=1E-5
    a = 0.04
    g = [a,0.05,a,a,a,a,a,a,a,a,a,1.725,1.73,1.738,1.743,1.745,1.75,1.755,1.765,1.77,1.78,1.785,w,w,w,w,w,w,w,w,w,w,w,0,0]
    s =  fitspectrum(r,(1.70,1.80), 'xGaussian', g)
    clf()
    r.plot()
    for i in s.peaks: plot(s.x,i)
    plot(s.x,s.y)
    print s.params[0]
    xlim(1.70,1.80)
    ylim(-0.01,0.1)
    return s.areas

def Oct29PPATitrationUVVis():
    a = loadtxt('/home/chris/Dropbox/DataWeiss/151029/151029UVVis.csv', delimiter = ',', unpack=True, skiprows=1)
    for i in range(1,8):
        a[i]-=a[i,0]
        peak = uv.findpeak(a[0],a[i],(410,420))
        print peak
        plot(a[0],a[i])
        diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
        print 'diam', diameter
        epsilon = 21536*diameter**2.3
       # print 'eps', epsilon
        print 'CONC', 5*peak[1]/epsilon 
    legend(['vial0','vial1','vial2','vial3','vial4','vial5','vial6',])
    ylabel('Absorbance')
    xlabel('wavelength (nm)')
    return 0
    
def Oct30PPATitrationUVVis():
    a = loadtxt('/home/chris/Dropbox/DataWeiss/151030/151030PPAtitration.csv', delimiter = ',', unpack=True, skiprows=1)
    for i in range(1,11):
        a[i]-=a[i,0]
        peak = uv.findpeak(a[0],a[i],(410,420))
        print peak
        plot(a[0],a[i])
        diameter = -0.000000066521*peak[0]**3+0.00019557*peak[0]**2-0.092352*peak[0]+13.29
        #print 'diam', diameter
        epsilon = 21536*diameter**2.3
       # print 'eps', epsilon
        print 'CONC', 5*peak[1]/epsilon 
    legend(['vial0','vial1','vial2','vial3','vial4','vial5','vial6','vial7','vial8','vial9', 'vial10',])
    ylabel('Absorbance')
    xlabel('wavelength (nm)')
    return 0

def peaksshift():
    x = linspace(-1,2,1000)
    noexchange = 1/((x-0)**2+.0004)+1/((x-1)**2+.0004)
    subplot(411)
    yticks()
    plot(x,noexchange)
    subplot(412)
    plot(x,1/((x-0.25)**2+.0004))
    subplot(413)
    yticks()
    plot(x,1/((x-0.5)**2+.0004))
    subplot(414)
    yticks()
    plot(x,1/((x-0.75)**2+.0004))
    for ax in gcf().axes:
        ax.set_yticks([])
        ax.set_xticks([0,0.25,0.5,0.75,1])
        ax.set_xlim(-0.3,1.3)
    return 0

def exampleplot():
    figure()
    ax1=subplot(121)
    ax2=subplot(122)
    c = linspace(0,10,1000)
    
    cmaxdot = 0.2
  #  subplot(121)
    for K in [100,1000,10000]:
        K=float(K)
        a = K
        #def b():return -ctot0*K - K*c +K*cmaxdot+1
        #def d():return ctot0+c
        #    
        #def cfree():return (-b()+sqrt(b()**2-4*a*d()))/(2*a)
        a=K
        b=1+K*cmaxdot-K*c
        d=-c
            
        cfree = (-b+sqrt(b**2-4*a*d))/(2*a)
        cfree2= (-b-sqrt(b**2-4*a*d))/(2*a)
        r = pf(c[10:15],cfree[10:15],1)
        
        
        #print r[0], (K+0.5*((1+K*cmaxdot-K*xlarge)**2+4*K*xlarge)**-0.5*(-2*K*(1+K*cmaxdot-K*xlarge)+4*K))/(2*K)
        
        M = (r[0]-0.5)**2
        A = (M-0.5)#*xlarge**2
        B = (2*M-1)#*xlarge
        
        C = M-0.5
        print M,A,B,C,B**2
        
        #print K,'estimated K=',(-B+sqrt(B**2-4*A*C))/(2*A)
        print 'early slope=', cfree[0]/c[1],cfree[0]/c[1]-c[1]*r[1]
       # plot(c[:10],(c[:10]-0.1)*r[1]+cfree[10]/c[10])
        ax1.plot(c,cfree/c)
        ax2.plot(c,cfree/c)
    
       # plot(c,findderivative(c,cfree/c,derivorder=1)/200,'--')
        #plot(c,fd(c,cfree/c),'-.')
        
        #plot(c,K*cfree/(1+K*cfree))
       # plot(c,cfree2)
    legend([1,10,100,1000])
    
    ax1.set_ylabel('$\delta_{observed}$',fontsize=24)
    #ax2.set_ylabel('$\delta$',fontsize=24)
    ax1.set_xlabel('c$_{total}$ (mM)', fontsize=24)
    ax2.set_xlabel('c$_{total}$ (mM)', fontsize=24)
    ax2.set_xlim((0,0.4))
    ax2.set_xticks([0,0.1,0.2,0.3,0.4,0.5])
    ax1.set_yticks([0,1])
    ax2.set_yticks([])
    ax1.set_yticklabels(['$\delta_{bound}$','$\delta_{free}$'],fontsize=24)
    
    figure()
    ax1=subplot(211)
    ax2=subplot(212)
   
    for K in [50]:
        K=float(K)
        a = K
        #def b():return -ctot0*K - K*c +K*cmaxdot+1
        #def d():return ctot0+c
        #    
        #def cfree():return (-b()+sqrt(b()**2-4*a*d()))/(2*a)
        a=K
        b=1+K*cmaxdot-K*c
        d=-c
            
        cfree = (-b+sqrt(b**2-4*a*d))/(2*a)
       
        ax1.plot(c,cfree/c)
        ax2.plot(c,c-cfree)#K*cfree*cmaxdot/(1+K*cfree))
        ax2.plot(c,cfree,'--')
        ax2.plot(c,c)
       
    
    legend(['bound', 'free', 'total'],loc=2)
    
    ax1.set_ylabel('$\delta_{observed}$',fontsize=24)
 
    ax2.set_xlabel('c$_{total}$ (mM)', fontsize=24)
    ax2.set_ylabel('c (mM)',fontsize=24)
    #ax2.set_xticks([0,0.1,0.2,0.3,0.4,0.5])
    ax1.set_yticks([0,1])
    ax1.set_xlim(0,1)
    ax2.set_xlim(0,1)
    
    #ax1.set_ylim(-0.1,1.1)
    ax2.set_ylim(0,1)
    
   
    ax1.set_yticklabels(['$\delta_{bound}$','$\delta_{free}$'],fontsize=24)
    
#    subplot(122)   
#    for cinit in [0,0.1,0.2,0.5,1]:
#        a = K
#        #def b():return -ctot0*K - K*c +K*cmaxdot+1
#        #def d():return ctot0+c
#        #    
#        #def cfree():return (-b()+sqrt(b()**2-4*a*d()))/(2*a)
#        ctot = cinit+c
#        a=K
#        b=1+K*cmaxdot-K*ctot
#        d=-ctot
#            
#        cfree = (-b+sqrt(b**2-4*a*d))/(2*a)
#        
#        plot(c,cfree/ctot)
#       # plot(c,cfree2)
#    legend([0,0.1,0.2,0.5,1])
    
    return 0

def datafit():
    def peakwalk(cadded,K,c_init,cmaxdot,deltadots,deltafree):
        
        c = cadded+c_init
        a=K
        b=1+K*cmaxdot-K*c
        d=-c
            
        return (deltafree-deltadots)*(-b+sqrt(b**2-4*a*d))/(2*a*c)+ deltadots +sin(200*int(c_init<0))
        
    def peakwalkfixinit(cadded,K,cmaxdot,deltadots,deltafree):
        c_init=200
        
        c = cadded+c_init
        a=K
        b=1+K*cmaxdot-K*c
        d=-c
            
        return (deltafree-deltadots)*(-b+sqrt(b**2-4*a*d))/(2*a*c)+ deltadots +sin(200*int(c_init<0))
        
    def peakwalkfixdeltas(cadded,K,c_init,cmaxdot):
        c_init=200
        
        c = cadded+c_init
        a=K
        b=1+K*cmaxdot-K*c
        d=-c
            
        return (20.95-19.53)*(-b+sqrt(b**2-4*a*d))/(2*a*c)+ 19.53 +sin(200*int(c_init<0))
    
    def peakwalksimple(cadded,c_init,cmaxdot,deltadots,deltafree):    
        
        return (deltafree-deltadots)*(cadded+c_init-cmaxdot)/(cadded+c_init)+ deltadots 
    
    def peakwalksimplefixinit(cadded,cmaxdot,deltadots):    
        c_init = 600
        return (20.96-deltadots)*(cadded+c_init-cmaxdot)/(cadded+c_init)+ deltadots 
    
    figure()
    usefunction =peakwalk#(cadded,K,c_init,cmaxdot) peakwalksimplefixinit
    guess =[1,1100,200,21,18]  

    
    
    
    xs = array([0,86,128,171,214,428,891,1644,1645,2041,2381,3833,7079]) ### added amount of PPA in mM
    ys = array([19.61,  19.67,  19.71,    19.74,  19.73,    19.82,  20.02,20.43, 20.44,  20.52,  20.55,  20.75,20.96])
    fit = scipy.optimize.curve_fit(usefunction,xs,ys,guess)
    print fit[0]#,fit[1]#np.sqrt(np.diag(fit[1]))
    
    xsOct30=array([0,40,79,197,408,812,1574,2372,3899,7992])
    
    ysOct30 = array([19.67,19.55,19.63,19.76,19.9,20.03,20.36,20.48,20.64,20.85])
    
    fitOct30 = scipy.optimize.curve_fit(usefunction,xsOct30,ysOct30,guess)
    print fitOct30[0]#,fitOct30[1]#np.sqrt(np.diag(fitOct30[1]))
    
    
    
    #print 'cmax as determined from slope=', cmax,'.  equivalents per dot =', cmax/0.0024
    #print 'K=',fit[0][0]
    #print 'Initial conc PPA total (mM)=',fit[0][1]
    #print 'maximum concentration on dots=', fit[0][2],'.  equivalents per dot =', fit[0][2]/0.0024
    #print  'chemical shift of PPA on dots=', fit[0][3]
    f = fit[0][1]
    fit[0][1]=0
    fOct30 = fitOct30[0][1]
    fitOct30[0][1]=0
    
    fitxs = arange(0,10000,1)
    plot(fitxs,usefunction(fitxs,*fit[0]))
    plot(xs+f,ys,'s')
    plot(fitxs,usefunction(fitxs,*fitOct30[0]))
    #f_free = (usefunction(fitxs,*fitOct30[0])-fitOct30[0][3])/(fitOct30[0][2]-fitOct30[0][3])
    #f_bound = 1-f_free
    
    plot(xsOct30+fOct30,ysOct30,'s')
    xlabel('Total PPA ($\mu$M)')
    ylabel('chemical shift (ppm)')
    return 0