# -*- coding: utf-8 -*-
"""
Created on Wed May 21 17:53:14 2014

@author: Chris
"""
import pandas
phaseNR=0.3
j = complex(0,1)
x = arange(2100,3005,5,dtype = complex)
y = abs(1*exp(j*phaseNR)+250/((x-2400)+j*150)+250/((x-2600)+j*150))**2
v = array((x-min(x))/(max(x)-min(x)),dtype = complex)
print 'M = ',(x.size-1)/2
_M = (x.size-1)/2
R = pandas.Series(arange(-_M,_M+1),dtype = complex)
R.index= arange(-_M,_M+1)

def autocorrelation(m):return sum(y*exp(j*2*pi*m*v)*(v[1]-v[0]))
    
def calcem():
    autocorr = ndarray((0,_M+1),dtype = complex)
    
    
    for M in range(0,_M+1):
        l = array([],dtype = complex)
        
        for N in range(M,M-_M-1,-1):
            if N<0:
                N = N
            l = append(l,R[N])
            
        autocorr = append(autocorr,[l],axis = 0)
    
    return autocorr




for M in R.index:
    
    R[M] = autocorrelation(M)
e= calcem()
#eigenvals,eigenvecs = linalg.eig(e)
#a,b = eigenvecs,sqrt(eigenvals)
print e.shape
firstrow = e[0,:]
print all(e == transpose(e))
s = e[1:,1:]
t = -e[1:,0]

if any(imag(s)):
    print "imaginary s"
if any(imag(t)):
    print "imaginary t"

ak = linalg.solve(s,t)
ak = append(1,ak)

betasqrd = sum(firstrow*ak)
#for M in range(0,-(_M+1),-1):
#    beta+=ak[M]*R[M]
print betasqrd
beta = sqrt(betasqrd)
print beta

A_m = ones((v.size,),dtype = complex)
for k in range(1,_M+1):
    A_m+=ak[k]*exp(-j*2*pi*k*v)  ##### WARNING added a negative sign w.r.t paper in exponent


ErrorPhase = 0
chi = beta*exp(j*ErrorPhase)/A_m
phiA = arctan(imag(A_m)/real(A_m))

S  = abs(chi)**2
#plot(v,phiA)
#plot(v,imag(chi))
#plot(v,real(chi))
subplot(121)
plot(x,y,'s')
plot(x,S)

plot(x,real(chi))
plot(x,sqrt(S))*sin(phaseNR+ErrorPhase+phiA)
legend(['exp','Itheo','real','imag'])
subplot(122)
plot(x,phiA)





     




 