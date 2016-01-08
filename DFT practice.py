# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 22:20:29 2014

@author: chris
"""
import scipy.optimize

global x

L = 1
clf()



x = linspace(0,2,4000)
v = ndarray((4000,))
v[:1000] = 1
v[1000:1500]=0
v[1500:2500]=0
v[2500:3000]=1
v[3000:] = 1
v*=10



basis_k = arange(1,8)





def f(k):
    global x
    return 1/L*sin(k*pi*x/2)/sqrt(2000)

#def psi(A): return sqrt(2000)*((A[0]/L*sin(1*pi*x/2)+
#                    A[1]/L*sin(2*pi*x/2)+
#                    A[2]/L*sin(3*pi*x/2)+
#                    A[3]/L*sin(4*pi*x/2)+
#                    A[4]/L*sin(5*pi*x/2)+
#                    A[5]/L*sin(6*pi*x/2)+
#                    A[6]/L*sin(7*pi*x/2))/
#                    sum((A[0]/L*sin(1*pi*x/2)
#                    +A[1]/L*sin(2*pi*x/2)
#                    +A[2]/L*sin(3*pi*x/2)+
#                    A[3]/L*sin(4*pi*x/2)+
#                    A[4]/L*sin(5*pi*x/2)+
#                    A[5]/L*sin(6*pi*x/2)+
#                    A[6]/L*sin(7*pi*x/2))
#                    **2))

psi = lambda A:sqrt(2000)*((A[0]/L*sin(1*pi*x/2)+
                    A[1]/L*sin(2*pi*x/2)+
                    A[2]/L*sin(3*pi*x/2)+
                    A[3]/L*sin(4*pi*x/2)+
                    A[4]/L*sin(5*pi*x/2)+
                    A[5]/L*sin(6*pi*x/2)+
                    A[6]/L*sin(7*pi*x/2))/
                    sum((A[0]/L*sin(1*pi*x/2)
                    +A[1]/L*sin(2*pi*x/2)
                    +A[2]/L*sin(3*pi*x/2)+
                    A[3]/L*sin(4*pi*x/2)+
                    A[4]/L*sin(5*pi*x/2)+
                    A[5]/L*sin(6*pi*x/2)+
                    A[6]/L*sin(7*pi*x/2))
                    **2))
    
#for k in basis_k:
#    plot(x,f(k)+3)
#show()
    
#def energy(A,B,C,D,E,F,G):return (1.635*sum((f(x,A)+f(x,B)++f(x,C)+f(x,D)+f(x,E)+f(x,F)+f(x,G))**6) 
#                                    + sum(V*(f(x,A)+f(x,B)++f(x,C)+f(x,D)+f(x,E)+f(x,F)+f(x,G))**2))

def DFT():
    global V
    
   
    def T(A): return 1.645*100000*sum(psi(A)**6) 
    def V(A):
        global v
        return sum(v*(psi(A)**2))
    def energy(A):return T(A)+V(A)
  
    cons = ({'type': 'eq','fun' : lambda z: z[0]**2+z[1]**2+z[2]**2+z[3]**2+z[4]**2+z[5]**2+z[6]**2-1 },)
    bnds = ((0, None), (0, None),(0, None),(0, None),(0, None),(0, None),(0, None))
    
    x0=array([0.377,0.377,0.377,0.377,0.377,0.377,0])  # need to adjust equation so that energy reflects the total amount of wavefunction
    x0=array([0.5,0,0,0,0,0,0])  #
    x0[6] = sqrt(1-sum(x0[:6]**2))
    #print 'DFT start', x0[6]
    A = scipy.optimize.minimize(energy,x0,method='SLSQP', bounds=bnds,constraints=cons).x
    #print 'DFT sum of coefficients squared=',sum(A**2)
    #print 'DFT final integrated density=',sum(psi(A))**2
    #print 'DFT T and V',T(A),V(A)
    #print 'DFT final energy',energy(A)
    plot(x,psi(A))
    show()
    return energy(A)
    
def AI():
    
  
    def T(A): return sum((A*pi*arange(1,8))**2)/2 
    def V(A):return sum(v*(psi(A)**2))
    def energy(A):return T(A) + V(A)
   
    
    cons = ({'type': 'eq','fun' : lambda z: z[0]**2+z[1]**2+z[2]**2+z[3]**2+z[4]**2+z[5]**2+z[6]**2-1 },)
    bnds = ((0, None), (0, None),(0, None),(0, None),(0, None),(0, None),(0, None))
    x0=array([0.1,0.1,0.1,0.1,0.1,0.1,0]) 
    x0[-1] = sqrt(1-sum(x0[:6]**2))
    print 'ai start',x0[6]
    A = scipy.optimize.minimize(energy,x0,method='SLSQP', bounds=bnds,constraints=cons).x
    #print 'AI final sum of coefficients squared=',sum(A**2)
    #print 'AI final integrated density=',sum(psi(A)**2)
    #print 'AI T and V', T(A),V(A)
    plot(x,psi(A))
    #print 'AI final energy',energy(A)

    ylim(0,10)
    show()
    return A

multielectronAI = lambda n: pi**2/(2*L**2)*n*(n+1)*(2*n+1)/6


#plot(x,v)
#print AI()
#print DFT()
#legend(['V','ai','dft'])
#ylim(0,0.05)
#  

for n in arange(1,101,10):
    print n, 'electrons; real:', multielectronAI(n)
    print 'dft:', n*DFT()
    
