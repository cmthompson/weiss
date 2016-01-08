# -*- coding: utf-8 -*-
"""
Created on Mon Jan 06 21:34:05 2014

@author: Chris
"""


from ThinFilmFresnel import System

SFG = 0
VIS = 1
IR  = 2

sy1 = System('platinum', 'methanol','water',d = 0.5)
sy2 = System('platinum','water','water',d = 0.5)

def sys1():
    angle_vis = 75
    angle_IR = 45
    # calculate the ppp fresnel factors for the first (pt/methanol) and second (methanol/water) interface .
    
    chi_ppp_1_int1 = (-sy1.L_xx_1[SFG]*sy1.L_xx_1[VIS]*sy1.L_zz_1[IR]*cos(radians(62))*cos(radians(angle_vis))*sin(radians(45))
               -sy1.L_xx_1[SFG]*sy1.L_zz_1[VIS]*sy1.L_xx_1[IR]*cos(radians(62))*cos(radians(angle_vis))*cos(radians(45))
                +sy1.L_zz_1[SFG]*sy1.L_xx_1[VIS]*sy1.L_xx_1[IR]*sin(radians(62))*cos(radians(angle_vis))*cos(radians(45))
                 +sy1.L_zz_1[SFG]*sy1.L_zz_1[VIS]*sy1.L_zz_1[IR]*sin(radians(62))*sin(radians(angle_vis))*sin(radians(45)))
    
    chi_ppp_1_int2 = (-sy1.L_xx_2[SFG]*sy1.L_xx_2[VIS]*sy1.L_zz_2[IR]*cos(radians(62))*cos(radians(angle_vis))*sin(radians(45))
               -sy1.L_xx_2[SFG]*sy1.L_zz_2[VIS]*sy1.L_xx_2[IR]*cos(radians(62))*cos(radians(angle_vis))*cos(radians(45))
                +sy1.L_zz_2[SFG]*sy1.L_xx_2[VIS]*sy1.L_xx_2[IR]*sin(radians(62))*cos(radians(angle_vis))*cos(radians(45))
                 +sy1.L_zz_2[SFG]*sy1.L_zz_2[VIS]*sy1.L_zz_2[IR]*sin(radians(62))*sin(radians(angle_vis))*sin(radians(45)))
                 
    #a = -sy1.L_xx_2[SFG]*sy1.L_xx_2[VIS]*sy1.L_zz_2[IR]*cos(radians(62))*cos(radians(70))*sin(radians(45))
    #b=-sy1.L_xx_2[SFG]*sy1.L_zz_2[VIS]*sy1.L_xx_2[IR]*cos(radians(62))*cos(radians(70))*cos(radians(45))
    #c=sy1.L_zz_2[SFG]*sy1.L_xx_2[VIS]*sy1.L_xx_2[IR]*sin(radians(62))*cos(radians(70))*cos(radians(45))
    #d=sy1.L_zz_2[SFG]*sy1.L_zz_2[VIS]*sy1.L_zz_2[IR]*sin(radians(62))*sin(radians(70))*sin(radians(45))
                 
    #chi_ssp_1_int1 = sy1.L_yy_1[SFG]*sy1.L_yy_1[VIS]*sy1.L_zz_1[IR]*sin(radians(45))             
    #chi_ssp_1_int2 = sy1.L_yy_2[SFG]*sy1.L_yy_2[VIS]*sy1.L_zz_2[IR]*sin(radians(45))
             
    
    plot(sy1.freq,abs(chi_ppp_1_int1)**2,'b')
    plot(sy1.freq,abs(chi_ppp_1_int2)**2,'r')
    
    #plot(sy1.freq,abs(chi_ssp_1_int1)**2,'b')    # ssp component at first interface
    #plot(sy1.freq,abs(chi_ssp_1_int2)**2,'r')   # ssp component at second interface
    
    # next four terms are the separate terms in ppp of the second interface
    #plot(sy1.freq,abs(a)**2,'r')   
    #plot(sy1.freq,abs(b)**2,'b')
    #plot(sy1.freq,abs(c)**2,'g')
    #plot(sy1.freq,abs(d)**2,'k')  # this term has the greatest influence on the ppp term of the second interface
    
    
    return 0
    
def sys2():
    chi_ppp_2_int1 = (-sy2.L_xx_1[SFG]*sy2.L_xx_1[VIS]*sy2.L_zz_1[IR]*cos(radians(62))*cos(radians(70))*sin(radians(45))
               -sy2.L_xx_1[SFG]*sy2.L_zz_1[VIS]*sy2.L_xx_1[IR]*cos(radians(62))*cos(radians(70))*cos(radians(45))
                +sy2.L_zz_1[SFG]*sy2.L_xx_1[VIS]*sy2.L_xx_1[IR]*sin(radians(62))*cos(radians(70))*cos(radians(45))
                 +sy2.L_zz_1[SFG]*sy2.L_zz_1[VIS]*sy2.L_zz_1[IR]*sin(radians(62))*sin(radians(70))*sin(radians(45)))
    
    chi_ssp_2_int1 = sy2.L_yy_1[SFG]*sy2.L_yy_1[VIS]*sy2.L_zz_1[IR]*sin(radians(45))      
    
   # plot(sy2.freq,abs(chi_ppp_2_int1)**2,'gs')
    
    plot(sy2.freq,abs(chi_ssp_2_int1)**2,'gs')
    
    return 0
    
cla()
sys1()
#sys2() 
legend(['int1', 'int2','h2o'])        

           