# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 12:03:49 2013

@author: Chris

ThinFilmFresnel is used to calculate the local field factors at the interfaces of a thin film interface.
"""






import math
import matplotlib.pyplot as py
import numpy
from numpy import *
import os
from simpleFresnel import open_ri, respace_x

SFG = 0
VIS = 1
IR  = 2
j = complex(0,1)






def p(ydata, component = VIS):
    global freq
    plot(freq,ydata[component])
    
    return 0


def s(coeff, exponent):  ### returns the square modulus of (1 + coeff* exp(j*exponent))

    

    
    a=real(coeff)
    b = imag(coeff)
    c = real(exponent)
    d = imag(exponent)
    ret_val = 1+ abs(coeff)**2*exp(-2*d) + 2*a* exp(-d)*cos(c) - 2 * b* exp(-d)* sin(c)
    
    return ret_val

def test_s():
    j = numpy.complex(0,1)
    

    a = numpy.random.random_integers(10,size =  (10,))
    b = numpy.random.random_integers(10,size = (10,))

    c = a + j*b
    

    a = numpy.random.random_integers(10,size = (10))
    b = numpy.random.random_integers(10,size =(10))

    d = a + j*b
    print c
    print d

    print abs(1 + c*exp(j*b))**2
    print s(c,b)

    return 0

    
    


class System:
        

        def __init__(self,material1, material2, material3, d=5, gamma = 22):
            self.material1 = material1
            self.material2 = material2
            self.material3 = material3
            self.d = d
            self.freq = numpy.arange(2600,3805,25)
            self.n_3 = numpy.ndarray([3,self.freq.size],dtype = complex)     # complex index material 3 (liquid)
            self.n_2= numpy.ndarray(self.n_3.shape,dtype = complex)      # complex index material 2 (film)
            self.n_1 = numpy.ndarray(self.n_3.shape,dtype = complex)  # complex index material 1 (prism)
            self.l = numpy.ndarray(self.n_3.shape, dtype = float)  #wavelength in nm
            self.theta_1 = numpy.ndarray(self.n_3.shape, dtype = float)

            
            os.chdir('C:/Users/Chris/Dropbox/Python Scripts')
            SFG_dict = {'water':1.337,
                   'd2o':1.337,
                   'methanol': 1.38,
                   'air': 1,
                   'gold':0.000623*self.freq-2.3846+ j* 3.15,
                   'platinum':numpy.complex(1.879,3.222),
                   'sapphire':1.77,
                   'hydrocarbon':1.5}
            VIS_dict = {'water':1.33,
                   'd2o':1.33,
                   'methanol': 1.38,
                   'air': 1,
                   'gold':numpy.complex(0.188,5.39),
                   'platinum':numpy.complex(2.078,3.629),
                   'sapphire':1.76,
                   'hydrocarbon':1.5}
                   
            IR_dict =  {'water':'water.csv',
                       'd2o':'d2o.csv',
                       'methanol': 'CH3OH_ri.csv',
                       'air': 1,
                       'gold':'gold_IR_palik.csv',
                       'platinum':'platinum_IR_palik.csv',
                       'sapphire':1.709,
                       'hydrocarbon':1.5}
                       
            
            self.n_1[SFG] = SFG_dict[material1]
            self.n_1[VIS] = VIS_dict[material1]
            
           
            if type(IR_dict[material1]) == str:
                IRdata = open_ri(IR_dict[material1],_plot = False)
                (self.freq,self.n_1[IR]) = respace_x(IRdata[0],IRdata[1],self.freq,_plot =False)
              
            else:
                self.n_1[IR] = IR_dict[material1]
                
            self.n_2[SFG] = SFG_dict[material2]
            self.n_2[VIS] = VIS_dict[material2]
            
            if type(IR_dict[material2]) == str:
                IRdata = open_ri(IR_dict[material2],_plot = False)
                (self.freq,self.n_2[IR]) = respace_x(IRdata[0],IRdata[1],self.freq,_plot =False)
              
            else:
                self.n_1[IR] = IR_dict[material1]
        ###################    
            self.n_3[SFG] = SFG_dict[material3]
            self.n_3[VIS] = VIS_dict[material3]
            if type(IR_dict[material3]) == str:
                IRdata = open_ri(IR_dict[material3],_plot = False)
                (self.freq,self.n_3[IR]) = respace_x(IRdata[0],IRdata[1],self.freq,_plot =False)
              
            else:
                self.n_3[IR] = IR_dict[material1]
                (self.freq,self.n_3[IR]) = respace_x(IRdata[0],IRdata[1],self.freq,_plot =False)
                   
            
          
           


            self.l = numpy.ndarray(self.n_3.shape, dtype = float)
            self.l[IR] = 10**7/self.freq
            self.l[VIS] = 532
            self.l[SFG] = 10**7/(18797+self.freq)
            

            
            self.theta_1[IR] = numpy.radians(calc_from_gamma(gamma))
            self.theta_1[VIS] = numpy.radians(calc_from_gamma(gamma))
            self.theta_1[SFG] = numpy.arctan((18797*sin(self.theta_1[VIS]) + self.freq*numpy.sin(self.theta_1[IR])) / (18797*numpy.cos(self.theta_1[VIS]) + self.freq*cos(self.theta_1[IR]))/(18797+self.freq))
            
            self.indices = [self.n_1, self.n_2, self.n_3]


            theta_generate(self, plot = False, useapproximations = False)
            
            calc_fresnel(self,d = self.d, _plot = False)
            
            

            
            return None



def calc_from_gamma(gamma, prism_base_angle = 60, n_air = 1, n_2 = 1.709):
    gamma = numpy.degrees(numpy.arcsin(n_air*numpy.sin(numpy.radians(gamma-prism_base_angle))/n_2))+prism_base_angle
    
    return gamma

   
    



def fit_indices(x_range,x_data, y_data,plot = False):
        fit = numpy.polyfit(x_data,numpy.real(y_data),5)
        fit_i = numpy.polyfit(x_data,numpy.imag(y_data),5)
      
        new_y_data = fit[0]*x_range**5 + fit[1]*x_range**4 +fit[2]*x_range**3 +fit[3]*x_range**2 +fit[4]*x_range +fit[5]
        new_y_data_i = fit_i[0]*x_range**5 + fit_i[1]*x_range**4 +fit_i[2]*x_range**3 +fit_i[3]*x_range**2 +fit_i[4]*x_range +fit_i[5]
        new_complex = new_y_data + j*new_y_data_i
        if plot == True:
            
            py.plot(x_data,numpy.real(y_data), 'bs')
            py.plot(x_range,new_y_data, '-')
            py.title("real")
            py.show()
            py.plot(x_data,numpy.imag(y_data), 'bs')
            py.plot(x_range,new_y_data_i, '-')
            py.title("imag")
            py.show()
        return 0

        


def theta_generate(system, plot = False, realonly = False, useapproximations = False):
        global theta_2,theta_3, cos_theta_2, cos_theta_3, tan_theta_2
        (n_1,n_2,n_3) = system.indices
        
        theta_1 = system.theta_1
        freq = system.freq


        cos_theta_2 = (n_2)**-1  * array(n_2**2-((n_1)*sin(theta_1))**2,dtype = complex)
        cos_theta_3 = (n_3)**-1  * array(n_3**2-((n_1)*sin(theta_1))**2,dtype = complex)
        tan_theta_2 = sqrt((1-cos_theta_2**2)/cos_theta_2)

            
        theta_2 = numpy.arcsin(sin(theta_1) * n_1/ n_2,dtype = complex)
        theta_3 = numpy.arcsin(sin(theta_1)* n_1 / n_3,dtype = complex)

        
        
        if plot == True:

                
                py.plot(freq,numpy.real(cos_theta_2[IR]),'r')
                py.plot(freq,numpy.imag(cos_theta_2[IR]),'b')
                py.plot(freq,numpy.real(cos_theta_3[IR]),'g')
                py.plot(freq,numpy.imag(cos_theta_3[IR]),'k')
                py.title("cos Angles of incidence")
                py.legend(('real2','imag2','real3','imag3'))
                py.show()
        
        system.angles = (theta_2,theta_3, cos_theta_2, cos_theta_3, tan_theta_2)
        
        return 0


        

        


def calc_fresnel(system, d = 5,realonly = False, _plot =True, useapproximations =False):
        global  L_xx_1, L_yy_1, L_zz_1,L_xx_2, L_yy_2, L_zz_2, B, delta #, L_xx_1_sqr, L_yy_1_sqr, L_zz_1_sqr,L_xx_2_sqr, L_yy_2_sqr, L_zz_2_sqr
        global r_12_s, r_12_p, t_12_s, t_12_p, r_23_s, r_23_p, t_23_s, t_23_p
        global g

        freq = system.freq
        indices = system.indices
        theta_1 = system.theta_1
        angles = system.angles
        l = system.l
        (n_1, n_2, n_3) = system.indices
        (theta_2,theta_3, cos_theta_2, cos_theta_3, tan_theta_2) = system.angles
      
        
        B = 2 * pi * n_2 * d * cos_theta_2 / l
        
        
        delta = numpy.ndarray(n_2.shape, dtype = numpy.complex)
        delta[SFG] = 2 * pi * n_2[SFG] * d / l[SFG] / cos_theta_2[SFG]
        delta[VIS] = 2 * pi * d * n_2[VIS] / l[VIS] / cos_theta_2[VIS] - 2 * pi * n_1[VIS] * d * (tan_theta_2[VIS] + tan_theta_2[SFG]) * sin(theta_1[VIS]) / l[VIS]
        delta[IR] = 2 * pi * d * n_2[IR] / l[IR] / cos_theta_2[IR] - 2 * pi * n_1[IR] * d * (tan_theta_2[IR] + tan_theta_2[SFG]) *sin(theta_1[IR])/l[IR]  # question here about lambda vis (changed it to IR as of reading source 30, Z.Chen)
                                   
 
        r_12_p = (n_2*cos(theta_1) - n_1*cos_theta_2)/(n_2*cos(theta_1) + n_1*cos_theta_2)  ## r and t matrices are 3*"100" with each column reresenting a color region (SFG, VIS OR IR)
        r_12_s = (n_1*cos(theta_1) - n_2*cos_theta_2)/(n_1*cos(theta_1) + n_2*cos_theta_2)
        r_23_p = (n_3*cos_theta_2 - n_2*cos_theta_3)/(n_3*cos_theta_2 + n_2*cos_theta_3)
        r_23_s = (n_2*cos_theta_2 - n_3*cos_theta_3)/(n_2*cos_theta_2 + n_3*cos_theta_3)

        t_12_p = 2*n_1*cos(theta_1)/(n_2*cos(theta_1) + n_1*cos_theta_2)
        t_12_s = 2*n_1*cos(theta_1)/(n_1*cos(theta_1) + n_2*cos_theta_2)
        t_23_p = 2*n_2*cos_theta_2/(n_3*cos_theta_2 + n_2*cos_theta_3)
        t_23_s = 2*n_2*cos_theta_2/(n_2*cos_theta_2 + n_3*cos_theta_3)

                #x = ((numpy.real(n_2) - 1/numpy.cos(theta_1))**2 + numpy.imag(n_2)**2)/((numpy.real(n_2) + 1/numpy.cos(theta_1))**2 + numpy.imag(n_2)**2)
       
        if _plot == True:

               
                py.plot(freq, abs(1-r_23_p[IR])**2, 'r')
                py.plot(freq,s(r_12_p*r_23_p,2*B)[IR],'b')
                py.plot(freq, abs(1-r_23_p[IR])**2/s(r_12_p*r_23_p,2*B)[IR], 'g')
                py.legend(("top","bottom","ratio"))
                
                py.title('|r23p|^2 terms for IR')
                py.show()

               

        
       
      
        L_xx_1 = t_12_p * (1 - r_23_p*exp(2*j*B)) * cos_theta_2/cos(theta_1) / (1+r_12_p * r_23_p * exp(2*j*B))
        L_yy_1 = t_12_s * (1 + r_23_s*exp(2*j*B)) / (1+r_12_s * r_23_s * exp(2*j*B))
        
        #L_xx_1_sqr = abs(t_12_p)**2  *  abs(cos_theta_2)**2  / abs(cos(theta_1))**2   *  s(-r_23_p,2*B) /   s(r_12_p*r_23_p,2*B)
#        L_yy_1_sqr = abs(t_12_s)**2  *  s(r_23_s,2*B) / s(r_12_p*r_23_p,2*B)
        
        L_xx_1_sqr = abs(L_xx_1)**2
        L_yy_1_sqr = abs(L_yy_1)**2
        
        
        L_xx_2 = exp(j*delta) * t_12_p * (1 - r_23_p) * cos_theta_2/cos(theta_1) / (1+r_12_p * r_23_p * exp(2*j*B))
        L_yy_2 = exp(j*delta) * t_12_s * (1 + r_23_s) / (1+r_12_s * r_23_s * exp(2*j*B))
        
        L_xx_2_sqr = abs(L_xx_2)**2
        L_yy_2_sqr = abs(L_yy_2)**2
     
        L_zz_1 = numpy.ndarray(n_3.shape, dtype = numpy.complex)
        L_zz_2 = numpy.ndarray(n_3.shape, dtype = numpy.complex)
        L_zz_1_sqr = numpy.ndarray(n_1.shape, dtype = numpy.complex)
        L_zz_2_sqr = numpy.ndarray(n_1.shape, dtype = numpy.complex)
        for i in [SFG,VIS,IR]:
                if i == SFG:
                        n_interfaceI = n_1
                        n_interfaceII = n_2
                else:
                        n_interfaceI = n_2
                        n_interfaceII = n_3
                        
                L_zz_1[i] = t_12_p[i] * (1 + r_23_p[i]*exp(2*j*B[i])) * n_1[i] * n_2[i] / n_interfaceI[i] / (1+r_12_p[i] * r_23_p[i] * exp(2*j*B[i]))
                L_zz_2[i] = exp(j*delta[i]) * t_12_p[i] * (1 + r_23_p[i]) * n_1[i] * n_2[i] / n_interfaceII[i] / (1+r_12_p[i] * r_23_p[i] * exp(2*j*B[i]))

                L_zz_1_sqr[i] = abs(t_12_p[i])**2 * s(r_23_p[i],2*B[i]) * abs(n_1[i])**2 * abs(n_2[i])**2 / abs(n_interfaceI[i])**4 / s(r_12_p[i] * r_23_p[i] ,2*B[i])### updside down
                L_zz_2_sqr[i] = exp(-2*numpy.imag(delta[i]) ) * abs(t_12_p[i])**2 * abs(1 + r_23_p[i])**2 * abs(n_1[i])**2 * abs(n_2[i])**2 / abs(n_interfaceII[i])**4 / s(r_12_p[i] * r_23_p[i],2*B[i])

        lis  = [L_xx_1_sqr, L_yy_1_sqr, L_zz_1_sqr, L_xx_2_sqr, L_yy_2_sqr, L_zz_2_sqr]

        r = 0
      
        
        system.L_xx_1 = L_xx_1
        system.L_yy_1 = L_yy_1

        system.L_xx_1_sqr = L_xx_1_sqr
        system.L_yy_1_sqr = L_yy_1_sqr
        system.L_xx_2 = L_xx_2
        system.L_yy_2 = L_yy_2

        system.L_xx_2_sqr =L_xx_2_sqr
        system.L_yy_2_sqr =L_yy_2_sqr 

        system.L_zz_1 = L_zz_1 
        system.L_zz_2 = L_zz_2 
        system.L_zz_1_sqr = L_zz_1_sqr
        system.L_zz_2_sqr = L_zz_2_sqr
       
        
        return (L_xx_1_sqr, L_yy_1_sqr, L_zz_1_sqr,L_xx_2_sqr, L_yy_2_sqr, L_zz_2_sqr)

def ratio(gamma = 22):
    global water, d2o
    water =System('sapphire','gold','water', gamma = gamma)
    d2o = System('sapphire','gold','d2o', gamma = gamma)

    
    if numpy.any(numpy.imag(water.L_xx_2_sqr)):
                 print "water has imaginary Lxx2"
    if numpy.any(numpy.imag(d2o.L_xx_2_sqr)):
                 print "d2o has imaginary Lxx2"

    x = (water.L_xx_1_sqr/d2o.L_xx_1_sqr)[IR]
    y = (water.L_yy_1_sqr/d2o.L_yy_1_sqr)[IR]
    z = (water.L_zz_1_sqr/d2o.L_zz_1_sqr)[IR]

    print water.L_xx_2_sqr[IR]
    plot(water.freq,water.L_xx_2_sqr[IR])
    plot(d2o.freq,d2o.L_xx_2_sqr[IR])
    
   
    plot(water.freq,x, 'r')
    plot(d2o.freq,y, 'g')
    plot(water.freq,z, 'b')
    
    title('ratios of L for interface I')
    legend(("Lxx_2", "Lyy_2","Lzz_2"))
   
    x = (water.L_xx_2_sqr[IR]/d2o.L_xx_2_sqr[IR])
    y = (water.L_yy_2_sqr/d2o.L_yy_2_sqr)[IR]
    z = (water.L_zz_2_sqr/d2o.L_zz_2_sqr)[IR]
   
    py.plot(water.freq,x, 'r')
    py.plot(d2o.freq,y, 'g')
    py.plot(water.freq,z, 'b')
    
    py.title('ratios of L for interface II')
    py.legend(("Lxx_2", "Lyy_2","Lzz_2"))
    py.show()

    
    return 0







def Figure1():
    
    water =System('sapphire','gold','water', gamma = 22)
    d2o = System('sapphire','gold','d2o', gamma = 22)
    
    
    if numpy.any(numpy.imag(water.L_xx_2_sqr)):
                 print "water has imaginary Lxx2"
    if numpy.any(numpy.imag(d2o.L_xx_2_sqr)):
                 print "d2o has imaginary Lxx2"
    subplot2grid((3,2),(0,0))
    plot(water.freq,water.n_3[IR].real,'k-')
    plot(water.freq,water.n_3[IR].imag,'k.')
    legend(['$Re(n_{H2O})$','$Im(n_{H2O})$'], loc = 6)
    xticks([],[])
    subplot2grid((3,2),(0,1))
    plot(d2o.freq,d2o.n_3[IR].real,'k-')
    plot(d2o.freq,d2o.n_3[IR].imag,'k.')
    legend(['$Re(n_{D2O})$','$Im(n_{D2O})$'],loc = 7)
    xticks([],[])
    subplot2grid((3,2),(1,0), rowspan = 2)
    xlabel("$IR \    Wavenumber \ (cm^{-1})$")
    plot(water.freq,water.L_xx_1_sqr[IR],'rs')
    plot(water.freq,water.L_xx_2_sqr[IR],'bo')
    legend(['$Quartz/Gold$','$Gold/Water$'],loc=3)
    subplot2grid((3,2),(1,1), rowspan = 2)
    xlabel("$IR \ Wavenumber \ (cm^{-1})$")
    plot(d2o.freq,d2o.L_xx_1_sqr[IR],'rs')
    plot(d2o.freq,d2o.L_xx_2_sqr[IR],'bo')
    legend(['$Quartz/Gold$','$Gold/D_{2}O$'],loc = 4)
    return 0
    
   
    
    
#    py.title('ratios of L for interface I')
#    py.legend(("Lxx_2", "Lyy_2","Lzz_2"))
#    py.show()
#    x = (water.L_xx_2_sqr[IR]/d2o.L_xx_2_sqr[IR])
#    y = (water.L_yy_2_sqr/d2o.L_yy_2_sqr)[IR]
#    z = (water.L_zz_2_sqr/d2o.L_zz_2_sqr)[IR]
#   
#    py.plot(water.freq,x, 'r')
#    py.plot(d2o.freq,y, 'g')
#    py.plot(water.freq,z, 'b')
#    
#    py.title('ratios of L for interface II')
#    py.legend(("Lxx_2", "Lyy_2","Lzz_2"))
#    py.show()

def thickness():
    d_list = arange(1,101)
    L_xx_list = list()
    L_zz_list = list()
    
    for d in d_list:
        w = System('sapphire', 'platinum', 'water',gamma = 60,d = d)
        
        L_xx_list.append(w.L_xx_2_sqr[VIS,0])
        L_zz_list.append(w.L_zz_2_sqr[VIS,0])
    
    plot(d_list,L_xx_list)
    plot(d_list,L_zz_list)
    return 0
        
        








    
