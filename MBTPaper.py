# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:59:20 2015

@author: chris
"""

from ramanTools.RamanTools import *



def VictorRaman():
    figure(figsize=(9,12))
    ax1 = subplot(211)
    ax2 = subplot(212)
    
    
    
    
    a= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150612/150612_01_CdSe.txt') ###### Native ligand only
    a[:]/=2
    a=removespikes(a)
    a.autobaseline((600,690,861,900,1196,1385,1515,1657),specialoption='points',order=6)
    a.smooth()
    
    

    
    b= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150617/150617_01.txt')  ###### 1000 eq MBT
    b=removespikes(b)
    b.autobaseline((803,861),order=1, join='start')
    b.autobaseline((861,1254),order = 2, join='start')
    b.autobaseline((1254,1515),order = 4, join = 'start')
    b.autobaseline((1515,2000),order = 3, join = 'start')
    b.autobaseline((555,613,764,1052,1141,1321,1565,1652),specialoption='points',order=8)
    b.smooth()
    
    
    c= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150617/150617_04.txt')  ###### solid MBT
    c=removespikes(c)
    c.smooth()
    
    lw = 2
    b[:]+=500
    c[:]+=1250
    
    
    c.plot(ax=ax1,linewidth = lw)
    b.plot(ax=ax1,linewidth = lw)
    a.plot(ax=ax1,linewidth = lw)
    ax1.set_ylabel('Intensity (a.u.)')
    ax1.set_xlabel('Raman shift (cm$^{-1}$')
    
   
    
    
    
    a= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150616/150616_04.txt')  ### native ligand only
    a[:]/=2
    a.autobaseline((2400,2773),order = 1)
    a.autobaseline((2773,2777),order = 1,join='start')
    a.autobaseline((2777,3164),order = 0,join='start')
    a.autobaseline((2400,2500,2700,2800,3160),specialoption='points', order = 5)
    
    a=removespikes(a,thresholds = [1,1,1])
    

    b = RamanSpectrum('/home/chris/Dropbox/DataWeiss/150617/150617_02.txt')  ### 1000 eq MBT
    b=removespikes(b)
    
    b.autobaseline((2400,2775),order = 1)
    b.autobaseline((2775,2779),order = 1,join='start')
    b.autobaseline((2779,3164),order = 0,join='start')
    b.autobaseline((2400,2500,2700,2800,3160),specialoption='points', order = 5)
    b.smooth()
    
    
    c= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150617/150617_03.txt')  ###### solid MBT
    c=removespikes(c)
    c.smooth()
    
    b[:]+=50
    c[:]+=200
    
    
    c.plot(ax=ax2,linewidth = lw)
    b.plot(ax=ax2,linewidth = lw)
    a.plot(ax=ax2,linewidth = lw)
    
    ax1.set_xlim((600,1650))
    ax1.set_ylim((0,2750))
    
    ax2.set_xlim((2400,3155))
    ax2.set_ylim((0,460))
    
    ax2.set_ylabel('Intensity (a.u.)')
    ax2.set_xlabel('Raman shift (cm$^{-1}$')
    
    ax1.legend([ 'solid CH$_3$-TP','QDs + 640 eq CH$_3$-TP','QDs with native ligands'],fontsize = 10)
    ax2.legend(['solid CH$_3$-TP','QDs + 640 eq CH$_3$-TP','QDs with native ligands'],fontsize = 10)
   
    adict = {'width':0.5,'color':'k','headwidth':3}
    assignmentfontsize = 10
    ax1.annotate('Ring bending',(805,2115),xytext=(875,2330), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax1.annotate('',(805,943),xytext=(890,2330), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
       
    ax1.annotate('Ring breathing',(1105,2133), xytext = (1130,2556),xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops = adict)
    ax1.annotate('',(1105,1154),xytext = (1140,2556), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops = adict)
    ax1.annotate('CSH bending',(903,1400),xytext = (915,1630), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    
    ax1.annotate('Ring bending',(1599,1404),xytext=(1500,1800), xycoords = 'data',horizontalalignment = 'right',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax1.annotate('',(1584,905),xytext=(1480,1800), xycoords = 'data',horizontalalignment = 'right',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
           
    ax1.annotate('PO$_3$ stretching\n +CC stretching',(903,310), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal')
    ax1.annotate('alkyl CH$_x$ deformation',(1430,750),xytext=(1513,1106), xycoords = 'data',horizontalalignment = 'right',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax1.annotate('',(1430,315),xytext=(1380,1106), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    
    ax1.annotate('alkyl CH$_x$ twisting',(1300,328),xytext=(1275,444), xycoords = 'data',horizontalalignment = 'right',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax1.annotate('PC stretching',(760,350),xytext=(605,425), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    
    ax2.annotate('SH stretching',(2570,350),xytext = (2600,410), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax2.annotate('alkyl CH stretching',(2870,196),xytext = (2750,230), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax2.annotate('',(2870,52),xytext = (2770,230), xycoords = 'data',horizontalalignment = 'left',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    ax2.annotate('aromatic CH$_x$ stretching',(3046,284),xytext = (2920,300), xycoords = 'data',horizontalalignment = 'right',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops =adict)
    savefig('/home/chris/Desktop/Raman.png',dpi=512)
    return 0
    
def VictorFluorescenceFWHM():
    a = loadtxt('/home/chris/Dropbox/DataWeiss/150617/CdSeFluorescenceVictor.csv',skiprows=1, delimiter = ',', unpack= True)
    plot(a[0],a[3])
    a = RamanSpectrum(pandas.Series(a[3],a[0]))
    r = fitspectrum(a,(500,700),'OneGaussian',[300000,590,50,0,0])
    plot(r.x, r.y)
    print r.params
    return r.params
    
def VictorUVVis():
    from ramanTools.RamanSpectrum import SGsmooth
    ax1=gca()
    a = loadtxt('/home/chris/Dropbox/DataWeiss/150617/150616UVVisCdSeVictor.csv',skiprows=2, delimiter = ',', unpack= True)
    s= argmin(abs(a[0]-567))
    lmax_list = []
    for i in [1,5,4,3,2]:
        a[i,:]=SGsmooth(a[0],a[i])
        a[i]-=min(a[i])
        lambdamax = argmax(a[i][s-10:s+10])+s-10
        lmax_list.append(a[0,lambdamax])
        a[i]/=a[i,lambdamax]
        plot(a[0],a[i])
    legend(['0 eq','32 eq','84 eq','179 eq','682 eq'])
    ax1.set_xlabel('wavelength (nm)')
    ax1.set_ylabel('absorbance (a.u.)')
    ax2 = axes([0.25, 0.2, .3, .3])
    ax2.plot([0,32,84,179,682],lmax_list)
    ax2.set_ylabel('$\lambda max$ (nm)')
    ax2.set_xlabel('equivalents MBT')
    
    return a