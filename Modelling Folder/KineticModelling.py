

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
    if model == 'Jelemensky':
        k1 = 6.2465E6 #Oxygen Adsorption Rate
        k2 = 9.5E-4 #OH to O conversion rate   
        _k2 = 1E-3 # O to OH converstion rate
        k3 = 2.8E-5  # PtO --> SO conversion
        _k3 = 1E-5
        k4 = 67.5   # Ethanol adsorption
        _k4 = 29.25 # Ethanol desorption
        k5 = 11.25 # Reaction of adosorbed ehtanol with OH
        k6 = 2 # reaction of aldehyde with OH
        k7 = 4.5 # desoprtio of aldehyden
        _k7 = 112.5
        k8=  2.025  # Reaction of of Ethanol with PtO
        k9 = 0.45  # Reaction of aldehdye with PtO to form acetate
        k10= 0.01  #Reaction of SO with E
        k11 = 0.01  # Reaction of SO with Al
        gOH = 0.5
        gE = -0.5
        gSO = 2.00
        DO = 24.5
        DSO = 7.3
        uO = 4*k1*X[Ox]/k5
        uE = k4*X[EtOH]/k5
    elif model == 'JelemenskyMod' or model == 'JelemenskyNoSO':
        k1 = 6.2465E6 #Oxygen Adsorption Rate
        k2 = 9.5E-4 #OH to O conversion rate   
        _k2 = 1E-3 # O to OH converstion rate
        k3 = 2.8E-5  # PtO --> SO conversion
        _k3 = 1E-5
        k4 = 67.5   # Ethanol adsorption
        _k4 = 29.25 # Ethanol desorption
        k5 = 11.25 # Reaction of adosorbed ehtanol with OH
        k6 = 0 # reaction of aldehyde with OH
        k7 = 4.5 # desoprtio of aldehyden
        _k7 = 112.5
        k8=  2.025  # Reaction of of Ethanol with PtO
        k9 = 0  # Reaction of aldehdye with PtO to form acetate
        k10= 0.01  #Reaction of SO with E
        k11 = 0 # Reaction of SO with Al
        gOH = 0.5
        gE = -0.5
        gSO = 2.00
        DO = 25
        DSO = 7.3
        uO = 4*k1*X[Ox]/k5
        uE = k4*X[EtOH]/k5
        vOads = 0.7*25
        vOH = 0.01*25
        voffset = -0.4
    elif model == 'Simple Langmuir-Hinshelwood' or 'L-H' in model:
        if parameters == None:
            k1 = 0.5 #ethanol adsorption
            _k1 =0.0001# Ethanol desorption
            k2 = 0.001### Jelemensky = 10 # second dehydrogenation onto Pt (assume similar as with OH)
            k3 = 0.01# Reaction of adosorbed ehtanol with PtOH
            k4 = 0# Reaction of of Ethanol with PtO
            
            k5 =0.01#1E-2#100#100#1 4# 50#4.5 # desoprtio of aldehyden
            k6 =6E5#1E7 #1 1E5#6.246E6 #O2 adsorption
            _k6 =0#k6*16#11.6E5# 1E4 O2 des
            k7 =0#  100 # O <-> OH speed factor
            
            k8 = 10#100#100 #reacgtion of PtO with PtH (assume 100)
            k9 =10# 100#100# reaction of PtOH with PtH (assume 100)
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
        try:
            if  mwin.endflag == True:
                
                break
            
            if endall == True:
                break
        except:
            "Something's not defined"
        
        timeconstant = 0.1
        
            
                
        if model == 'Jelemensky':
             dX[OH] = timeconstant*(uO*X[Pt]**4*exp(-gOH*X[OH]-gSO*X[SO]) - 2*X[Ethoxy]*X[OH]**2 - 2*k6*X[Al]*X[OH]**2 - 2*k2*X[OH]**2*exp(DO*X[Oads]) + 2*_k2*X[Oads]*X[Pt]*exp(-DO*X[OH]))
            
             dX[Ethoxy]= timeconstant*(uE*X[EtOH]*X[Pt]**2*exp(-gE*X[Ethoxy]) - _k4*X[Ethoxy]**2*exp(gE*X[Ethoxy])-X[Ethoxy]*X[OH]**2 - k8*X[Ethoxy]*X[Oads]-k10*X[Ethoxy]*X[SO])
            
             dX[Al]=  timeconstant*(X[Ethoxy]*X[OH]**2  + k8*X[Ethoxy]*X[Oads] + k10*X[Ethoxy]*X[SO] - k6*X[Al]*X[Oads] - k11*X[Al]*X[SO] - k7*X[Al] + 0)
            
             dX[Oads]= timeconstant*(k2*X[OH]**2*exp(DO*X[Oads]) - _k2*X[Oads]*X[Pt]*exp(-DO*X[OH]) - k8*X[Ethoxy]*X[Oads] - k9*X[Al]*X[Oads] - k3*X[Oads]*X[Pt_ss]*exp(DSO*X[SO]) + _k3*X[SO]*X[Pt]*exp(-DSO*X[Oads]))
            
             dX[SO]= timeconstant*(k3*X[Oads]*X[Pt_ss]*exp(DSO*X[SO]) - _k3*X[SO]*X[Pt]*exp(-DSO*X[Oads]) - k10*X[Ethoxy]*X[SO] - k11*X[Al]*X[SO])
             dX[Pt] = -sum(dX[1:5])  
             dX[Pt_ss] = -dX[SO]
            
             dX[7:9]= 0
        elif model == 'JelemenskyMod':
             dX[OH] = timeconstant*(uO*X[Pt]**4*exp(-gOH*X[OH]-gSO*X[SO]) - 2*X[Ethoxy]*X[OH]**2 - 2*k6*X[Al]*X[OH]**2 - 2*k2*X[OH]**2*exp(DO*X[Oads]) + 2*_k2*X[Oads]*X[Pt]*exp(-DO*X[OH]))
            
             dX[Ethoxy]= timeconstant*(uE*X[EtOH]*X[Pt]**2*exp(-gE*X[Ethoxy]) - _k4*X[Ethoxy]**2*exp(gE*X[Ethoxy])-X[Ethoxy]*X[OH]**2 - k8*X[Ethoxy]*X[Oads]-k10*X[Ethoxy]*X[SO])
            
             dX[Al]=  timeconstant*(X[Ethoxy]*X[OH]**2  + k8*X[Ethoxy]*X[Oads] + k10*X[Ethoxy]*X[SO] - k6*X[Al]*X[Oads] - k11*X[Al]*X[SO] - k7*X[Al] + 0)
            
             dX[Oads]= timeconstant*(k2*X[OH]**2*exp(DO*X[Oads]) - _k2*X[Oads]*X[Pt]*exp(-DO*X[OH]) - k8*X[Ethoxy]*X[Oads] - k9*X[Al]*X[Oads] - k3*X[Oads]*X[Pt_ss]*exp(DSO*X[SO]) + _k3*X[SO]*X[Pt]*exp(-DSO*X[Oads]))
            
             dX[SO]= timeconstant*(k3*X[Oads]*X[Pt_ss]*exp(DSO*X[SO]) - _k3*X[SO]*X[Pt]*exp(-DSO*X[Oads]) - k10*X[Ethoxy]*X[SO] - k11*X[Al]*X[SO])
             dX[Pt] = -sum(dX[1:5])  
             dX[Pt_ss] = -dX[SO]
            
             dX[7:9]= 0
        elif model == 'JelemenskyNoSO':
             V_oc = (vOads*X[Oads] + vOH*X[OH]+voffset)/2
             
             dX[OH] = timeconstant*(uO*X[Pt]**4*exp(-gOH*X[OH]) - 2*X[Ethoxy]*X[OH]**2 - 2*k6*X[Al]*X[OH]**2 - k2*X[OH]**2*exp(V_oc) + _k2*X[Oads]*X[Pt]*exp(-V_oc))
            
             dX[Ethoxy]= timeconstant*(uE*X[EtOH]*X[Pt]**2*exp(-gE*X[Ethoxy]) - _k4*X[Ethoxy]**2*exp(gE*X[Ethoxy])-X[Ethoxy]*X[OH]**2 - k8*X[Ethoxy]*X[Oads])
            
             dX[Al]=  timeconstant*(X[Ethoxy]*X[OH]**2  + k8*X[Ethoxy]*X[Oads] - k6*X[Al]*X[Oads] - k7*X[Al] + 0)
            
             dX[Oads]= timeconstant*(k2*X[OH]**2*exp(V_oc) - _k2*X[Oads]*X[Pt]*exp(-V_oc) - k8*X[Ethoxy]*X[Oads] - k9*X[Al]*X[Oads] )
            
             dX[SO]= 0
             dX[Pt] = -sum(dX[1:5])  
             dX[Pt_ss] = 0
            
             dX[7:9]= 0
        elif model == 'Simple Langmuir-Hinshelwood':
            
            dX[Ethoxy] = timeconstant*(k1*X[Pt]**2*X[EtOH] -_k1*X[Ethoxy] - k2*X[Ethoxy]*X[Pt]  - k3*X[Ethoxy]*X[OH] - k4*X[Ethoxy]*X[Oads])
            
            dX[Al] = timeconstant*(k2*X[Ethoxy]*X[Pt]  + k3*X[Ethoxy]*X[OH] + k4*X[Ethoxy]*X[Oads] - k5*X[Al])
            dX[OH]= timeconstant*(k8*X[Oads]*X[H] +  2*k7*X[Oads]*X[Pt]- 2*_k7*X[OH]**2- k3*X[Ethoxy]*X[OH]  -k9*X[OH]*X[H])
            dX[Oads] = timeconstant*(2*k6*X[Pt]**2*X[Ox] +_k7*X[OH]**2 - k4*X[Ethoxy]*X[Oads] - k7*X[Oads]*X[Pt]-k8*X[Oads]*X[H] )
            dX[H] = timeconstant*(k1*X[Pt]**2*X[EtOH] +k2*X[Ethoxy]*X[Pt] - k8*X[Oads]*X[H] -k9*X[OH]*X[H] )
            dX[Pt] = -sum(dX[array([Ethoxy,Al,OH,Oads,H])])
            dX[Pt_ss] = 0
         
            dX[7:9]= 0
        elif model == 'L-H with O2 Frumkin':
            V_oc =(vOads*X[Oads] + vOH*X[OH]+voffset)/2
            
            dX[Ethoxy] = timeconstant*(k1*X[Pt]**2*X[EtOH]-_k1*X[Ethoxy]  - k2*X[Ethoxy]*X[Pt]  - k3*X[Ethoxy]*X[OH] - k4*X[Ethoxy]*X[Oads])
            
            dX[Al] = timeconstant*(k2*X[Ethoxy]*X[Pt]  + k3*X[Ethoxy]*X[OH] + k4*X[Ethoxy]*X[Oads] - k5*X[Al])
            dX[OH]= timeconstant*(k8*X[Oads]*X[H] +  2*k7*X[Oads]*X[Pt]*exp(V_oc)- 2*_k7*X[OH]**2*exp(-V_oc)- k3*X[Ethoxy]*X[OH]  -k9*X[OH]*X[H])
            dX[Oads] = timeconstant*(2*k6*X[Pt]**2*X[Ox]*4*(0.25-X[Oads]-X[OH])*exp(-g*X[Oads]) +_k7*X[OH]**2*exp(V_oc) - k4*X[Ethoxy]*X[Oads] - k7*X[Oads]*X[Pt]*exp(V_oc)-k8*X[Oads]*X[H] )
            dX[H] = timeconstant*(k1*X[Pt]**2*X[EtOH] +k2*X[Ethoxy]*X[Pt] - k8*X[Oads]*X[H] -k9*X[OH]*X[H] )
            
            dX[Pt_ss] = 0
         
            dX[7:9]= 0
       
        elif model == 'L-H with ethoxy switch':
            
            
            V_oc = (vOads*X[Oads] + vOH*X[OH]+voffset)
