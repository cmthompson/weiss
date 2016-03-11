# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 21:16:59 2015

@author: chris

"""
from numpy.random import random
from RamanTools3 import polyeval,SGsmooth
from scipy.optimize import curve_fit, leastsq, minimize

def ffc():
    numpix=300
    numshifts = 100
    p = arange(2048)
    S = random((2048,))/10
    l=0.00025*p**2+1000
    print l
    
    F = -(l-1500)**2/10 +10**4
    R = 1000*exp(-(l-1150)**2*0.01)
    spectrum = (1+S)*(F+R)
   
    
    tup = ndarray((numshifts,1024))
    for i in range(numshifts):
        tup[i,:]=spectrum[i:1024+i]*(1+random((1024,))/100)
    I_ff = mean(tup,axis = 0) 
    D = mean(spectrum[0:1024],axis = 0)    
    spec_2 = tup[:,0:1024]
    for i in range(1):
        #plot(spec_2[i])
        #plot(I_ff)
        #plot(spec_2[i]-I_ff)
        z = polyfit(range(1024),spec_2[i]/I_ff,4)
        print z
        def D_p(x,a,b,c,d):return polyeval([a,b,c,d],x)*I_ff
        r = curve_fit(D_p,arange(1024),spec_2[i],p0=[0.01,0.01,0.01,0.01])[0]
        print r
        #plot(D_p)
        plot(spec_2[i])
        plot(D_p(arange(1024),*r))
    return 0    
        
    print tup.shape
    
    plot(I_ff)
    plot(D)
    plot(spectrum)
    return 0
    for i in range(numshifts):
       
        r =  array([tup[i,100+i:100+numpix+i]])
        
        fit = polyfit(range(numpix),r[0,:],4)
        r[0]-=polyeval(fit,arange(numpix))
        tup2 = append(tup2,r, axis = 0)
    subplot(211)
    plot(transpose(tup2),'k',label='ffc')
    subplot(212)
    plot(range(100,100+numpix),mean(tup2,axis=0))
    plot((1+S)*R,'b',label='data')
    
    s = mean(tup[:numshifts],axis=0)
    fit = fit = polyfit(arange(1024),s,4)
    s-=polyeval(fit,arange(1024))
    plot(s,'r',label='traditional')
    legend()
    
    
    return tup
    
def ct():
    numpix=300
    numshifts = 200
    fluorescencelevel = 10**4
    ramanlevel = fluorescencelevel/1000
    randomnoiselevel = 0.1*fluorescencelevel
    patternnoiselevel = 0.01*fluorescencelevel
    ax1=axes()
    figure()
    ax2=axes()
    
    p = arange(2048)
    S = random((2048,))*patternnoiselevel/10000
    l=0.00025*p**2+1000
    n = random((numshifts,2048))*randomnoiselevel
    
    
    F = (-(l-1500)**2/1E6 +1)*fluorescencelevel
    R = ramanlevel*exp(-(p-1000)**2*0.001)
    
    spectrum=(F+R)
    #spectrum = array([((F+R))[512:1536]]*numshifts)+random((numshifts,1024))*randomnoiselevel
    
    sp = array([(F+R)*(1+S)]*numshifts)+n
    sp = mean(sp,axis=0)
    
    
    ax1.plot(p,spectrum)
    ax1.vlines(1000, 0,10000)
   
    data = array([spectrum]*numshifts)+n
    for i in range(numshifts):
        data[i]=roll(data[i],-i)
       # ax1.plot(data[i])
    data*=1+S
    data = data[:,512:512+1024]
    
    
    if False:
        for i in range(0,numshifts,20):
            plot(data[i])
            return 0
    ############################ data has been generated in 'data', an array of spectra shifted by one pixel.  
    
    
    ###############use something like etchegoin to get out noise
    
    tup = copy(data)
   
    pad = zeros((tup.shape[0],512))
    tup = append(pad,tup,axis = 1)
    tup = append(tup,pad,axis = 1)   #### pad with zeroes
    Snoise = array([mean(tup,axis = 0)]*tup.shape[0])
    tup-=Snoise
    if False:
        plot(tup[0])
        plot(Snoise[0])
        plot(1+S[0])
        
        ## tup-=Snoise
        plot(tup[0])
        return 0
    
    
    
    for i in range(tup.shape[0]):
        def addup(a): return sum((tup[i]-Snoise[i]-a)**2)
        r = minimize(addup,40000)
        tup[i]-=r.x
        tup[i] = roll(tup[i],i)  ###### correct the pixel offset
    
    
    fit = polyfit(arange(2048), sp,4)
    sp2 = sp- polyeval(fit,arange(2048))
   # ax2.plot(arange(2048),sp2,label='averaged')   #### just averaged, no pixel noise removed
    
    tup_av = mean(tup[:numshifts,512:1536],axis = 0)
    tup_av-=41800+5500
    
    ax2.plot(arange(512,1536),tup_av,label='etchegoin')  #######averaged to remove pattern and random noise from CCD
    ###############use something like find from flat spectrum and divide
    
    
    
    
    flatdata = array([F]*numshifts)*(1+S)+random((numshifts,2048))*randomnoiselevel
    flatdata = mean(flatdata,axis = 0)
    noise =flatdata/SGsmooth(arange(2048), flatdata, width =21)
    if False:
        plot(flatdata,'s')
        plot(SGsmooth(arange(2048), flatdata, width =21))
        plot(noise)
        return 0
    sp/=noise
    fit = polyfit(arange(2048), sp,4)
    sp2 =sp-polyeval(fit,arange(2048))#### remove flourescence baseline 4th order using polyfit
    
    ax2.plot(sp2,label = 'divide')
    plot(arange(2048),R,label = 'pure')
    legend()
    
    vlines(1000, 0,10000)
    ylim(-100,2000)
    
    return 0
    
def ct2():
    from RamanTools3 import RamanSpectrum
    os.chdir('/home/chris/Documents/DataWeiss/150318/1percent')
    data = zeros((0,1024))
    frequency = zeros(data.shape)
    
    l = os.listdir(os.curdir)

    l.sort()
    for x in l:
        if 'notes' not in x and '.txt' in x:
            a = loadtxt(x,unpack = True)
            data = append(data,array([a[1]]), axis = 0)
            frequency = append(frequency, array([a[0]]),axis = 0)
    print data.shape[0], 'spectra averaged'
    plot(frequency[:,512], 's')
    figure()
    ##########now the data is in the proper form.
    
    tup = copy(data)
   
    pad = zeros((tup.shape[0],512))
    tup = append(pad,tup,axis = 1)
    tup = append(tup,pad,axis = 1)   #### pad with zeroes
    Snoise = array([mean(tup,axis = 0)]*tup.shape[0])
   
    if False:
        plot(tup[0])
        plot(Snoise[0])
        plot(tup[1],'s')
        
        plot(tup[0])
        return 0
    
    for i in range(tup.shape[0]):
        
        z = mean(tup[i])/mean(Snoise[0])
        
        tup[i]-=z*Snoise[0]
       
        
       
        tup[i] = roll(tup[i],i)  ###### correct the pixel offset
       
    figure()     
    
    
    
    tup_av = mean(tup[:,512:1536],axis = 0)
    
    
    
    plot(arange(512,1536),tup_av,label='etchegoin') 

    return 0
    
        
        
        
    