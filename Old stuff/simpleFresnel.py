# -*- coding: utf-8 -*-
"""
Created on Wed Oct 09 15:02:58 2013

@author: Chris

simpleFresnel is the program to calculate the fresnel factors for a simple interface of two materials.  
"""


import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from mpl_toolkits.mplot3d import Axes3D
from numpy import *
import numpy

def open_ri(filename, _plot = False, use_loadtxt_command = True):
    
    
        import os, csv
        if use_loadtxt_command == True:
            a = loadtxt(filename,
                          dtype = str,
                          delimiter = ",",
                          usecols = [0,1,2],
                          skiprows = 1,
                          unpack = True)
           
            freq = a[0].astype(numpy.float)
            
            x = ndarray(freq.shape, dtype = complex) 
            
            x.real = a[2].astype(numpy.float)
            x.imag = a[1].astype(numpy.float)
       
        
        if _plot == True:
                plot(freq, numpy.real(x))
                plot(freq, numpy.imag(x))
                
                title("index of refraction (real and complex)")
                show()

        return (freq,x)


def respace_x(array_xdata,array_ydata,values_to_lookup, _plot = False):
    
    
    return_array = array([])
    for value in values_to_lookup:
            idx = (abs(array_xdata-value)).argmin()
          
            if idx<2:
                p = array_ydata[idx]
            elif idx>values_to_lookup.size-2 :
                p = array_ydata[idx]
            else:
                d = polyfit(array_xdata[idx-2:idx+2],array_ydata[idx-2:idx+2],2)
                p = d[0]*value**2 + d[1]*value + d[2]

            
            return_array = append(return_array,p)
    if _plot ==True:
        plot(values_to_lookup,return_array, 'r-')
        plot(array_xdata,real(array_ydata),'bs')
        
    
        
    return (values_to_lookup,return_array)


###   NOTE: All angles for fresnel factors in radians.  

def rss(n1,t1,n2,n0 = None,mirabella = False,nearfield = False):
    
    
    if type(t1) is not ndarray:
        t1 = array([t1])
    
    cost2= (1/n2)*sqrt((n2**2-n1**2*sin(t1)**2),dtype = complex)
    r = (n1*cos(t1)-n2*cost2)/(n1*cos(t1)+n2*cost2)
 
    return r      

def rpp(n1,t1,n2):
    ##########  r and s are rpp calclulated two different ways, which are mathematically equivalent.... some issue here, since they do not agree. 
    
    if type(t1) is not ndarray:
        t1 = array([t1])
    
    cost2= (1/n2)*sqrt(n2**2-n1**2*sin(t1)**2,dtype = complex)
    
    r = (n2*cos(t1)-n1*cost2)/(n1*cost2+n2*cost2)
    
    e2= n2**2
    
    e2 = complex(abs(n2)**2, 2*n2.real*n2.imag)
    
    s = (cos(t1)- sqrt(1/e2 -sin(t1)**2/e2**2,dtype=complex))/(cos(t1)- sqrt(1/e2 + sin(t1)**2/e2**2,dtype = complex))
      
    plot(t1,r)
    plot(t1,s) 
    legend(['r','s'])
    return (r,s) 

def Lxx(n1,t1,n2,n0 = None,mirabella = False,nearfield = False):
    
    try:
        if type(t1) is not ndarray:
            t1 = array([t1])
        
        cost2= (1/n2)*sqrt((n2**2-n1**2*sin(t1)**2),dtype = complex)
        t = 2*n1*cost2/(n1*cost2+n2*cos(t1)) 
        if any(imag(t)!=0):
            print "TIR detected"
            if mirabella:
                
                  tmira = 2*sqrt(sin(t1)**2-(n2/n1)**2)*cos(t1)/(sqrt(1-(n2/n1)**2)*sqrt((1+(n2/n1)**2)*sin(t1)**2-(n2/n1)**2))## mirabella
                 
                  if n0 >=0:
                      
                  #### FOR THIN LAYER MODEL.   euqatoin from mirabella: INternal reflection spectroscopy theory and applicatoins for 
                      tmira *= sqrt((1+(n2/n0)**4)*sin(t1)**2- (n2/n1)**2) 
                      print tmira
                  t[imag(t)!=0] = tmira[imag(t)!=0]
            if nearfield:
                 tnf = (n2*cost2/n1/cos(t1))*abs(t)**2*sin(t1)*n1/n2
                 t[imag(t)!=0] = tnf[imag(t)!=0]
    except:
        print "error calculation Lxx", n1,t1,n2
    return t                                            
def Lyy (n1,t1,n2, mirabella = False,nearfield = False):
    try:
        if type(t1) is not ndarray:
            t1 = array([t1])
        cost2= (1/n2)*sqrt((n2**2-n1**2*sin(t1)**2),dtype = complex)
        t= 2*n1 * cos(t1)/(n1*cos(t1)+n2*cost2)
        if any(imag(t)!=0):
            if mirabella:
          
               tmira = 2*cos(t1)/sqrt(1-(n2/n1)**2)
               t[imag(t)!=0] = tmira[imag(t)!=0] 
            if nearfield:
                tnf = abs(t)**2
                t[imag(t)!=0] = tnf[imag(t)!=0]
    except:
        print "error calculation Lyy", n1,t1,n2   
    return t
def Lzz(n1,t1,n2,n0,mirabella = False,nearfield = False):
    try:
        if type(t1) is not ndarray:
            t1 = array([t1])
        cost2= (1/n2)*sqrt((n2**2-n1**2*sin(t1)**2),dtype = complex)
        t = 2*n2*cos(t1)*(n1/n0)**2/(n1*cost2 + n2*cos(t1))