#            if V_oc > -0.2 :
#                k5 = 1E-2
#            else:
#                k5 = 1E-4
            
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
                                    
            dX[Oads] = timeconstant*(2*k6*X[Pt]**2*X[Ox]#*exp(-g*(V_oc+0.3)/2) 
                                    - 2*_k6*X[Oads]**2#*exp(g*(V_oc+0.3)/2)
                                    + k7*20*X[OH]**2#*exp((V_oc-0.6)/2)
                                    - k7*X[Oads]*X[Pt]#*exp(-(V_oc-0.6)/2)
                                    - k4*X[Ethoxy]*X[Oads]
                                    -k8*X[Oads]*X[H]) 
                                    
            dX[H] = timeconstant*(k1*X[Pt]*X[EtOH]
                                -_k1*X[Ethoxy]*X[H] 
                                +k2*X[Ethoxy]#*(-exp(V_oc+0.2)) 
                                - k8*X[Oads]*X[H] 
                                -k9*X[OH]*X[H]
                                +0.0)
            
            
        else: 
            print "model not recognized"
            return (X,0)
        
        if max(numpy.absolute(dX)) ==  nan or any(numpy.isnan(dX)) or any(numpy.isinf(dX)):
            print dX  
            print X
           
            print 'nan or inf error'
            dX[dX == nan] = 0
            dX[dX == inf] = 1
        if max(numpy.absolute(dX))< 1E-5:
            print max(numpy.absolute(dX))
        
       
      
            
        divisor = max(numpy.absolute(dX))/minstep 
        dX/=divisor
            
            
        timeconstant/=divisor
        
        
        
                
       
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


