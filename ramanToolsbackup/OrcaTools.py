# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 12:06:45 2015

@author: chris
"""

import pdb
import numpy
from numpy import array,float64, pi,exp, transpose,sign
import scipy.optimize
import pandas
#from ramanTools.SPETools import File
from copy import deepcopy,copy
import scipy.optimize
import matplotlib.pyplot as plt
from collections import namedtuple
import inspect


def import_raman_spectrum(orca_output_file, normalize = False,color='k',labelpeaks = True):

    fileopen = open(orca_output_file,'rb')
    f=fileopen.readlines()
    fileopen.close()
    for l in f:
        if 'IR SPECTRUM' in l:
            start =  f.index(l)+5
    table=list()
    for z in f[start:]:
        i = z.split(' ')
        while '' in i: 
            i.remove('')
       
        if i[0][0].isdigit():
           
            table.append([float(i[1])-0.5,float(i[2])])
            if labelpeaks:   
                plt.gca().annotate(i[0], (float(i[1]), float(i[2])+0.2), color=color,fontsize = 8,horizontalalignment='center') 
        elif not i[0][0].isdigit():
            
	    break
    table = transpose(table)
    if normalize == True:
            table[1]/=max(table[1])
    return plt.vlines(table[0],0,table[1],linewidth = 2,color=color)
    
def import_TDDFT_spectrum(orca_output_file,axistoploton=None,broaden=False, normalize = False,color='k',labelpeaks = True):

    fileopen = open(orca_output_file,'rb')
    f=fileopen.readlines()
    fileopen.close()
    for l in f:
        if 'ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS' in l:
            start =  f.index(l)+5
    table=list()
    for z in f[start:]:
        i = z.split(' ')
        while '' in i: 
            i.remove('')
       
        if i[0][0].isdigit():
           
            table.append([float(i[2]),float(i[4])])
            if labelpeaks:   
                plt.gca().annotate(i[0], (float(i[2]), float(i[4])+0.2), color=color,fontsize = 8,horizontalalignment='center') 
        elif not i[0][0].isdigit():
            
	    break
    table = transpose(table)
    print table
    if normalize == True:
            table[1]/=max(table[1])
    if broaden:
        gamma=3
        freqs = table[0]
        amps = table[1]
        x = arange(freqs[-1]-10,freqs[0]+100,0.1)
        
        y = zeros(x.shape)
        print table
        for i in range(amps.size):
            print i
            y+=    (1/pi)*amps[i]*(0.5*gamma)/((x-freqs[i])**2+(0.5*gamma)**2)
        
        if axistoploton==None:
            axistoploton=gca()
        return axistoploton.plot(x,y)
        
    return plt.vlines(table[0],0,table[1],linewidth = 2,color=color)
    
def separateNWgeo(filename):

    fileopen = open(filename,'rb')
    f=fileopen.readlines()
    fileopen.close()
    namefile = 0
    indexlist = []
    
    for l in range(len(f)):
        if 'Geometry "geometry" -> "geometry"' in f[l]:
            indexlist.append(l)
    print indexlist
    for start in indexlist:
            
            start =  start+7#f.index(l)+7
            table=str()
            
            for z in f[start:]:
                
                i = z.split(' ')
                while '' in i: 
                    i.remove('')
               
                if i[0][0].isdigit():
                    lengthoflist = i[0]
                    table+=(str(i[1])+ ' ' + str(i[3]) + ' ' + str(i[4])+' '+ str(i[5]))
                elif not i[0][0].isdigit():
                    table = str(lengthoflist)+'\nnocomment\n'+table
                    with open('/home/chris/Desktop/geos/xyzfile'+str(namefile)+'.xyz', 'wb') as writefile:
                        writefile.write(table)
                        writefile.close()
                        namefile+=1
                    break
                
    indexlist = []            
    for l in range(len(f)):
        if 'Total DFT energy =' in f[l]:
            indexlist.append(l)
    energies=array([])
    for start in indexlist:

            z= f[start]
            #print z
                
            i = z.split(' ')
            while '' in i: 
                i.remove('')
                
            energies = append(energies, float(i[4]))
    plot(energies)
    ylabel('energy')
    xlabel('step')
          
    
    return 0
    
def makeaspectrum():
    a = loadtxt('/home/chris/Desktop/TDDFT_.csv', unpack=True,delimiter = ',')
    
    print a[0]
    x = arange(0.01,10,0.01)
    y=zeros(x.shape)
    gamma=0.1

    for i in range(a.shape[1]):
            print i
            y+=    (1/pi)*a[1,i]*(0.5*gamma)/((x-a[0,i])**2+(0.5*gamma)**2)
        
    
    return (x,y)
        

    