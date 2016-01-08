# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 11:04:47 2014

@author: chris
"""
import pandas
from ramanTools.RamanSpectrum import *
from copy import deepcopy,copy


def Fig1(show_vib_numbers = True): ### reference spectra of methylbenzenethiol
    figure(figsize = (6,6))
    
    MBT = copy(MeOTPRef)
    MBT-=min(MBT[0:2000])
    MBT/=max(MBT[0:2000])
    

    CdMBT = copy(CdMeOTPRef)
    CdMBT.index = array(CdMBT.index)-3
    CdMBT-=min(CdMBT[0:2000])
    CdMBT/=max(CdMBT[0:2000])
    
    a = RamanSpectrum('/home/chris/Documents/DataWeiss/150408/150408_15.txt')
    
    a.autobaseline((268,440,723,915,1200,1391,1505,1680),specialoption='points', order = 4)
    a.smooth(window_len=11,window = 'SG')
    a[:]/=3000
                  
    
    MBT.plot(color = 'b',linewidth = 2)
    CdMBT.plot(color = 'k',linewidth = 2)
    a.plot(color = 'r',linewidth = 2) 
    xlim(500,1675)
    ylim(0,1.5)
    
    ylabel('Intensity (a.u.)')
    xlabel('Raman shift (cm$^{-1}$)')
         
                    
    ####Assignments
    assignmentfontsize = 10
   # annotate('Ring bending',(635,0.2), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('Ring bending',(647,0.38), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('Ring stretching',(1105,1.05), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal')
    annotate('Ring stretching',(806,1.1), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal')
    annotate('CSH bending ',(914,0.25), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
 #   annotate('CH bending ',(1190,0.33), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    #annotate('Ring stretching',(1300,0.5), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
   # annotate('CH bending',(1382,0.1), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('CC ring stretching',(1607,0.5), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')

    legend(['MTP', 'CdMTP$_2$', 'QDs-MTP'])

    matplotlib.pyplot.tight_layout()
    return 0
    
    
#def Fig1(show_vib_numbers = True): ### reference spectra of methylbenzenethiol
#    figure(figsize = (6,6))
#    
#    MBT = RamanSpectrum('/home/chris/Documents/DataWeiss/141007/1_methylbenzenethiol_1.txt')
#    MBT-=min(MBT[0:2000])
#    MBT/=max(MBT[0:2000])
#    
#
#    CdMBT = RamanSpectrum('/home/chris/Documents/DataWeiss/141007/3_CdMethylthiophenol647_1.txt')
#    CdMBT-=min(CdMBT[0:2000])
#    CdMBT/=max(CdMBT[0:2000])
#                  
#    
#    subplot(211)
#    MBT.plot(color = 'k')
#    
#    ylabel('Intensity (a.u.)')
#    xlabel('Raman shift (cm$^{-1}$)')
#    annotate('MBT',(0.02,0.9), xycoords = 'axes fraction',
#                    color = 'k',
#                    horizontalalignment = 'left',
#                    size = 12)
#    ics('/home/chris/Orca/Successful/Methylbenzenethiol/methylbenzenethiol.out',normalize=True,color = 'r',labelpeaks = False)
#    xlim(500,1700)
#    ylim(-0.01,1.2)
#    legend(['expt', 'calc'])  
#    
#                    
#                    
#    ####Assignments
#    assignmentfontsize = 10
#   # annotate('Ring bending',(635,0.2), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('Ring bending',(647,0.38), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('Ring stretching',(1105,1.05), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal')
#    annotate('Ring stretching',(806,0.6), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('CSH bending ',(914,0.09), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('CH bending ',(1190,0.25), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('Ring stretching',(1225,0.4), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('CH bending',(1382,0.1), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    annotate('CC ring stretching',(1607,0.05), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
#    
#    
#    subplot(212)
#    CdMBT.plot(color = 'k')
#    
#    ylabel('Intensity (a.u.)')
#    xlabel('Raman shift (cm$^{-1}$)')
#    annotate('Cd(MBT)$_2$',(0.02,0.9), xycoords = 'axes fraction',
#             color = 'k',
#             horizontalalignment = 'left',
#             size = 12)
#             
#    ### Plot Raman calculation
#    ics('/home/chris/Orca/Successful/CdMBT/CdMBT.out',normalize=True,color = 'r',labelpeaks = False)
#    
#   
#    legend(['expt', 'calc']) 
#    xlim(500,1700)
#    ylim(-0.01,1.2)
# 
#     ####Assignments
#    #annotate('CS$_{\\nu}$',(639,0.38), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
#    #annotate('$\phi$CC$_{\\nu}$',(1088,1.05), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
#    #annotate('Ring CH$_\delta,oop$ ',(796,0.6), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
#    #annotate('$\phi$CC$_{\\nu}$ ',(1600,0.45), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
#
#    matplotlib.pyplot.tight_layout()
#    return 0
def Fig2(show_vib_numbers = False): ### reference spectra of methoxythiphenol
    figure(figsize = (6,6))
    a= loadtxt('/home/chris/Documents/DataWeiss/141014/4_methoxythiophenol_1.csv',
                  delimiter = ',',
                  unpack = True)
    MBT = pandas.Series(a[1],a[0])
    MBT-=min(MBT[0:2000])
    MBT/=max(MBT[0:2000])
    
    #a = loadtxt('/home/chris/Documents/DataWeiss/140918/9_MeOTP_1.txt',
    #              delimiter = ',',
    #              unpack = True)
    CdMBT = RamanSpectrum('/home/chris/Documents/DataWeiss/140918/9_CdMeOTP_1.txt')
   
    CdMBT-=min(CdMBT[200:1000])
    CdMBT/=max(CdMBT[500:2000])
    
   
    
    subplot(211)
    MBT.plot(color = 'b')
   
    
    xlim(500,1700)
    ylim(-0.01,1.2)
    ylabel('Intensity (a.u.)')
    xlabel('Raman shift (cm$^{-1}$)')
    annotate('MTP',(0.01,0.9), xycoords = 'axes fraction',
                    color = 'k',
                    horizontalalignment = 'left',
                    size = 12)
    
    
    legend(['expt', 'calc']) 
    
  
                    
                    
    ####Assignments
    assignmentfontsize = 10
    annotate('Ring bending',(647,0.25), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('Ring stretching',(1098,0.8), xytext=(1070,1.05), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops = {'width':2,'color':'k','headwidth':5})
    annotate('Ring stretching',(805,1.02), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal')
    annotate('CSH bending ',(914,0.25), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('CH bending ',(1190,0.35), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('Ring stretching',(1245,0.15), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    #annotate('CH bending',(1382,0.1), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='vertical')
    annotate('CC ring stretching',(1590,0.65),xytext=(1557,0.75), xycoords = 'data',horizontalalignment = 'center',verticalalignment = 'bottom',color = 'k',size = assignmentfontsize,rotation ='horizontal',arrowprops = {'width':2,'color':'k','headwidth':5})
    
    
    subplot(212)
    
    CdMBT.plot(color = 'k')
    ics('/home/chris/Orca/Successful/CdMeOTP/CdMeOTP.out',normalize=True,color = 'r', labelpeaks = False)
 
    xlim(500,1700)
    ylim(-0.01,1.6)
    ylabel('Intensity (a.u.)')
    xlabel('Raman shift (cm$^{-1}$)')
    annotate('Cd(MTP)$_2$',(0.01,0.9), xycoords = 'axes fraction',
             color = 'k',
             horizontalalignment = 'left',
             size = 12)
             
          
     ####Assignments
    #annotate('CS$_{\\nu}$',(639,0.38), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
    #annotate('$\phi$CC$_{\\nu}$',(1088,1.05), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
    #annotate('Ring CH$_\delta,oop$ ',(796,0.6), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
    #annotate('$\phi$CC$_{\\nu}$ ',(1600,0.45), xycoords = 'data',horizontalalignment = 'center',color = 'k',size = assignmentfontsize)
    
    matplotlib.pyplot.tight_layout()
    return 0
    

    

def Apr8Raman():
    os.chdir('/home/chris/Documents/DataWeiss/150408')
    fig = figure()
    a = RamanSpectrum('150408_15.txt')
    a.autobaseline((268,440,723,915,1200,1391,1505,1680),specialoption='points', order = 4)
    a.smooth(window_len=11,window = 'SG')
    #a+=800
    
    b = RamanSpectrum('150408_02.txt')
    #b = autobaseline(b,(200,1700),leaveout=(200,300), order = 4)
    b.autobaseline((268,440,723,915,1200,1391,1505,1680),specialoption='points', order = 4)
    b.smooth(window_len=11,window = 'SG')
    
    (normalize(MeOTPRef,(0,10000))*4000+1000).plot(color ='b',linewidth=2)
    a.plot(color = 'k',linewidth = 2)
    b.plot(color = 'r', linewidth = 2)
    
    ylim(-500,6000)
    xlim(200,1675)
    
    
    
    legend(['MeOTP ref', 'MeOTP treated','Native ligand only'])
    
    ylabel('Raman Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')
    
    figure()
    title('Washing')
    a = RamanSpectrum('150408_11.txt')
    b = RamanSpectrum('150408_02.txt')
    a = autobaseline(a, (200,1700),leaveout=(200,300),order=4)
    b = autobaseline(b,(200,1700),leaveout=(200,300), order = 4)
   
    (normalize(ODPARef,(0,10000))*4000+2000).plot(color ='b',linewidth=2, label='ODPA Ref')
    a.plot(color = 'r',label='washed 5x')
    b.plot(color = 'k',label='washed 4x')
    #a= fitspectrum(b,(900,1150),'SixGaussian', [200,200,200,200,200,200,950,990,1026,1064,1087,1115,10,10,10,10,10,10,1,-100])
    #plot(a[1],a[2],linewidth =3,label='fit')
    legend()
    ylabel('Raman Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')
    return 0


    
def smooth_phonon():
    import RamanTools2
    
    aa = RamanSpectrum('/home/chris/Documents/DataWeiss/141029/4_RubyRed in PS phonon_1.txt')
     
    
    aa-=min(aa)    
    aa/=max(aa)
    aa._smooth(aa.values,window = 'flat')  
    
    aa.plot(color = 'r')
   
    return aa

def hthiol():
    a = loadtxt('/home/chris/Orca/hexanethiol/RamanSpectrum.txt',delimiter=',',unpack=True,skiprows=2)
    b = RamanTools3.RamanSpectrum('/home/chris/Documents/DataWeiss/150113/17.SPE')
    b-=min(b)
    
    b/=max(b)
    b*=max(a[2])
    b=RamanTools3._smooth(b)
    b.plot()
    vlines(a[1],0,a[2],linewidth=2)
    return 
    

def OPAFig():
    os.chdir('/home/chris/Documents/DataWeiss')
    a = copy(CdOPARef)
    b = copy(OPARef)
    a.autobaseline((211,600,756,1144,1503,1802),specialoption='points',order = 5)
    b.autobaseline((224,458,686,916,977,1184,1393,1511,1802),specialoption='points',order=6)
    
    a.smooth()
    b.smooth()
    a = normalize(a,(800,1600))
    b = normalize(b,(800,1600))
    
    figure()
    subplot(211)
    b.plot(color = 'b')
    annotate( "CH$_2$ def",(1450,1))
    annotate("CH$_2$ twist",(1250,1.05))
    annotate("CC stretch",(1025,1))
    annotate("P-OH bend",(945,0.5),rotation ='vertical',verticalalignment='bottom')#xytext = (930,0.2),arrowprops = {'width':2,'color':'k','headwidth':5})
    annotate("P-C stretch",(740,1.2),rotation ='horizontal')#xytext= (688,0.25), arrowprops = {'width':2,'color':'k','headwidth':5})
    annotate("CH$_3$ rock",(880,0.4),rotation ='vertical',verticalalignment='bottom')#xytext = (840,0.3),arrowprops = {'width':2,'color':'k','headwidth':5})    
    
    ylabel('Raman Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)')   
    xlim((300,1800))
    ylim((-0.1,1.3))
    annotate('OPA',(0.01,0.9), xycoords = 'axes fraction',
                    color = 'k',
                    horizontalalignment = 'left',
                    size = 12)
    
   
 
    subplot(212)
    a.plot(color ='b')
    annotate( "CH$_2$ def",(1406,0.9))
    annotate("CH$_2$ twist",(1254,0.8))
    annotate("CC stretch",(1025,1.05))
    #annotate("P-OH bend",(,0.4))
    annotate("P-C stretch",(779,0.7),rotation ='vertical',verticalalignment='bottom')#xytext= (671,0.5), arrowprops = {'width':2,'color':'k','headwidth':5})
    annotate("CH$_3$ rock",(884,0.85),rotation ='vertical')#xytext= (840,0.4), arrowprops = {'width':2,'color':'k','headwidth':5})  
    annotate("PO$_{3}$$^{2-}$ stretch",(835,0.3),rotation ='vertical',verticalalignment = 'bottom')#xytext= (840,0.4), arrowprops = {'width':2,'color':'k','headwidth':5})  
    
    xlim((300,1800))
    ylim((-0.1,1.3))
       
    ylabel('Raman Intensity (a.u.)')
    xlabel('Raman Shift (cm$^{-1}$)') 
    annotate('CdOPA',(0.01,0.9), xycoords = 'axes fraction',
                    color = 'k',
                    horizontalalignment = 'left',
                    size = 12)
    
    
     
    
    #import_calcd_spectrum('/home/chris/Orca/ODPA/ODPA.out',normalize = True)
    return 0

  
    
    
    
    
    

    
    