class ThreadControl:
        global endall
       
       
        def __init__(self,master,control_window,model = 'Jelemensky'):
                
                self.master = master
                self.c_window = control_window
                self.model = model
                self.periodicCall()
                print self.c_window.endflag
                return None
        def KinModelJelemensky(self, clear = True):
            global endall
    
            
            initial_conc = array([[0.5,0,0,0,0,0.1,0,1,0.001]])
            etohliq = 1
            

            if self.model == 'Simple Langmuir-Hinshelwood' :
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                for h in arange(0,1.25,0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o+h),e,al,oh,o,0,h,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            elif 'L-H' in self.model: 
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                for h in arange(0,1.25,0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o+h),e,al,oh,o,0,h,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            elif self.model == 'Jelemensky' or self.model == 'JelemenskyMod':
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                for so in arange(0,1.25,0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o),e,al,oh,o,1-so,so,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            elif self.model == 'JelemenskyNoSO':
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o),e,al,oh,o,1,0,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            else:
                print "Model not recognized:", self.model
                return 0
            print "Number of Initial Conditions", initial_conc.shape
            self.Command_GUI((UPDATE_PROGRESS,("0/"+str(initial_conc.shape[0]))))
            
            if clear == True:
                self.c_window.RR_list = []
                self.c_window.groups_list = []
                self.c_window.groups_name_list = []
           
                     
            for i in range(len(self.c_window.RR_list),initial_conc.shape[0]): 
                self.Command_GUI((UPDATE_PROGRESS,(str(i)+"/"+str(initial_conc.shape[0]))))
                RR = RateRunout(inits = initial_conc[i])
               
                RR.RunOut(self.model,slope_limit = 1E-3,break_param = self.c_window.endflag)
                
                
                self.Command_GUI((PLOT,RR))
                
                self.c_window.RR_list.append(RR)
