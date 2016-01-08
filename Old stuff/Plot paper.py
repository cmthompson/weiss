# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 12:03:49 2013

@author: Chris

"""


#plt.title(r'$\alpha > \beta$')
#subscript:  r'$\alpha_i > \beta_i$'


from Tkinter import *

import Tkinter
import tkFileDialog, tkSimpleDialog
import tkMessageBox
import os
from scipy import optimize
from SFG_Analysis import SG_Smooth, OpenSFG, DisplaySpectrum


os.chdir('C:/Users/Chris/Dropbox/Paper')



j = complex(0,1)




    
def plot1():
    (x,y) = OpenSFG('C:/Users/Chris/My Documents/Data/130716/13071602and03.csv',channel = 'AvgSFG')
    y[:] = SG_Smooth(y[:])
    reference =  OpenSFG('C:/Users/Chris/My Documents/Data/130716/13071601.csv',channel = 'AvgIR')[1][0:61]
    reference[:] = SG_Smooth(reference[:],width = 40, order = 3)
    #y[:]/=reference[:]
    fit_x = arange(2850,3030,5)
    w_name = ('A1','A2','A3','A4','w1','w2','w3','w4','G1','G2','G3','G4','m','b')
    def function(x,A1,A2,A3,A4,w1,w2,w3,w4,G1,G2,G3,G4,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4))**2
    guess = [1.103554037,
              3.122120205,
              3.072474181,
              -2.145426852,
              2863.055036,
              2921.060524,
              2955.495269,
              2981.282328,
              17.17213039,
              19.82232459,
              15.09600975,
              13.69904151,
              -0.220743836,
              1.312173785]      
    
    
    plot(x,y,'bs')
    plot(fit_x,function(fit_x,guess[0],guess[1],guess[2],guess[3],guess[4],guess[5],guess[6],guess[7],guess[8],guess[9],guess[10],guess[11],guess[12],guess[13]),'r')
    axvline(2863)
    axvline(2921)
    axvline(2955)
    axvline(2981)
    annotate('$CH_{3(s)}$',(2863,0.5),xytext = (2825,0.55),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$CH$',(2921,0.6),xytext = (2895,0.65),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$CH_{3 (fr)}$',(2955,0.75),xytext = (2955,0.85),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$CH_{3 (a)}$',(2981,0.67),xytext = (2985,0.7),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    xlabel('IR Wavenumber cm-1')
    ylabel('SFG Intensity (a.u.)')
    

    
    
    
    
    return 0 
    
    
def plot2():
    
    name_list = [u'C:/Users/Chris/My Documents/Data/130716/13071602and03.csv',  #100%
                 u'C:/Users/Chris/My Documents/Data/130715/13071510.csv', # 25%
                 u'C:/Users/Chris/My Documents/Data/130715/13071511.csv', #0%
                 u'C:/Users/Chris/My Documents/Data/130710/AverageAll.csv']  #15% 
    reference_list =   [u'C:/Users/Chris/My Documents/Data/130716/13071601.csv',
                 u'C:/Users/Chris/My Documents/Data/130715/13071505.csv',
                 u'C:/Users/Chris/My Documents/Data/130715/13071505.csv',
                 u'C:/Users/Chris/My Documents/Data/130710/13071001.csv'] 
    offset_list = [0.55,-0.2,-0.6,0]
           
    legend_list = ('100%','25%','0%', '15%') 
    for i in range(len(name_list)):
        reference =  OpenSFG(reference_list[i],channel = 'AvgIR')[1]
        reference[:] = SG_Smooth(reference[:],width = 75,order =3)
        (x,y) =  OpenSFG(name_list[i],channel = 'AvgSFG') 
        y[:] = SG_Smooth(y)
        y[:]/=reference[0:y.size]
        y[:]+=offset_list[i]
        plot(x,y)
        
    legend(legend_list)
    xlim(2800,3100)
    xlabel('IR Wavenumber cm-1')
    ylabel('SFG Intensity (a.u.)')
    
    
    return 0
    
def plot3():
    annotate('a',(2815,0.5),xytext = (0.05,0.9),textcoords = 'axes fraction',size = 30)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
   
    subplot(122)
    plot3b()
    annotate('b',(2850,0.45),xytext = (0.05,0.9),textcoords = 'axes fraction',size = 30)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    return 0


def plot3a():
    figure(figsize = (8,8))
    
    rc('xtick', labelsize =16)
    rc('ytick', labelsize =16)    
    
    (x,y) = OpenSFG('C:/Users/Chris/My Documents/Data/130716/13071602and03.csv',channel = 'AvgSFG')
    y[:] = SG_Smooth(y[:])
    reference =  OpenSFG('C:/Users/Chris/My Documents/Data/130716/13071601.csv',channel = 'AvgIR')[1][0:61]
    reference[:] = SG_Smooth(reference[:],width = 41, order = 3)
    #y[:]/=reference[:]
    fit_x = arange(2850,3030,5)
    w_name = ('A1','A2','A3','A4','w1','w2','w3','w4','G1','G2','G3','G4','m','b')
    def function(x,A1,A2,A3,A4,w1,w2,w3,w4,G1,G2,G3,G4,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4))**2
    guess = [1.103554037,
              3.122120205,
              3.072474181,
              -2.145426852,
              2863.055036,
              2921.060524,
              2955.495269,
              2981.282328,
              17.17213039,
              19.82232459,
              15.09600975,
              13.69904151,
              -0.220743836,
              1.312173785]      
    
    
    plot(x,y,'bs')
    plot(fit_x,function(fit_x,guess[0],guess[1],guess[2],guess[3],guess[4],guess[5],guess[6],guess[7],guess[8],guess[9],guess[10],guess[11],guess[12],guess[13]),'r')
    axvline(2880)
    axvline(2905)
    axvline(2935)
    axvline(2965)
    annotate('$CH_{3(s)}$',(2863,0.5),xytext = (2870,0.55),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$CH$',(2921,0.6),xytext = (2900,0.65),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$CH_{3 (fr)}$',(2955,0.75),xytext = (2930,0.83),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$CH_{3 (a)}$',(2981,0.67),xytext = (2960,0.85),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    xlabel('IR Wavenumber (cm$^{-1}$)', size =20)
    ylabel('SFG Intensity (a.u.)', size =20)
    

   
    
    return 0 #r'$\alpha_i > \beta_i$'
def plot3b():
    figure(figsize = (10,8))
    rc('xtick',labelsize = 16)
    rc('ytick',labelsize = 16)
    
    name_list = [u'C:/Users/Chris/My Documents/Data/130703/13070302.csv',  #D2O
                 u'C:/Users/Chris/My Documents/Data/130703/13070306and07.csv']  #H2O
    reference_list =   [u'C:/Users/Chris/My Documents/Data/130703/13070301.csv',
                 u'C:/Users/Chris/My Documents/Data/130703/13070303.csv'] 
    offset_list = [0,0]
           
   
    for i in range(len(name_list)):
        reference =  OpenSFG(reference_list[i],channel = 'AvgIR')[1]
        reference[:] = SG_Smooth(reference[:],width = 75,order =3)
        (x,y) =  OpenSFG(name_list[i],channel = 'AvgSFG') 
        y[:] = SG_Smooth(y, width = 21)
        if i == 1:
            
            y[:]-=0.15
            
        y[:]/=reference[0:y.size]
        #y[:]/=0.34823841726942772 #normalization constant is the same for both spectra but necessary for comparison to figure 5
        y[:]+=offset_list[i]
        plot(x,y,linewidth = 5)
        
    legend_list = ('$D_2O$','$H_2O$')     
    legend(legend_list, fontsize = 20)
    
    xticks(arange(2800,3700,100))
    xlim(2800,3600)
    ylim(-0.2,1.5)
    xlabel('IR Wavenumber (cm$^{-1}$)', size = 20)
    ylabel('SFG Intensity (a.u.)',size = 20)
    ylim(0,0.5)
    annotate('$OH_{ice-like}$',(3150,0.45),xytext = (3000,0.37),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    annotate('$OH_{liquid-like}$',(3450,0.4),xytext = (3250,0.37),size = 20)#,arrowprops=dict(facecolor='black', shrink=0.05,width = 1))
    axvline(3150)
    axvline(3450) 
    
    
    
   
    
    return 0 #r'$\alpha_i > \beta_i$'    
def plot4():
    rc('xtick', labelsize=20) 
    rc('ytick', labelsize=20) 
    name_list = [ u'C:/Users/Chris/My Documents/Data/130703/13070306and07.csv',  #0%
                        u'C:/Users/Chris/My Documents/Data/130627/13062703.csv',  #5%
                         u'C:/Users/Chris/My Documents/Data/130627/13062704.csv',  #15%
                         u'C:/Users/Chris/My Documents/Data/130627/13062705and06.csv',#25%
                         u'C:/Users/Chris/My Documents/Data/130627/13062708and09.csv',#35%
                         u'C:/Users/Chris/My Documents/Data/130627/13062710.csv',#50%
                         u'C:/Users/Chris/My Documents/Data/130628/13062804.csv',#65%
                         u'C:/Users/Chris/My Documents/Data/130628/13062805.csv',#75%
                         u'C:/Users/Chris/My Documents/Data/130702/13070205.csv'] #100%
                         
    reference_list =   [u'C:/Users/Chris/My Documents/Data/130703/13070303.csv',
                u'C:/Users/Chris/My Documents/Data/130627/13062707.csv',
                u'C:/Users/Chris/My Documents/Data/130627/13062707.csv',
                u'C:/Users/Chris/My Documents/Data/130627/13062707.csv',
                u'C:/Users/Chris/My Documents/Data/130627/13062707.csv',
                u'C:/Users/Chris/My Documents/Data/130628/13062801.csv',
                u'C:/Users/Chris/My Documents/Data/130628/13062801.csv',
                u'C:/Users/Chris/My Documents/Data/130628/13062801.csv',
                u'C:/Users/Chris/My Documents/Data/130702/13070202.csv']
    norm_list = [0.34823841726942772 , # for 0703
                0.53715214600288186,# for 06/27
                 0.53715214600288186,
                 0.53715214600288186,
                 0.53715214600288186,
                 0.38087085024317607,# for 06/28
                 0.38087085024317607,
                 0.38087085024317607
                 ,0.16558730116407236] # for 0702
                 
    offset_list = [-0.5,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1]
    color_list = ('r','c','y','g','b','m','k','r','c','y') 
       
    #legend_list = ('0%','5%','15%','25%','35%','50%','65%','75%','100%') 
    legend_list = ('0','0.02','0.05','0.09','0.14','0.23','0.35','0.47','1')
    w1= 2859#2863
    w2= 2916#2921
    w3= 2950#2955
    
    w4= 2976#2981
    G1=17
    G2=20
    G3=15
    G4=14
    
    def function(x,A1,A2,A3,A4,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4))**2
    def function_H2O(x,A1,A2,w1,w2,G1,G2,m,b): return abs(abs(m*x/1000+b) + A1/((x-w1)+j*G1) + A2/((x-w2)+j*G2))**2
    figure(figsize = (7,10) )      
    result_array  = ndarray((0,6))
    result_array_H2O = ndarray((0,8))
    for i in range(9):
        
        reference =  OpenSFG(reference_list[i],channel = 'AvgIR')[1]
        reference[:] = SG_Smooth(reference[:],width = 101,order =3, plot_val = False)
        (x,y) =  OpenSFG(name_list[i],channel = 'AvgSFG')
       
        y[:51] = SG_Smooth(y[:51],width=9, plot_val = False)
        y[50:] = SG_Smooth(y[50:], width = 17)# smooth figure savitzgy-golay
        y[:]/=reference[0:y.size] # divide by IR intensity
        y[:]/=norm_list[i]  #divide by sverage signal of D2O spectrum
        y[:]+=offset_list[i]  #add offset
        
       
        
        guess = [1,1,1,1,1,1] 
        x2 = x[10:41] # fit from 2850 to 3000 cm-1 for IPA
        y2 = y[10:41]
        result = optimize.curve_fit(function,x2,y2,guess)
        
        x3 = x[50:151] # fit from 3000 to 3600 for water
        y3 = y[50:151]
        plot(x2,function(x2,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5]),color_list[i],linewidth =4)
        if i<6:
            result_H2O = optimize.curve_fit(function_H2O,x3,y3,[-10,10,3150,3430,50,50,0.1,0.1])
            plot(x3,function_H2O(x3,result_H2O[0][0],result_H2O[0][1],result_H2O[0][2],result_H2O[0][3],result_H2O[0][4],result_H2O[0][5],result_H2O[0][6],result_H2O[0][7]),color_list[i],linewidth =4)
            result_array_H2O = append(result_array_H2O,array([result_H2O[0]]),axis = 0)
        
        #if i==0:
           # y3 = function_H2O(x3,-36.22376521,21.29423771,3136.975513,3476.782658,77.97268811,67.86901679,-0.104459889,-1.151515356)
            
        
        #elif i==1:
            #y3 = function_H2O(x3,-25.31784695,5.180934043,3108.867602,3455.612769,131.8565447,63.33178542,-0.015918855,-0.486201069)

       #elif i==2:
             #y3 =function_H2O(x3,-4.568841514,3.865655113,3124.711339,3465.091993,54.87312064,51.61844185,0.057203456,-0.760867995)

    
        #elif i == 3:
             #y3 =function_H2O(x3,-5.84448918,0.823920061,3129.902346,3436.019638,51.9399975,16.00292659,0.056675103,-0.787918739)

    
       # elif i ==4:
            # y3 =function_H2O(x3,-2.970988747,	0.408897952,3134.367035,3427.876978,40.65950836,11.32752222,0.135930715,-1.111467587)
             
        #elif i == 5:
             #y3 = array([])
             #y_fit =function_H2O(x_fit, 1.355348504 , 1.51379438, 1.559280317,-1.097137258, -0.220032648, 1.31)#1.373172743)   
             #pass
        #elif i == 6:
             #y3 = array([])#y_fit =function_H2O(x_fit,1.302183006,	2.39825097,	1.325861562,	-0.260937415,	-0.605493556,	2.483331291)
    
        
       # elif i==7: 
             #y3 = array([])#y_fit =function_H2O(x_fit,-0.049702526,	2.478475264,	1.821007869,	-0.777435133,	-0.737636108,	2.965568993)
        #elif i==8: 
             #y3 = array([])#y_fit =function_H2O(x_fit,-1.285316086,	1.071303025,	0.927914076,	-0.588546652,	0.401797317,	-0.572372568)
        
        
       
        
        
        
        result_array = append(result_array,array([result[0]]),axis = 0)
        
        
       
        plot(x,y,color_list[i]+'s',ms = 2)
        
    print result_array
    print result_array_H2O
     ###Superimpose fits
    
    
   
   
    
    annotate(legend_list[0],(3615,0.25), color = color_list[0], size = 20)   
    annotate(legend_list[1],(3615,0.45), color = color_list[1],size = 20)   
    annotate(legend_list[2],(3615,0.65), color = color_list[2], size = 20)   
    annotate(legend_list[3],(3615,0.85), color = color_list[3], size = 20)   
    annotate(legend_list[4],(3615,1.05), color = color_list[4], size = 20)   
    annotate(legend_list[5],(3615,1.25), color = color_list[5], size = 20)   
    annotate(legend_list[6],(3615,1.45), color = color_list[6], size = 20)   
    annotate(legend_list[7],(3615,1.65), color = color_list[7], size = 20) 
    annotate(legend_list[8],(3615,1.85), color = color_list[8], size = 20) 
    annotate('$x_{IPA}$',(3580,2.2), color = 'k', size = 30) 
        
    #legend(legend_list, loc = 'upper center')#,bbox_to_anchor=(0, 0, 1, 1), bbox_transform=gcf().transFigure)
    xlim(2800,3750)
    ylim(-0.2,4.0)
    xlabel('IR Wavenumber (cm$^{-1}$)',size = 20)
    ylabel('SFG Intensity (a.u.)',size = 20)
    
    
    return 0 
    
def plot5():
    rc('xticks', size = 20)
    rc('yticks',size = 20)
    figure(figsize = (7,10))
    x_IPA = array([0,
                    0.015050167,
                    0.048736462,
                    0.088235294,
                    0.135193133,
                    0.225,
                    0.350299401,
                    0.465517241,
                    1
                    ])
    A1_IPA = array([0.047297109,
                    -0.143025279,
                    -0.074895293,
                    0.624672435,
                    0.369673593,
                    1.079470605,
                    1.302183006,
                    -0.049702526,
                    -0.122363778
                    ])
                    
    A2_IPA = array([-0.020950403,
                    0.05661484,
                    -0.168033639,
                    0.566215325,
                    0.849798598,
                    1.689967469,
                    2.39825097,
                    2.478475264,
                    2.054756425,
                    ])
                    
    A3_IPA = array([-0.667742323,
                    0.44554716,
                    0.14023071,
                    0.35655671,
                    0.736610231,
                    1.53489196,
                    1.325861562,
                    1.821007869,
                    1.978216743
                    ])
    A4_IPA = array([-0.514026588,
                    -0.10197774,
                    -0.798580157,
                    -0.689524951,
                    -0.511129019,
                    -0.629020004,
                    -0.260937415,
                    -0.777435133,
                    -1.370506262
                    ])
                    
    x_H2O = x_IPA
    A1_H2O = array([-36.22376521,
                    -25.31784695,
                    -8.624633315,
                    -5.84448918,
                    -3.338038686,
                    -0.979848231,
                    0,
                    0,
                    0])
                    
    A2_H2O =array([21.29423771,
                    5.180934043,
                    6.698567817,
                    0.823920061,
                    0.970508557,
                    0,#-8.887221378,
                    0,
                    0,
                    0])
                    
    subplot(211)
    plot(x_IPA,(A1_IPA), 'bs-', label = 'A1')
    plot(x_IPA,(A2_IPA),'rs-', label = 'A2')
    plot(x_IPA,(A3_IPA),'ms-', label = 'A3')
    plot(x_IPA,(A4_IPA),'ks-', label = 'A4')
    ylim(-1.5,3)
    annotate('$\omega_0 = CH_{3(s)}$', (0.7,0.2), color = 'b', size = 20)
    annotate('$\omega_0 = CH$', (0.7,2.5), color = 'r', size = 20)
    annotate('$\omega_0 = CH_{3 (fr)}$', (0.7,1.2), color = 'm', size = 20)
    annotate('$\omega_0 = CH_{3 (a)}$', (0.7,-0.7), color = 'k', size = 20)
    xlabel('$x_{2-propanol}$', size = 20)
    ylabel('$A_q (a.u.)$',size = 20)
    axhline(0, color = 'k')
    annotate('$2-prop$',(0.05,2), size = 20)
    
    
    subplot(212)
    plot(x_H2O,(A1_H2O), 'bs-',label = 'A1')
    plot(x_H2O,(A2_H2O),'rs-', label = 'A2')
    annotate('$\omega_0 = OH_{ice-like}$', (0.3,15), color = 'b', size = 20)
    annotate('$\omega_0 = OH_{liquid-like}$', (0.3,5), color = 'r', size = 20)
    xlabel('$x_{2-propanol}$', size = 20)
    ylabel('$A_q (a.u.)$',size = 20)
    xlim(0,1)
    ylim(-35,45)
    axhline(0, color = 'k')
    annotate('$H_2O$',(0.05,15), size = 20)
    return 0
    
def plot5bigtext():
    figure(figsize = (8,10))
    rc('xtick', labelsize = 20)
    rc('ytick',labelsize = 20)
    
    x_IPA = array([0,
                    0.015050167,
                    0.048736462,
                    0.088235294,
                    0.135193133,
                    0.225,
                    0.350299401,
                    0.465517241,
                    1
                    ])
    A1_IPA = array([0.047297109,
                    -0.143025279,
                    -0.074895293,
                    0.624672435,
                    0.369673593,
                    1.079470605,
                    1.302183006,
                    -0.049702526,
                    -0.122363778
                    ])
                    
    A2_IPA = array([-0.020950403,
                    0.05661484,
                    -0.168033639,
                    0.566215325,
                    0.849798598,
                    1.689967469,
                    2.39825097,
                    2.478475264,
                    2.054756425,
                    ])
                    
    A3_IPA = array([0,#-0.667742323,
                    0.44554716,
                    0.14023071,
                    0.35655671,
                    0.736610231,
                    1.53489196,
                    1.325861562,
                    1.821007869,
                    1.978216743
                    ])
    A4_IPA = array([-0.514026588,
                    -0.10197774,
                    -0.798580157,
                    -0.689524951,
                    -0.511129019,
                    -0.629020004,
                    -0.260937415,
                    -0.777435133,
                    -1.370506262
                    ])
                    
    x_H2O = x_IPA
    A1_H2O = array([-36.22376521,
                    -25.31784695,
                    -8.624633315,
                    -5.84448918,
                    -3.338038686,
                    -0.979848231,
                    0,
                    0,
                    0])
                    
    A2_H2O =array([21.29423771,
                    5.180934043,
                    6.698567817,
                    0.823920061,
                    0.970508557,
                    0,#-8.887221378,
                    0,
                    0,
                    0])
                    
    ax1 = subplot(211)
    
    #tick_params(axis ='both', which = 'major',labelsize=10)
    plot(x_IPA,(A1_IPA), 'bs-', label = 'A1')
    plot(x_IPA,(A2_IPA),'rs-', label = 'A2')
    plot(x_IPA,(A3_IPA),'ms-', label = 'A3')
    plot(x_IPA,(-A4_IPA),'ks-', label = 'A4')
    ylim(-0.25,4)
    annotate('$\omega_0 = CH_{3(s)}$', (0.7,0.2), color = 'b', size = 25)
    annotate('$\omega_0 = CH$', (0.7,2.5), color = 'r', size = 25)
    annotate('$\omega_0 = CH_{3 (fr)}$', (0.7,1.5), color = 'm', size = 25)
    annotate('$\omega_0 = CH_{3 (a)}$', (0.7,0.7), color = 'k', size = 25)
    #xlabel('$x_{2-propanol}$', size = 30)
    ylabel('$A_q (a.u.)$',size = 25)
    
    
    rc('ytick', labelsize = 20)
    axhline(0, color = 'k')
    
    annotate('$IPA$',(0.02,2), size = 20)
    #ax1.yaxis.set_label_coords(-0.1,0.5)
  
    
    
    ax2 = subplot(212)
    plot(x_H2O,(-A1_H2O), 'bs-',label = 'A1')
    plot(x_H2O,(A2_H2O),'rs-', label = 'A2')
    annotate('$\omega_0 = OH_{ice-like}$', (0.3,15), color = 'b', size = 25)
    annotate('$\omega_0 = OH_{liquid-like}$', (0.3,5), color = 'r', size = 25)
    xlabel('$x_{IPA}$', size = 30)
    ylabel('$A_q (a.u.)$',size = 25)
   
    ylim(-5,40)
    xlim(0,1)
    
    axhline(0, color = 'k')
    

    annotate('$H_2O$',(0.05,15), size = 30)
    #subplots_adjust(left = 0.1)    
    return 0  

   
                 
                 
                    