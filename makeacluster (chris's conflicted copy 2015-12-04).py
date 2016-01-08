# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:57:17 2015

@author: chris
"""
from numpy import radians
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import itertools
import numpy

def makeacluster(radius,charges = 0, distance =2,cadmium_term=False):

    
    #########cell vectors in angstroms
    a = array([4.16,0,0])
    b = 4.16*array([cos(radians(60)),sin(radians(60)),0])
    c = array([0,0,6.756])
    
    
        
        
    cellvectors = array([a,b,c])
    
    
    
    ##Atomic positions in fractional coordinates in cell
    ### For Wurtzite#####
    Cdcoord = array([[0,0,0],[0.33,0.333,0.5]])
    Scoord = array([[0,0,0.375],[0.3333,0.3333,0.875]])
    tetarray = array([[0,0,0.375],[-0.333,-0.333,-0.125],[0.6666,-0.3333,-0.125],[-0.3333,0.6666,-0.125]])
    Cdcoord= dot(Cdcoord,cellvectors)
    Scoord=dot(Scoord,cellvectors)
  

    Cdcoordlist1 = ndarray((0,3))
    Cdcoordlist2 = ndarray((0,3))
    Scoordlist1 = ndarray((0,3))
    Scoordlist2 = ndarray((0,3))
    OHcoordlist=ndarray((0,3))
    Hcoordlist=ndarray((0,3))
    
    numbertorepeat = int(radius/b[1])+2
    
    for p in itertools.product(range(-numbertorepeat,numbertorepeat+1),repeat=3):
        
        x= dot(array([p]),cellvectors)+Cdcoord[0]
        x2=dot(array([p]),cellvectors)+Cdcoord[1]
        y = dot(array([p]),cellvectors)+Scoord[0]
        y2 = dot(array([p]),cellvectors)+Scoord[1]
        
        Cdcoordlist1 = append(Cdcoordlist1,x,axis=0)
        Cdcoordlist2 = append(Cdcoordlist2,x2,axis=0)
        Scoordlist1 = append(Scoordlist1,y,axis=0)
        Scoordlist2 = append(Scoordlist2,y2,axis=0)
    
    
    
    tetcoord=array([[ -2.08208000e+00,   1.19968767e+00,  -8.44500000e-01],
                     [ -2.08000000e-03,  -2.40297801e+00 , -8.44500000e-01],
                     [  2.07792000e+00,   1.19968767e+00,  -8.44500000e-01],
                     [  0.00000000e+00,   0.00000000e+00,   2.53350000e+00]])#ndarray((0,3))

       
#    Cdtetcoord1=array( [[ -2.08020800e+00 ,  1.20076847e+00,  -8.44500000e-01],
#                         [ -2.08000000e-04,  -2.40189721e+00,  -8.44500000e-01],
#                         [  2.07979200e+00,   1.20076847e+00,  -8.44500000e-01],
#                         [  0.00000000e+00,   0.00000000e+00,   2.53350000e+00]])

    tetcoord2 = array( [[ -2.06544000e+00,  -1.19968767e+00,  -8.44500000e-01],
                             [  1.43520000e-02,   1.08079970e-03,   2.53350000e+00],
                             [  1.45600000e-02,   2.40297801e+00,  -8.44500000e-01],
                             [  2.09456000e+00,  -1.19968767e+00,  -8.44500000e-01]])
    Cdtetcoord1=tetcoord*array([[1,1,-1]])
    Cdtetcoord2=tetcoord2*array([[1,1,-1]])
    
    x= where(numpy.sum(Cdcoordlist1**2,axis=1)<radius**2)[0]
    Cdcoordlist1=Cdcoordlist1[x]
    
    x= where(numpy.sum(Cdcoordlist2**2,axis=1)<radius**2)[0]
    Cdcoordlist2=Cdcoordlist2[x]
   
    
    
    Scoordlist1=Scoordlist1[numpy.sum(Scoordlist1**2,axis=1)<radius**2]
    Scoordlist2=Scoordlist2[numpy.sum(Scoordlist2**2,axis=1)<radius**2]
    
   

    Cdcoordlist1[:]+=array([[radius,radius,radius]])
    Scoordlist1[:]+=array([[radius,radius,radius]])
    Cdcoordlist2[:]+=array([[radius,radius,radius]])
    Scoordlist2[:]+=array([[radius,radius,radius]])

    if cadmium_term:
        for i in Scoordlist1:
            
            bondlength=1.34  ## angstroms
            x= append(Cdcoordlist1,Cdcoordlist2,axis=0)[numpy.sum((append(Cdcoordlist1,Cdcoordlist2,axis=0)[:]-i)**2,axis=1)<9]-i
            if x.shape[0]==4:
                pass
            else:
                #print 'undercoordinated atom found'
                for s in Cdtetcoord1:
                    if not any(sum((x[:]-s)**2,axis=1)<0.5):
                       
                       Cdcoordlist= append(Cdcoordlist1,[i+s],axis=0)
                       
        for i in Scoordlist2:
            bondlength=1.34  ## angstroms
            x= append(Cdcoordlist1,Cdcoordlist2,axis=0)[numpy.sum((append(Cdcoordlist1,Cdcoordlist2,axis=0)[:]-i)**2,axis=1)<9]-i
            if x.shape[0]==4:
                pass
            else:
                #print 'undercoordinated atom found'
                for s in Cdtetcoord2:
                    if not any(sum((x[:]-s)**2,axis=1)<0.5):
                       
                       Cdcoordlist= append(Cdcoordlist2,[i+s],axis=0)

    
    
    for i in Cdcoordlist1:
        bondlength=0.4
        x= append(Scoordlist1,Scoordlist2,axis=0)[numpy.sum((append(Scoordlist1,Scoordlist2,axis=0)[:]-i)**2,axis=1)<9]-i
        
        if x.shape[0]==4:
            pass
        else:
            #print 'undercoordinated atom found'
            for s in tetcoord:
                if not any(sum((x[:]-s)**2,axis=1)<0.5):
                  
                   OHcoordlist= append(OHcoordlist,[i+s],axis=0)
                       
 

    for i in Cdcoordlist2:
        bondlength=1.34  ## angstroms
        x= append(Scoordlist1,Scoordlist2,axis=0)[numpy.sum((append(Scoordlist1,Scoordlist2,axis=0)[:]-i)**2,axis=1)<9]-i
        if x.shape[0]==4:
            pass
        else:
            #print 'undercoordinated atom found'
            for s in tetcoord2:
                if not any(sum((x[:]-s)**2,axis=1)<0.5):
                  
                   OHcoordlist= append(OHcoordlist,[i+s],axis=0)
    for i in Scoordlist1:
        
        bondlength=1.34  ## angstroms
        x= append(Cdcoordlist1,Cdcoordlist2,axis=0)[numpy.sum((append(Cdcoordlist1,Cdcoordlist2,axis=0)[:]-i)**2,axis=1)<9]-i
        if x.shape[0]==4:
            pass
        else:
            #print 'undercoordinated atom found'
            for s in Cdtetcoord1:
                if not any(sum((x[:]-s)**2,axis=1)<0.5):
                   
                   Hcoordlist= append(Hcoordlist,[i+s/sqrt(sum(s**2))*bondlength],axis=0)
                   
    for i in Scoordlist2:
        bondlength=1.34  ## angstroms
        x= append(Cdcoordlist1,Cdcoordlist2,axis=0)[numpy.sum((append(Cdcoordlist1,Cdcoordlist2,axis=0)[:]-i)**2,axis=1)<9]-i
        if x.shape[0]==4:
            pass
        else:
            #print 'undercoordinated atom found'
            for s in Cdtetcoord2:
                if not any(sum((x[:]-s)**2,axis=1)<0.5):
                   
                   Hcoordlist= append(Hcoordlist,[i+s/sqrt(sum(s**2))*bondlength],axis=0)

    listofcoordlists = [Cdcoordlist1,Cdcoordlist2,Scoordlist1,Scoordlist2,OHcoordlist,Hcoordlist]
    alllists = ndarray((0,3))
    
    print 'duplicate checke'
    for i in listofcoordlists:
        allists=append(alllists,i,axis=0)
        
        for x in range(i.shape[0]):
            
            if any(sum((Cdcoordlist1[:]-i[x])**2)<2):
                print 'repeat Cd', x,where(sum((Cdcoordlist1[:]-i[x])**2)<2)
            if any(sum((Cdcoordlist2[:]-i[x])**2)<2):
                print 'repeat Cd', x,where(sum((Cdcoordlist2[:]-i[x])**2)<2)
            if any(sum((Scoordlist1[:]-i[x])**2)<2):
                print 'repeat S', x,where(sum((Scoordlist1[:]-i[x])**2)<2)
            if any(sum((Scoordlist2[:]-i[x])**2)<2):
                print 'repeat S', x,where(sum((Scoordlist2[:]-i[x])**2)<2)
            if any(sum((Hcoordlist[:]-i[x])**2)<2):
                print 'repeat H', x,where(sum((Hcoordlist[:]-i[x])**2)<2)
            if any(sum((OHcoordlist[:]-i[x])**2)<2):
                print 'repeat OH', x,where(sum((OHcoordlist[:]-i[x])**2)<2)
    for i in range(alllists.shape[0]):
        if where(sum((alllists[:]-i)**2,axis = 1)<1)[0].size !=1:
            print where(sum((alllists[:]-i)**2,axis = 1)<1)[0]
    
    print '_____________________'
    chargecoordlist=pointsonsphere(charges,radius+distance)+array([[radius,radius,radius]])

        
    fig=figure()
    ax = fig.add_subplot(111, projection='3d')
        
            
    Axes3D.scatter(ax,Cdcoordlist1[:,0],Cdcoordlist1[:,1],Cdcoordlist1[:,2],c='b')
    Axes3D.scatter(ax,Cdcoordlist2[:,0],Cdcoordlist2[:,1],Cdcoordlist2[:,2],c='b')
    Axes3D.scatter(ax,Scoordlist1[:,0],Scoordlist1[:,1],Scoordlist1[:,2],c='r') 
    Axes3D.scatter(ax,Scoordlist2[:,0],Scoordlist2[:,1],Scoordlist2[:,2],c='r')    
    Axes3D.scatter(ax,OHcoordlist[:,0],OHcoordlist[:,1],OHcoordlist[:,2],c='y')
    Axes3D.scatter(ax,Hcoordlist[:,0],Hcoordlist[:,1],Hcoordlist[:,2],c='k')
    Axes3D.scatter(ax,chargecoordlist[:,0],chargecoordlist[:,1],chargecoordlist[:,2],c='k')
#    print Cdcoordlist
#    print OHcoordlist
    numcoreatoms = sum((x.shape[0] for x in [Cdcoordlist1,Cdcoordlist2,Scoordlist1,Scoordlist2]))#+OHcoordlist.shape[0]+Hcoordlist.shape[0])
    print 'number of core atoms', numcoreatoms
    numatoms= Cdcoordlist1.shape[0]*1+Cdcoordlist2.shape[0]+Scoordlist1.shape[0]*1+Scoordlist2.shape[0]*1+OHcoordlist.shape[0]*1+Hcoordlist.shape[0]*1
        
    print 'num atoms:', numatoms, 'total charge:', str(Cdcoordlist1.shape[0]*2+Cdcoordlist2.shape[0]*2+
                                                Scoordlist1.shape[0]*-2+Scoordlist2.shape[0]*-2+
                                                OHcoordlist.shape[0]*-1+
                                                Hcoordlist.shape[0]*1)
        
    with open('/home/chris/Desktop/CdSParticle.xyz','wb') as f:
        f.write(str(numatoms)+'\n')
        f.write('total charge: '+ str(Cdcoordlist1.shape[0]*2
                                +Cdcoordlist2.shape[0]*2
                                +Scoordlist1.shape[0]*-2
                                +Scoordlist2.shape[0]*-2
                                +OHcoordlist.shape[0]*-1
                                +Hcoordlist.shape[0]*1)+'\n')
        
        
        for i in append(Cdcoordlist1,Cdcoordlist2,axis=0):
            f.write('Cd '+str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')
        for i in append(Scoordlist1,Scoordlist2,axis=0):
            f.write('S '+str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')
        for i in OHcoordlist:
            f.write('F '+str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')
        for i in Hcoordlist:
            f.write('H '+str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')
        for i in chargecoordlist:
            f.write('Q '+str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')
        f.close()
    return None
    
def pointsonsphere(n,rad):
    if n ==0:
        return ndarray((0,3))
    
 
    golden_angle = numpy.pi * (3 - numpy.sqrt(5))
    theta = golden_angle * numpy.arange(n)
    z = numpy.linspace(1 - 1.0 / n, 1.0 / n - 1, n)
    radius = numpy.sqrt(1 - z * z)*rad
     
    points = numpy.zeros((n, 3))
    points[:,0] = radius * numpy.cos(theta)
    points[:,1] = radius * numpy.sin(theta)
    points[:,2] = z
    fig=figure()
    ax = fig.add_subplot(111, projection='3d')
        
            
   
    
    return points
    
def perm(n, seq):
    coordlist = ndarray((0,3))
    for p in itertools.product(seq, repeat=n):
        coordlist = append(coordlist,array([p]),axis=0)
    return coordlist
    
def rotate(vector, aroundvector, bydegrees):
    bydegrees = radians(bydegrees)
    apar = dot(vector,aroundvector)*aroundvector/sum(aroundvector**2)**2
    
    aper = vector - apar
    
    w = numpy.cross(aroundvector,aper)
    
    aperrot = sqrt(sum(aper**2))*(cos(bydegrees)*aper/sqrt(sum(aper**2))+sin(bydegrees)*w/sqrt(sum(w**2)))
    return aperrot+apar
    