#                if CheckForInduction(RR.conc[Al],time_array = RR.time_array, _plot = False) == True:
#                    
#                    
#                    
#                    temp_array = array([])
#                    if len(self.c_window.groups_list) == 0:
#                        RR.SetType(len(self.c_window.groups_list))
#                        self.c_window.groups_list.append(RR)
#                        self.c_window.groups_name_list.append(str(len(self.c_window.groups_list)))
#                        self.Command_GUI((RESET_MENU,))
#                        print "NEW TYPE FOUND. Group type " + str(RR._type)
#                       
#                    else:
#                        for group in self.c_window.groups_list:
#                            
#                            temp_array = append(temp_array,_correlate(RR.conc[Al],group.conc[Al]))
#                            
#                        if max(temp_array) > 0.8:
#                            group = self.c_window.groups_list[where(temp_array == max(temp_array))[0]]
#                            
#                            RR.SetType(group._type)
#                            
#                        
#                        else:
#                            
#                            RR.SetType(len(self.c_window.groups_list))
#                            self.c_window.groups_list.append(RR)
#                            self.c_window.groups_name_list.append(str(len(self.c_window.groups_list)))
#                            self.Command_GUI((RESET_MENU,))
#                            print "NEW TYPE FOUND. Group type " + str(RR._type)
                
                
                    
                self.c_window.PauseFlag.wait()
                
                
                if self.c_window.endflag == True:
                    print "Thread Control Received end commande"
                    break
                if endall == 1:
                    break
    
                
                
            
            print "progam finished"
            return 0
            
        
        def SpanParameters(self):
            global endall
    
            
            
            etohliq = 1
            

            return 0
           
        def Command_GUI(self,msg):
                
                
                self.c_window.queue.put(msg)
               
                
                return 0
        
        

        def periodicCall(self):
               
                if endall == 1:
                    time.sleep(0.1)
                    self.master.destroy()
                    return 0
                else:
                    self.c_window.Queue_Callback()
                    self.master.after(50,self.periodicCall)
                
                
                        
                return 0



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
        
      
    
    def RunOut(self, model, _plot = False, time_limit = 1000,slope_limit = 0,break_param = False):
              
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
            ax1.legend(['Pt', 'E', 'Al', 'OH', 'O', 'Pt_ss','SO'])
            
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

