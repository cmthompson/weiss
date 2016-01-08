

from Tkinter import *
import tkFileDialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from ThinFilmFresnel import respace_x
from SFG_Analysis import SG_Smooth
import threading
import Queue
import pickle
import pdb

from matplotlib.pyplot import plot, legend, ioff,gcf,clf,cla,show
from matplotlib.figure import Figure
from numpy import *
import numpy
import pandas
import time



Pt = 0
Ethoxy = 1
Al = 2
OH = 3
Oads = 4
Pt_ss = 5
SO = H= 6
EtOH = 7
Ox = 8


PLOT = 0
UPDATE_PROGRESS = 1
RESET_MENU =2

endall = 0



def dX_dt(X,time_in,model,minstep = 1E-3, parameters = None):
    global mwin , eVc  
    
    
    if parameters == None:
        k1 =0.8 #ethanol adsorption
        _k1 =0.0007# Ethanol desorption
        k2 = 0.001#0.001#140# 5 ### Jelemensky = 10 # second dehydrogenation onto Pt (assume similar as with OH)
        k3 = 1#5#11.25 # Reaction of adosorbed ehtanol with PtOH
        k4 = 1# 2.025  # Reaction of of Ethanol with PtO
        
        k5 =0.2#1E-4#100#100#1 4# 50#4.5 # desoprtio of aldehyden
        k6 =5E6 #O2 adsorption
        _k6 =50# O2 des
        k7 =0#  100 # O <-> OH speed factor
        
        k8 = 100#100 #reacgtion of PtO with PtH (assume 100)
        k9 = 100#100# reaction of PtOH with PtH (assume 100)
        g =  0
        vOads = 1.53  ### set this to the 1.23/0.2+0.3  (maximum coverage is 0.2)
        vOH =  1.53# 4.3  ### set this to the 0.8/0.2 + 0.3   assumed a surface covered with OH should be at 0.8V
        voffset = -0.3  ### surface with no oxygen should be at -0.3 V??
    else:
        (k1,_k1,k2, k3,k4 ,k5,k6 ,k7,_k7,k8 ,k9 ,g ,vOads,vOH,voffset) = parameters  ### su
            
    time_elapsed = 0
    dX = numpy.zeros(X.shape)
    X_init = copy(X)
    X_keeptrack = array([X])
    t_keeptrack = array([0])
    
   
    numcycles = 0
    while(time_elapsed<0.1):
        numcycles +=1
        if numcycles>1E4:
           
            
           minstep*=10
       
        
        timeconstant = 0.1
        
        V_oc = (vOads*X[Oads] + vOH*X[OH]+voffset)
    
        dX[Ethoxy] = timeconstant*(k1*X[Pt]*X[EtOH]
                                -_k1*X[Ethoxy]*X[H]  
                                - k2*X[Ethoxy]#*(-exp(V_oc+0.2)) 
                                - k3*X[Ethoxy]*X[OH] 
                                - k4*X[Ethoxy]*X[Oads])
        
        dX[Al] = timeconstant*(k2*X[Ethoxy]#*exp(eVc*V_oc) 
                                + k3*X[Ethoxy]*X[OH] 
                                + k4*X[Ethoxy]*X[Oads] 
                                - k5*X[Al])#*exp(10*V_oc))
                                
        dX[OH]= timeconstant*(k8*X[Oads]*X[H] 
                                - k7*20*X[OH]**2*exp((V_oc-0.6)/2)
                                + k7*X[Oads]*X[Pt]*exp(-(V_oc-0.6)/2)
                                - k3*X[Ethoxy]*X[OH] 
                                -k9*X[OH]*X[H])
                                
        dX[Oads] = timeconstant*(2*k6*X[Pt]**2*X[Ox]*exp(-g*(V_oc+0.3)/2) 
                                - 2*_k6*X[Oads]**2*exp(g*(V_oc+0.3)/2)
                                + k7*20*X[OH]**2*exp((V_oc-0.6)/2)
                                - k7*X[Oads]*X[Pt]*exp(-(V_oc-0.6)/2)
                                - k4*X[Ethoxy]*X[Oads]
                                -k8*X[Oads]*X[H]) 
                                
        dX[H] = timeconstant*(k1*X[Pt]*X[EtOH]
                            -_k1*X[Ethoxy]*X[H] 
                            +k2*X[Ethoxy]#*(-exp(V_oc+0.2)) 
                            - k8*X[Oads]*X[H] 
                            -k9*X[OH]*X[H]
                            +0.0)
        
            
      
          
        
        
        if any(numpy.isnan(dX)):
            print 'nan error', where(numpy.isnan(dX))[0]
            print X
        elif any(numpy.isinf(dX)):
            print 'inf error', where(numpy.isinf(dX))[0]
             
            print X
           
            
            dX[dX == nan] = 0
            dX[dX == inf] = 1
        if max(numpy.absolute(dX))< 1E-5:
            
            print 'max change', max(numpy.absolute(dX))
            (X, time_in+0.1) 
       
      
            
        divisor = max(numpy.absolute(dX))/minstep 
        dX/=divisor
            
            
        timeconstant/=divisor
        if numpy.isnan(timeconstant):
            print 'time constant isnan'
        elif numpy.isinf(timeconstant):
            print 'time constant isinf'
        
        
        
                
       
        if model == 'Jelemensky' or model =='JelemenskyMod' or model == 'JelemenskyNoSO' :
            X+=dX  
            X[Pt] = 1-sum(X[array([Ethoxy,Al,OH,Oads])])
            X[Pt_ss]=1-X[SO]
            X[X>1]=1#X[where(X>1)[0]]=1
            X[X<0]=0#X[where(X<0)[0]]=0
        elif model == 'Simple Langmuir-Hinshelwood' or 'L-H' in model:
            
            X+=dX  
            X[Pt] = 1-sum(X[array([Ethoxy,Al,OH,Oads])])#1-sum(X[array([Ethoxy,Al,OH,Oads,H])])
            X[Pt_ss]=V_oc
            
            i = array([Ethoxy,Al,OH,Oads])
           # X[i][X[i]>1]=1#X[where(X>1)[0]]=1
            X[H] = min(X[H],5)
            X[i][X[i]>1]=1
            X[X<0]=0#X[where(X<0)[0]]=0
            X[Pt_ss]=V_oc
        else:
            print 'model not regcognized. 2'
            
        
       
        
        
        time_elapsed += timeconstant
        X_keeptrack = numpy.append(X_keeptrack,array([X]),axis = 0)
        t_keeptrack = numpy.append(t_keeptrack,time_elapsed)
       
        
       
    out_time = time_in+time_elapsed
  
    return (X, out_time)      






