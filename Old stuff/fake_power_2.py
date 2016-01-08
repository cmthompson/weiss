# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 18:04:59 2013

@author: Chris
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 16:35:49 2013

@author: Chris
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize
import numpy.linalg 
from numpy.linalg import norm 


#def power(m1,m2,m3,m4): return (1-(m4-m1)**2/100000)*(1-(m3-m1)**2/100000)*(1-(m2-m1)*2/100000)
def power(m1,m2): return (1-m1/4000)*(1-(m2-m1)**2/500000)
l = 100

m1_range = array([linspace(-100,100,l)]*l)
print m1_range.shape
m2_range = transpose(m1_range)  


pow_data = power(m1_range,m2_range)
#print pow_data
print pow_data.shape
#print m1
 
#plot(x_range,pow_data)
#subplot(111,projection = '3d')
#ax3 = fig.add_subplot(313,projection = '3d')
#ax1.plot_surface(m1,m2,pow_data)

#ax2.plot_surface(m1_range,m2_range,pow_data)
#ax3.plot_surface(m1,m2,pow_data)  
def slope_at(m1,m2,direction):
    grad = array([power(m1+0.01,m2)-power(m1,m2),
                      power(m1,m2+0.01)-power(m1,m2)])/0.01
    direction/=norm(direction)
   
    slope2 = dot(grad,direction) 
          
    
    return slope2
    
def step_along_ridge(m1,m2):
    
    
    gradient = array([power(m1+0.01,m2)-power(m1,m2),
                      power(m1,m2+0.01)-power(m1,m2)])/0.01
    
    
   
    
    #plot([0,gradient[0]*50000],[0,gradient[1]*50000],'b-')
                        
    ortho_1  =  array([-gradient[1],gradient[0]])
   
    ortho_1/=norm(ortho_1)
    
    if dot(gradient,ortho_1) >1E-20:
        print "error ortho1"
    
        
    #print ortho_3
    
    
    
    out = array([m1+10*ortho_1[0]/norm(ortho_1),m2+10*ortho_1[1]/norm(ortho_1)])
    return out
    
def plot_slope(m1,m2):
    r = linspace(0,2*3.14159,50)
    s = array([])
    for _r in r:
        s = numpy.append(s,slope_at(m1,m2,array([sin(_r),cos(_r)])))
    #plot(r,s)
   
    return 0
#plot_slope(1,1)

cla()
cs = contour(m1_range,m2_range,pow_data)
clabel(cs,inline = 1)   
m = array([0])
n = array([0.01])
_m = _n = 0
for i in range(10):
    (_m,_n) = step_along_ridge(_m,_n)
    m = append(m,_m)
    n = append(n,_n)
print m, n
plot(m,n, 'rs')