#        if any(imag(t)!=0):
#            if mirabella:
#                tmira = 2*sin(t1)*cos(t1)/(sqrt(1-(n2/n1)**2)*sqrt((1+(n2/n1)**2)*sin(t1)**2-(n2/n1)**2)) ## mirabella
#                if n0 >=0:
#                  #### FOR THIN LAYER MODEL.   euqatoin from mirabella: INternal reflection spectroscopy theory and applicatoins for 
#                      tmira *= sqrt((1+(n2/n0)**4)*sin(t1)**2- (n2/n1)**2)                
#                t[imag(t)!=0] = tmira[imag(t)!=0]
#            
    except:
        print "error calculation Lzz", n1,t1,n2
    return t  
#IRdata = open_ri('C:/Users/Chris/Dropbox/Python Scripts/water.csv', _plot = False)
#(freq,n2) = respace_x(IRdata[0],IRdata[1],linspace(2800,3600,100))

def miratest():
    clf()
    t1 = linspace(0,1.57,100)
    n1 = 2.2
    n2 = 1.5
    #t = argmin(abs(n2[:,0]-1.33))
    
    c = Lxx(n1,t1,n2)
    d = Lxx(n1,t1,n2,mirabella = False)
    e = Lxx(n1,t1,n2,mirabella = False,nearfield = True)
    
    print c.shape
    plot(t1,abs(c))
    plot(t1,abs(d))
    plot(t1,abs(e))
    plot(t1,abs(Lyy(n1,t1,n2)))
    plot(t1,abs(Lzz(n1,t1,n2,n2)))
    legend(['mira','nomira','nearfield'])
    return 0
    
def FuncOfAngle():
    
    clf()
    t1 = linspace(0,1.57,100)
    n1 = 1.46
    n2 = 1.33
    #t = argmin(abs(n2[:,0]-1.33))
    
    c = Lxx(n1,t1,n2)
    d = Lyy(n1,t1,n2)
    e = Lzz(n1,t1,n2,1.33)
    print c.shape
    plot(degrees(t1),abs(c))
    plot(degrees(t1),abs(d))
    plot(degrees(t1),abs(e))
#    plot(t1,real(c),'r-',linewidth = 3)  #  givex Lxx as a funcitno of angle of incidence
#    plot(t1,imag(c),'r-.')
#    plot(t1,real(d),'bs') #Lyy
#    plot(t1,imag(d),'b-.')
#    plot(t1,real(e),'go')  #  givex Lxx as a funcitno of angle of incidence
#    plot(t1,imag(e),'g-.')  #  givex Lxx as a funcitno of angle of incidence
    ylabel('Local Field Factor')
    xlabel('Angle (degrees)')
    legend(['$L_{xx}$','$L_{yy}$','$L_{zz}$'], loc = 2)
    return 0
    
def FuncOfIndex():
    #from matplotlib.pyplot import xticks
    from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
    
    clf()
    n1 = 1.46
   
    angle_dict = {1:30,2:45,3:70}
    
    for i in range(1,4):
        
        Lx = array([])
        Ly = array([])
        Lz = array([])
        subplot(130+i)
        l = radians(angle_dict[i])
        n2_space = linspace(1.33,1.38,35)
        for n2 in n2_space:

           
            Lx = append(Lx,Lxx(n1,l,n2))
            Ly = append(Ly,Lyy(n1,l,n2))
            Lz = append(Lz,Lzz(n1,l,n2,n2))

        
        plot(n2_space,Lx,'s')
        plot(n2_space,Ly,'-')
        plot(n2_space,Lz,'o')
        
        at = AnchoredText(str(angle_dict[i])+"$^\circ$C", prop=dict(size=12), loc=2)
        gca().add_artist(at)
        if i == 1:
            ylabel('Local Field Factor',size = 20)
        xlabel('$n_2$',size = 20)
        legend(['$L_{xx}$','$L_{yy}$','$L_{z}$'], loc = 6)
        xticks([1.33,1.34,1.35,1.36,1.37,1.38])
        
        
           
        
    return 0

def _3DPlot():

    fig  = figure()
    ax1 = fig.add_subplot(311,projection = '3d')
    ax2 = fig.add_subplot(312,projection = '3d')
    ax3 = fig.add_subplot(313,projection = '3d')
    ax1.plot_surface(t1,freq,c)
    
    ax2.plot_surface(t1,freq,d)
    ax3.plot_surface(t1,freq,e)
    return 0
#ax.plot_wireframe(t1[0],n1[:,0],)
    
    
def TIR():
    clf()
    n2 = 1
    n1 = 1.46
    
    t1 = linspace(0,pi/2,100)
    
    plot(degrees(t1),abs(Lzz(n1,t1,n2,1.23))**2)
   
    xlabel('angle')
    ylabel('Efield_trans/Efield_inc (at d = lambda)')
    return 0
    
def platinum():
    clf()
    n2 = 1.33
    n1 = 1.46
    n0 = 2
    t1 = linspace(0,pi/2,100)
    
    plot(degrees(t1),abs(Lzz(n1,t1,n2,n0))**2*sin(t1)**2)
    plot(degrees(t1),abs(Lxx(n1,t1,n2))**2*cos(t1)**2)
    xlabel('angle')
    ylabel('Efield_trans/Efield_inc (at d = lambda)')
    legend(['z','x'])
    return 0 
    
def silver():
    j = complex(0,1)
    clf()
    n2 = complex(0.14,2.91)
    n1 = 1.00
   
    t1 = linspace(0,pi/2,100)
    
   
    

    plot(degrees(t1),abs(rss(n1,t1,n2))**2,label='ss')
    plot(degrees(t1),abs(rpp(n1,t1,n2,n2))**2,'s', label='pp')
    xlabel('angle')
    ylabel('')
    legend()
    return 0 