class Window(object):
    endflag = bool(False)
    control_thread = None
    def __init__(self, master  = None, upload = True):
        global saved
            
        if master  == None:
                self.top = Toplevel()
        else:
                self.top = master

        self.queue = Queue.Queue(maxsize = 2)
        
        self.frame = Frame(master = self.top)
        self.frame.grid()
        self.plotframe = Frame(master = self.frame)
        self.plotframe.grid(row = 0,column = 0, columnspan = 10)
       

        self.menubar = Menu(self.top)
        

       
        self.init_idx = 0

        self.nextbutton = Button(self.frame, text = 'next', command = self._next)
        
        self.nextbutton.grid(row = 1, column = 5)

        self.lastbutton= Button(self.frame, text ='last', command = self.last)
        self.lastbutton.grid(row = 1, column = 4)
        self.skiptenbutton= Button(self.frame, text ='print_inits', command = self.print_inits)
        self.skiptenbutton.grid(row = 1, column = 7)
        #self.inquirebutton= Button(self.frame, text ='')
        #self.inquirebutton.grid(row = 2, column = 7)
        self.RR_Entry = Entry(self.frame,width=5)
        self.RR_Entry.insert(END,"0")
        self.RR_Entry.grid(row=1,column=6)
        self.RR_Entry.bind("<Return>",self.Goto)
        
        self.clearRRbutton = Button(self.frame, text = 'clear', command = self.clearRR)
        self.clearRRbutton.grid(row = 1, column = 0)
        self.save = Button(self.frame, text = 'save',command = self.save)
        self.save.grid(row = 1,column = 1)
        self.loadbutton = Button(self.frame, text = 'load',command = self.loadwindow)
        self.loadbutton.grid(row = 3,column = 1)
        
        self.prog_label = Label(self.frame,width=20, height = 1, text = "0/0")
        self.prog_label.grid(row=2,column=6)
        
        self.types_label = Label(self.frame,width=20, height = 1, text = "0")
        self.types_label.grid(row=3,column=5)
        
        self.var_plot = IntVar()
        self.var_plot.set(0)
        self.plotbox = Checkbutton(self.frame, text = "plot", variable=self.var_plot)
        self.plotbox.grid(row = 3, column =6)
        
        self.startbutton= Button(self.frame, text ='start', command = self.start)
        self.startbutton.grid(row = 2, column = 0)
        self.pausebutton= Button(self.frame, text ='pause', command = self.pause)
        self.pausebutton.grid(row = 2, column = 1)
        self.quitbutton= Button(self.frame, text ='stop', command = self.stop)
        self.quitbutton.grid(row = 2, column = 2)
        self.show_list = list()
        
        self.groups_name_list = ['all']
        
        self.var_curr_group = StringVar()
        self.var_curr_group.set('all')
        self.groupMenu = OptionMenu(self.frame,self.var_curr_group, *self.groups_name_list, command = self.updategroup)
        self.groupMenu.grid(row = 5,column =6,sticky = W)
       
        self.groups_list = list()
        self.RR_list = list()
        self.show_list = list()
        
        
           
                    
            
        
        
        
        self.PauseFlag = threading.Event()
        self.PauseFlag.set()
        
        self.figure = Figure(figsize = (5,5))
        self.canvas = FigureCanvasTkAgg(self.figure,master = self.plotframe)
        self.canvas.show()
        
        self.canvas._tkcanvas.grid()
        
        #self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.plotframe)
        #self.toolbar.update()
        #self.toolbar.grid()
        
        self.canvas.draw()
        
        self.top.config(menu= self.menubar)
        
      
                      
        return None
    def Queue_Callback(self):
            
            
        while self.queue.qsize():
            try:
                msg = self.queue.get()
                
                
                if msg[0] == PLOT:
                    
                    if self.var_plot.get() == 1:
                        msg[1].PlotRunOut(_fig = self.figure)
                        self.canvas.draw()
                        
                        
                            
                        
                elif msg[0] == UPDATE_PROGRESS:
                    self.prog_label.config(text = msg[1])
                elif msg[0] == RESET_MENU:
                    self._reset_option_menu(*self.groups_name_list)
                    
                       
                else:
                    print "unidentified msg"
                
                    
                            

                        
            except Queue.Empty:
                pass
            except:
                print "exception in queue"

        
        return 0
    
    
    def _reset_option_menu(self, *options):
        '''reset the values in the option menu

        if index is given, set the value of the menu to
        the option at the given index
        '''
        menu = self.groupMenu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                 self.updategroup(value))
       
        return 0
                
                
    def clearRR(self):
        self.RR_list = []
        self.groups_list = []
        self.groups_name_list = []    
        self.prog_label.config(text = '0/0')
        return 0
        
    def _next(self):
        
        clf()
        
        
        if self.init_idx<len(self.show_list)-1:
            self.init_idx+=1
            self.show_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.canvas.draw()
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
        
        else:
            
            print "last file to show"
                    
            
        return 0
    def last(self):
        
        clf()
        if self.init_idx>=0:
            self.init_idx-=1
            self.show_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.canvas.draw()
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
        
        else:
            
            print "already on first file"
                    
            
        return 0
    def Goto(self,extra):
         self.init_idx = int(self.RR_Entry.get())
         if self.init_idx in range(len(self.show_list)):
            self.init_idx-=1
            self.show_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.canvas.draw()
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
        
         else:
            
             print "invalid RR number"
         return 0
    def skipten(self):
        
        clf()
        if self.init_idx<len(self.show_list)-10:
            self.init_idx+=10
            self.show_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
            self.canvas.draw() 
        else:
           
            print "can't go that high"
                   
            
        return 0
    def print_inits(self):
        
        if self.init_idx in range(len(self.RR_list)):
            output = pandas.Series(self.RR_list[self.init_idx].initials)
            output.index = ['Pt','Ethoxy','Al','OH','Oads','Pt_ss', 'SOorH','CH3OHliq','O2liq']
            print output
        else:
            print "invalid RR number"
        return 0
    def remember(self,filename):
        import pickle
        print "Saving..."
        fh      = open(filename, 'wb') 
        pickler = pickle.Pickler(fh)
        
 
        pickler.dump(self.RR_list)
        fh.close()
        print "saved to", filename
        print len(self.RR_list), "runouts."
        
        return 0
    def save(self):
         
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*')]
        options['title'] = 'Save RRResults...'
        options['parent'] = self.top
     
        
        filename = tkFileDialog.asksaveasfilename(**options)
        
        athread = threading.Thread(target = self.remember, args = (filename,) )
        athread.daemon = True 
        athread.start()
        
        return 0
    def loadwindow(self):    
        import re
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*')]
        options['multiple'] = False
        options['title'] = 'Open RRResults...'
        options['parent'] = self.top
        
        filename = tkFileDialog.askopenfilename(**options)
        
        athread = threading.Thread(target = self.load, kwargs = {'filename':filename} )
        athread.daemon = True 
        athread.start()
        return 0

        
        
       
        
    def load(self, filename = 'RRresults.txt'):
        print "Loading from", filename , "..."
        
        
        fh = open(filename, 'rb')