class RateRunout(object):
    
    _type = None
    _induc = False
    
    
    conc = zeros((9,1))
    time_array = array([0])
    initials = ndarray((9,1)) 
    finals = ndarray((9,1))
    
    def __init__(self, inits = None, _plot = False, _type = -1):
        self.initials = inits
        
        if inits == None:
            self.conc = array([0,0,0,0,0,1,1,1,1E-6])
            
        elif inits == 'default':
            self.conc[0]  =array([[0,0.3,0.3,0.05,0,0.1,0,1,0.001]])
            self.conc[0,Pt] = 1-sum(self.conc[1:5,0])
            self.conc[0,Pt_ss] = 1-self.conc[SO,0]
        else:
            self.conc = numpy.array([self.initials])
        self._type = _type
        
        
       
        return None
        
      
    
    def RunOut(self, model, _plot = False, time_limit = 1000,slope_limit = 1E-8,break_param = False):
              
        global mwin,dX_dt
        
        time_limit = max(self.time_array)+time_limit
        
        for t in range(20):
            
            
            z = dX_dt(self.conc[-1],self.time_array[-1],model,minstep = 0.001)
            
            self.conc = numpy.append(self.conc,array([z[0]]),axis = 0)
            
            self.time_array = append(self.time_array,z[1])
           
            i_count = 0
            max_delta = numpy.max(numpy.absolute(self.conc[-1]-self.conc[0]))
            try:
                if break_param == True:
                    
                    print 'programmed stopped by user'
                    print "max_delta", str(max_delta)
                    return 0
            except:
                print "something's not defined in RateRunout.RunOut"
            print self.time_array[-1]
        
        while max_delta>slope_limit and numpy.max(self.time_array)<time_limit:
            
          
            
             
            z = dX_dt(self.conc[-1],self.time_array[-1],model,minstep = 0.001) 
            
            self.conc = numpy.append(self.conc,array([z[0]]),axis = 0)
            self.time_array = append(self.time_array,z[1])
            
            i_count +=1
            max_delta = numpy.max(numpy.absolute(self.conc[-1]-self.conc[-19]))/(self.time_array[-1]-self.time_array[-19])
            
            if break_param == True:
                
                print 'programmed stopped by user'
                print "max_delta", str(max_delta), "per second"
                break
        print "max_delta", str(max_delta),"per second"
        print "time end", max(self.time_array)
        
        
       
        if _plot == True:
            
            self.PlotRunOut()
            
        return 0
        
    def PlotRunOut(self, _fig = None):
        if _fig == None:
            _fig = gcf()
        _fig.clf()
        ax1=_fig.add_subplot(211)
        x= '-'
        try:
            ax1.plot(self.time_array,self.conc[:,Pt],x)
            ax1.plot(self.time_array,self.conc[:,1],x)
            ax1.plot(self.time_array,self.conc[:,2],x)
            ax1.plot(self.time_array,self.conc[:,3],x)
            ax1.plot(self.time_array,self.conc[:,4],x)
            ax1.plot(self.time_array,self.conc[:,5],'-.')
            ax1.plot(self.time_array,self.conc[:,6],'-.')
            ax1.legend(['Pt', 'E', 'Al', 'OH', 'O', 'V_oc','H'])
            
            ax2 = _fig.add_subplot(212)
            ax2.plot(self.time_array,self.conc[:,2])
            #CheckForInduction(self.conc[Al],time_array= self.time_array)
        except:
            pass
         
        return 0
    def SetType(self, _type):
        self._type = _type
        return 0
    def SetInduc(self,boolean):
        self._induc = boolean
        return 0





def go():
    
    global eVc
    eVc = 0
    a = array([  0,  # pt
                1,  # ethoxy
                0,    ###aldehyde
                0.0, ##OH
                0.0,  # oxide
                0,  #pt subsurface
                5,   #h so
                1,  
                50E-6])
    a[Pt] = 1-sum(a[array([Ethoxy,OH,Oads,Al])])
    

    x = RateRunout(inits = a)
    #threading.Thread(target = x.RunOut, args = ('Jelemensky',), kwargs = {'time_limit':10,'_plot':True} ).start()
    x.RunOut('L-H with ethoxy switch',time_limit = 2000,_plot = True)
    
    
    return x


    
  




        
    
    
        