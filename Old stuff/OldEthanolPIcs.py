# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 11:05:33 2014

@author: Chris
"""

def Figure7():
    import sys
    if sys.platform == 'linux2':
        p = "/home/chris/Dropbox/SFG Data/"
    else:
        p = "C:/Users/Chris/Dropbox/SFG Data/"
    
    
    clf()
    
    subplot(221)   ###50% ethanol
    file_list =  ['140204/14020410.csv',
              '140204/14020411.csv',
              '140130/14013013.csv']
    all_data = ndarray((1,61))
    all_data[0] = arange(2800,3105,5)
    for n in file_list:
        a = OpenSpectrum(p+n).Array
        x = a[0,:,0]
        x1 = where(x == 2800)[0]
        x2 = where(x==3100)[0]
        x = x[x1:x2+1]
        
        y = a[2:,x1:x2+1,0]
        plot(a[0,:,0],a[1,:,0])
        
        all_data = append(all_data,y,axis  =0)
    
  
    plot(all_data[0],mean(all_data[1:],axis = 0), color = 'k')
    title("50%")
    #legend(file_list)
    
    subplot(222)  ###100% ethanol
    file_list =  ['140201/14020105.csv',
              '140201/14020106.csv',
              '140201/14020107.csv',
              '140201/14020108.csv']
    all_data = ndarray((1,61))
    all_data[0] = arange(2800,3105,5)
    for n in file_list:
        a = OpenSpectrum(p+n).Array
        x = a[0,:,0]
        x1 = where(x == 2800)[0]
        x2 = where(x==3100)[0]
        x = x[x1:x2+1]
        
        y = a[2:,x1:x2+1,0]
        plot(a[0,:,0],a[1,:,0])
        
        all_data = append(all_data,y,axis  =0)
    
  
    plot(all_data[0],mean(all_data[1:],axis = 0), color = 'k')
    
    title("100%")
 
    subplot(223)  ###100% ethanol
    file_list =  ['140204/14020403.csv',
              '140204/14020404.csv',
              '140204/14020405.csv']
    all_data = ndarray((1,61))
    all_data[0] = arange(2800,3105,5)
    for n in file_list:
        a = OpenSpectrum(p+n).Array
        x = a[0,:,0]
        x1 = where(x == 2800)[0]
        x2 = where(x==3100)[0]
        x = x[x1:x2+1]
        
        y = a[2:,x1:x2+1,0]
        plot(a[0,:,0],a[1,:,0])
        
        all_data = append(all_data,y,axis  =0)
    
  
    plot(all_data[0],mean(all_data[1:],axis = 0), color = 'k')
    
    subplot(224)
    
        
    
    width = 5
    interval = 5
    _plot = True
    smooth = True
    _from = 1
    to = -1
    _legend = True
    
    legend_list = list()       
    
    time_series_spec = ndarray((all_data.shape[0],all_data.shape[1],4)) 
    time_series_spec[:,:,0] = all_data
    
    freq = time_series_spec[0,_from:to,0]
    return_val = [freq]
    size= time_series_spec.shape[0]
    averaged = ndarray((0,26))
    for i in range(1,size-width/2,interval):
        
        
        
        ys =  mean(time_series_spec[i:i+width,_from:to,0], axis = 0)
        
        if smooth == True:
            ys = SG_Smooth(ys)
        return_val.append(ys)
        if i > 20:
            char_str = 's'
        else: 
            char_str = '-'
        plot(freq,ys,char_str,label = str(i), )
        legend_list.append(str(i))
    if _legend ==True:
        gca().legend(legend_list)
    
    
    return 0
    
    def Figure6():
    global t
    clf()
    
    
  
       
    subplot((121))
    g = TimeSeries('C:/Users/Chris/Dropbox/SFG Data/140103/14010302.csv',interval  =3, _legend = False)  
    h = TimeSeries('C:/Users/Chris/Dropbox/SFG Data/140103/14010303.csv',interval  =3, _legend = False)
    ylabel('$SFG\ Intensity\ (a.u.)$', size = 20)
    xlabel('$IR\ Wavenumber\  (cm^{-1})$', size = 20)
    t = array([])
    for z in g[1:]:
        #print z.shape
        t= append(t,mean(z))
    for z in h[1:]:
        #print z.shape
        t= append(t,mean(z))
     
        #print z[40]
    subplot((122))
    plot(arange(t.size),t,'.')
    plot(arange(t.size),t,'-')
    plot(arange(6,13),arange(6,13)*-0.05149798+0.62875121)
    ylabel('$Average\ Signal\ (a.u.)$', size =20)
    xlabel('$Time (min))$',size = 20)

    return 0  
    
    def Figure3():  # Shows results from 1/8 where H2 bubbled water and O2 bubbled water then alcohol were flowed.

    if sys.platform == 'linux2':
        p = "/home/chris/Dropbox/SFG Data/140108/"
    else:
        p = "C:/Users/Chris/Dropbox/SFG Data/140108/"
    clf()
    plot(*OpenSFG(p+"14010802.csv", "AvgSFG"),color = 'r')  # pure H2 bubbled water
    plot(*OpenSFG(p+"14010803.csv", "AvgSFG"),color = 'b') # 0/30 air/n2 bubbled water
    plot(*OpenSFG(p+"14010804.csv", "AvgSFG"),color = 'k') # 1% Ethanol in water 10/30 air/n2
    s = OpenSpectrum(p+"14010805.csv").Array 
    plot(s[0,:,0],mean(s[7:,:,0],axis = 0),color = 'g')       # flushed with water
    legend(['H2/H2O','air/H2O', 'air/1% EtOH','air/H2O'],loc = 2)
    
    
    return 0
    
def Figure4():# Time series of adsorption of alcohol onto an oxygen covered surface and desorption of into water only.  
    
    
        
#    file_list = ["/140121/14012103.csv",
#                 "/140121/14012104.csv",
#                 "/140121/14012105.csv"]
   
    file_list = ["/140108//14010802.csv",
                 "140108/14010803.csv",
                  "140108/14010804.csv",
                 "/140108/14010805.csv"]
                 
#    file_list = ['/140107/14010703.csv',
#                '/140107/14010704.csv',
#                '/140107/14010705.csv']

    clf()
    s = len(file_list)*100 + 21
    total = array([])
    line_pos = array([])
    for i in range(len(file_list)):
       
        subplot((s+i*2))
        g = TimeSeries(SFGDataFolder+file_list[i],interval  =1, _legend = False)  #O2 covered surface covered by 1% ethanol
        t = array([])
        for z in g[1:]:
            #print z.shape
            t= append(t,mean(z))
            total = append(total,mean(z))
            #print z[40]
        line_pos = append(line_pos,len(total))
        subplot((s+i*2+1))
        plot(t,'.')
        plot(t,'-')
    f = figure()
    ax = f.add_subplot(111)
    ax.plot(total)
    arr_dict = {'color':'k','width':2}
    for x in line_pos:
        axvline(x =x)
    annotate('H2/H2O',(10,0.3), color = 'k', size = 15)
    annotate('O2/N2/H2O',(20,0.35), color = 'k', size = 15)
    annotate('EtOH/O2/N2/H2O',(65,0.3), color = 'k', size = 15)
    annotate('O2/N2/H2O',(80,0.35), color = 'k', size = 15)
    
    

    return 0