# Creating the unpickler object.
        unpk = pickle.Unpickler(fh)
        
# Re-load the eggs object from our dumpfile.
        self.RR_list = unpk.load()
       
        fh.close()
        
        #self._reset_option_menu(*self.groups_name_list)
        print "loaded from", filename
        print len(self.RR_list), "runouts."
            
        
        self.queue.put((UPDATE_PROGRESS,"0/"+str(len(self.RR_list))))

#        for item in self.RR_list:
#            item.initials = item.conc[:,0]
        
        return 0
    
    def pause(self):
        if self.PauseFlag.is_set() == True:
            self.PauseFlag.clear()
            print "program Paused"
        else:
            self.PauseFlag.set()
            print "program unpaused"
        return 0
    def stop(self):
        print "Stopping program..."
        self.endflag = True
        return 0
    def start(self):
        
        self.endflag = False
        threading.Thread(target = self.control_thread.KinModelJelemensky, kwargs = {'clear':False}).start()
        return 0
    def updategroup(self, value):
    
        self.init_idx = 0
        self.var_curr_group.set(value)
        
       
        if self.var_curr_group.get() == 'all':
            self.show_list = list(self.RR_list)
            print "showing all groups"
            
        else:
            self.show_list = list()
            target_type = int(self.var_curr_group.get())
            for rr in self.RR_list:
                if rr._type == target_type:
                    
                    self.show_list.append(rr)
            print len(self.show_list), "schemes of this type."
        self.show_list[0].PlotRunOut()
        self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
        self.canvas.draw()
            
            
        return 0
        
