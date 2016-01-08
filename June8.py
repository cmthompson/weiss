# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:59:20 2015

@author: chris
"""

from ramanTools.RamanTools import *

def June8washalternative():
    clf()
    
    pointfornormalization = 1065
    a = RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_02.txt')
    a = SPIDcorrect785(a)
    a.smooth(window='SG')
    a.autobaseline((292,632), order = 2)
    a.autobaseline((632,905), order = 0,join='start')
    a.autobaseline((905,1180), order = 0,join='start')
    a.autobaseline((1180,1390), order = 0,join='start')
    a.autobaseline((1390,1534), order = 0,join='start')
    a.autobaseline((1534,2000), order = 0,join='start')
    a[:]/=a[pointfornormalization]
    r = fitspectrum(a,(909,1185),'xGaussian',[1,1,1,1,1,1,1,950,986,1034,1040,1060,1080,1117,5,5,5,5,5,5,5,0,0])
    print r.params[0][7:14]
    outlist = [r.params[0][0]*sqrt(r.params[0][14])*sqrt(pi),
          r.params[0][1]*sqrt(r.params[0][15])*sqrt(pi),
          r.params[0][2]*sqrt(r.params[0][16])*sqrt(pi),
          r.params[0][3]*sqrt(r.params[0][17])*sqrt(pi),
          r.params[0][4]*sqrt(r.params[0][18])*sqrt(pi),
          r.params[0][5]*sqrt(r.params[0][19])*sqrt(pi),
          r.params[0][6]*sqrt(r.params[0][20])*sqrt(pi)]
    print outlist    
         
   # plot(r.x,r.y)
    a.plot()
    
    a = RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_03.txt')
    a = SPIDcorrect785(a)
    a.smooth(window='SG')
    a.autobaseline((292,632), order = 2)
    a.autobaseline((632,905), order = 0,join='start')
    a.autobaseline((905,1180), order = 0,join='start')
    a.autobaseline((1180,1390), order = 0,join='start')
    a.autobaseline((1390,1534), order = 0,join='start')
    a.autobaseline((1534,2000), order = 0,join='start')
    a[:]/=a[pointfornormalization]
    r = fitspectrum(a,(909,1185),'xGaussian',r.params[0])
    print r.params[0][7:14]
    outlist = [r.params[0][0]*sqrt(r.params[0][14])*sqrt(pi),
          r.params[0][1]*sqrt(r.params[0][15])*sqrt(pi),
          r.params[0][2]*sqrt(r.params[0][16])*sqrt(pi),
          r.params[0][3]*sqrt(r.params[0][17])*sqrt(pi),
          r.params[0][4]*sqrt(r.params[0][18])*sqrt(pi),
          r.params[0][5]*sqrt(r.params[0][19])*sqrt(pi),
          r.params[0][6]*sqrt(r.params[0][20])*sqrt(pi)]
    print outlist    
         
   # plot(r.x,r.y)
    a.plot()
    
    a = RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_10.txt')
    a = SPIDcorrect785(a)
    a.smooth(window='SG')
    a.autobaseline((292,632), order = 2)
    a.autobaseline((632,905), order = 0,join='start')
    a.autobaseline((905,1180), order = 0,join='start')
    a.autobaseline((1180,1390), order = 0,join='start')
    a.autobaseline((1390,1534), order = 0,join='start')
    a.autobaseline((1534,2000), order = 0,join='start')
    a[:]/=a[pointfornormalization]
    r = fitspectrum(a,(909,1185),'xGaussian',r.params[0])
    print r.params[0][7:14]
    outlist = [r.params[0][0]*sqrt(r.params[0][14])*sqrt(pi),
          r.params[0][1]*sqrt(r.params[0][15])*sqrt(pi),
          r.params[0][2]*sqrt(r.params[0][16])*sqrt(pi),
          r.params[0][3]*sqrt(r.params[0][17])*sqrt(pi),
          r.params[0][4]*sqrt(r.params[0][18])*sqrt(pi),
          r.params[0][5]*sqrt(r.params[0][19])*sqrt(pi),
          r.params[0][6]*sqrt(r.params[0][20])*sqrt(pi)]
    print outlist    
    a.plot()
    
        
    a = add_RamanSpectra(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150609/150609_03.txt'),RamanSpectrum('/home/chris/Dropbox/DataWeiss/150609/150609_04.txt'))
   
    a = SPIDcorrect785(a)
    
    a.smooth(window='SG')
    a.autobaseline((292,500), order = 0)
    a.autobaseline((500,632), order = 0,join='start')
    a.autobaseline((632,905), order = 0,join='start')
    a.autobaseline((905,1180), order = 0,join='start')
    a.autobaseline((1180,1587), order = 0,join='start')
    #a.autobaseline((1390,1535), order = 0,join='start')
   # a.autobaseline((1534), order = 0,join='start')
    a[:]/=a[pointfornormalization]
    r = fitspectrum(a,(909,1185),'xGaussian',r.params[0])
    print r.params[0][7:14]
    outlist = [r.params[0][0]*sqrt(r.params[0][14])*sqrt(pi),
          r.params[0][1]*sqrt(r.params[0][15])*sqrt(pi),
          r.params[0][2]*sqrt(r.params[0][16])*sqrt(pi),
          r.params[0][3]*sqrt(r.params[0][17])*sqrt(pi),
          r.params[0][4]*sqrt(r.params[0][18])*sqrt(pi),
          r.params[0][5]*sqrt(r.params[0][19])*sqrt(pi),
          r.params[0][6]*sqrt(r.params[0][20])*sqrt(pi)]
    print outlist   
         
 
   
    a.plot()
    
    a = add_RamanSpectra(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150610/150610_01.txt'),RamanSpectrum('/home/chris/Dropbox/DataWeiss/150610/150610_02.txt'))
   
    a = SPIDcorrect785(a)
    
    a.smooth(window='SG')
    a.autobaseline((300,500), order = 0)
    a.autobaseline((500,632), order = 0,join='start')
    a.autobaseline((632,905), order = 0,join='start')
    a.autobaseline((905,1180), order = 0,join='start')
    a.autobaseline((1180,1480), order = 0,join='start')
    #a.autobaseline((1390,1535), order = 0,join='start')
   # a.autobaseline((1534), order = 0,join='start')
    a[:]/=a[pointfornormalization]
    r = fitspectrum(a,(909,1185),'xGaussian',r.params[0])
    print r.params[0][7:14]
    outlist = [r.params[0][0]*sqrt(r.params[0][14])*sqrt(pi),
          r.params[0][1]*sqrt(r.params[0][15])*sqrt(pi),
          r.params[0][2]*sqrt(r.params[0][16])*sqrt(pi),
          r.params[0][3]*sqrt(r.params[0][17])*sqrt(pi),
          r.params[0][4]*sqrt(r.params[0][18])*sqrt(pi),
          r.params[0][5]*sqrt(r.params[0][19])*sqrt(pi),
          r.params[0][6]*sqrt(r.params[0][20])*sqrt(pi)]
    print outlist   
         
 
   
    a.plot()
    
    
    legend(['No Wash', '1.5 mL','6.0 mL','20 mL','34 mL'])
    return 0
def June8wash():
    clf()
    f1 = gcf()

    ax1 = f1.add_subplot(211)
    ax2 = f1.add_subplot(212)
    
    listofspectra=list()
    midpeakintegrals = ndarray((8,0))
    lowpeakintegrals = ndarray((5,0))
    pointfornormalization = 1065
    listofspectra.append(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_02.txt'))
    listofspectra.append(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_03.txt'))
    listofspectra.append(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_10.txt'))
    listofspectra.append(add_RamanSpectra(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150609/150609_03.txt'),RamanSpectrum('/home/chris/Dropbox/DataWeiss/150609/150609_04.txt')))
    listofspectra.append(add_RamanSpectra(RamanSpectrum('/home/chris/Dropbox/DataWeiss/150610/150610_01.txt'),RamanSpectrum('/home/chris/Dropbox/DataWeiss/150610/150610_02.txt')))
    
#    guess = [1,1,1,1,1,1,1,950,986,1034,1040,1060,1080,1117,200,200,200,200,200,200,200]
    midguess = [1,1,1,1,1,1,1,1,1020,1040,950,986,1034,1060,1080,1117,15,15,15,15,15,15,15,15,0,0]
    lowguess = [1,1,1,1,1,690,730,750,780,800,15,15,15,15,15,0,0]
    p = ndarray((len(midguess),0))
    lowp = ndarray((len(lowguess),0))
    for x in range(len(listofspectra)):
        a = listofspectra[x]
        
        a.smooth(window='SG',window_len=11)
        
        a.autobaseline((297,623,911,1150,1191,1483), order = 4,specialoption='points')
        a.autobaseline((906,1144),order = 0)
        
        a[:]/=a[pointfornormalization]
        r = fitspectrum(a,(909,1139),'xGaussianNoBase',midguess)
        
        midguess = r.params[0]
        p = append(p,transpose([r.params[0]]), axis = 1)
        if x==0:
            for i in r.peaks:
                ax1.plot(r.x,i,'k')
            ax1.plot(r.x,r.y)

        outlist = list((i/r.areas[-1] for i in r.areas))
       

        midpeakintegrals=append(midpeakintegrals, transpose([outlist]),axis=1)
        
        r = fitspectrum(a,(635,823),'xGaussianNoBase',lowguess)
        lowguess = r.params[0]
        lowp = append(lowp,transpose([r.params[0]]), axis = 1)
      
        outlist = list((i/r.areas[-1] for i in r.areas))
              
        lowpeakintegrals=append(lowpeakintegrals, transpose([outlist]),axis=1)

        a.plot(ax=ax1)  
    
    ax1.legend(['No Wash', '1.5 mL','6.0 mL','20 mL','34 mL'])
    savetxt('/home/chris/Desktop/june8wash.csv', lowp, delimiter = ',') 
   
    for l in midpeakintegrals:
        l/=l[0]
    [ax2.plot([0,1,4,20,34],l,'s-') for l in midpeakintegrals]
#    [ax3.plot([0,1,4,20,34],l,'s-') for l in lowpeakintegrals]
    
    ax2.legend([str(i) for i in [0,950,986,1034,1060,1080,1117]])
#    ax3.legend([str(i) for i in [690,730,750,780,800]])
    return 
def June8Fluorescence():
    a= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_09.txt')
    b= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_06.txt')
    c= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150608/150608_13.txt')
    
    a.normalize()
    b.normalize()
    c.normalize()
    
    a.plot(color = 'k')
    b.plot(color ='r')
    c.plot(color = 'b')
    
    legend(['no wash', '1 wash', '4 washes'])
    
    return 0
    
def CdOPAvsDots():
    a= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150612/150612_01_CdSe.txt')
    #b= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150612/150612_05.txt')
    b= RamanSpectrum('/home/chris/Dropbox/DataWeiss/150521/150521_01.txt')
    b= removespikes(b)
    b[:]*=5
    c = RamanSpectrum('/home/chris/Dropbox/DataWeiss/150612/150612_07.txt')
    a.autobaseline((310,635,1196,1385,1515),specialoption='points',order=5)
    b.autobaseline((310,635,1196,1385,1515),specialoption='points',order=4)
    c.autobaseline((310,635,1196,1385,1515),specialoption='points',order=4)
    a.plot()
    b.plot()
    c.plot()
    return 0


    