def quitproc():
        global endall
        endall = 1     
        return 0
    
            
        

def CheckForInduction(conc_series, time_array = None, _plot = True):

    
    
    if time_array == None:
        time_array = arange(conc_series.size)
        dt = ndarray(conc_series.size)
        dt = 0.001
    else:
        #print respace_x(time_array,conc_series,linspace(0,time_array, conc_series.size))
        (time_array,conc_series) = respace_x(time_array,conc_series,linspace(0,time_array[-1], 1000))
        dt = time_array[-1]/1000
    conc_series = SG_Smooth(conc_series)    
    
    
    dAl_dt=  append(diff(conc_series,n=1)/dt,0)
  
    d2Al_dt2= append(diff(conc_series,n=2)/dt,[0,0])
    
   
    
    if _plot == True:
        
     
        plot(time_array[:],conc_series,'b.')
        plot(time_array[:-2],dAl_dt[:-2],'r.')
        plot(time_array[:-2],d2Al_dt2[:-2],'g.')
        legend(['0','1','2'])
    
    
    induction = (any(d2Al_dt2>1E-4) and any(d2Al_dt2<-1E-4) and any(dAl_dt>1E-3))
     
    
    return induction

def GoesPosToNeg(a):
    b = (diff(sign(a)) > 0).nonzero()[0] + 1 # local min
    c = (diff(sign(a)) < 0).nonzero()[0] + 1 # local max
  
   
    return any(c)
    
    
def _correlate(a1,a2):
    if a1.size>a2.size:
        a1 = a1[0:a2.size]
        
    elif a2.size>a1.size:
        a2 = a2[0:a1.size]
       
    else:
        pass
    return 2*sum(a1*a2)/(sum(a1**2)+sum(a2**2))



def go():
    
    global eVc
    eVc = 0
    a = array([  0,  # pt
                0.99,  # ethoxy
                0,    ###aldehyde
                0.0, ##OH
                0.0,  # oxide
                0,  #pt subsurface
                5,   #h so
                1.00000000e+00,  
                50E-6])
    a[Pt] = 1-sum(a[array([Ethoxy,OH,Oads,Al])])
    

    x = RateRunout(inits = a)
    #threading.Thread(target = x.RunOut, args = ('Jelemensky',), kwargs = {'time_limit':10,'_plot':True} ).start()
    x.RunOut('L-H with ethoxy switch',time_limit = 10000,_plot = True)
    
    
    return x

def r():
    x = linspace(0,2,1000)
    ya = (1-x)*exp(1*x)+exp(1*x**2)-1.02
    yr =(exp(x*1) )
    plot(x,ya,'r')
    plot(x,yr,'b')
    return 0
    
def extrapolate(x,y,xout,_plot = False):
    outy = ndarray((y.size,))
    a = array([],dtype = int)
    t =linspace(x[0],x[-1],10)
    for i in t:
       
        a = append(a,where(abs(x-i)==min(abs(x-i)))[0],axis = 0)
    
    y_fit = y[a] 
    
    try:
        r = polyfit(t,y_fit,3)
    except:
        return y_fit[-1]
    
    yout = sum(r*array([xout**3,xout**2,xout,1]))
    if _plot == True:
       
        plot(xout,yout,'s',color =plot(t,y_fit,'s')[-1].get_color())
    
    return yout
    
  




    
    
        