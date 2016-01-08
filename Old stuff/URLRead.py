from urllib2 import urlopen
import re
import numpy
from matplotlib import pyplot as py


def MovingAvg(data,window_len=50):
     y = array([])
     for k  in range(data.size):
         if k<window_len:
             y = append(y,mean(data[:k]))
         else:
             y = append(y,mean(data[k-window_len:k]))
     return y
         
  
  
watchlist = ["SSYS",
             "DDD",
             "SANW",
             "VO",
             "BBH"]



def Collect():
    
    subplot_i = 0
    array_list = []
    
    for company in watchlist:
        name = "http://ichart.finance.yahoo.com/table.csv?s="+company+"&a=06&b=15&c=2013&d=01&e=07&f=2014&g=d&ignore=.csv"
        response = urlopen(name)
        html= str(response.read())
        
        x = html.split('\n')
    
        
        
        g = numpy.array([])
        for a in x[1:-1]:
            i = a.split(',')
            g=numpy.append(g,float(i[4]))
        g = g[::-1]
        array_list.append(g)
        FDMA  = MovingAvg(g) 
        subplot_i +=1
        subplot(320+subplot_i)
        plot(g,'k')
        plot(FDMA,'b')
        title(company)
        
        
        for k in numpy.where(g>1.1*FDMA)[0]:
            axvline(x=k,color = 'b')
        
        for k in numpy.where(g>1.15*FDMA)[0]:
            axvline(x=k,color = 'y')
        for k in numpy.where(g>1.2*FDMA)[0]:
            axvline(x=k,color = 'r')
    show()
    return array_list
    
def TimeCorr(line):
    if type(line) == list:
        line=array(line[0], copy = True)
    FDMA = MovingAvg(line)
    no_plummets = 0
    no_highs = 0
    threshold = 1.1
    clf()
    
    plot(FDMA)
    plot(line)
    
    for k in where(line>threshold*FDMA)[0]:
        no_highs +=1
         
        axvline(x=k,color ='r')
        plummet=where(line[k:k+10]<line[k]*0.95)[0]
        
        if any(plummet):
            
            for i in plummet:
                print  line[k],line[i]
                axvline(x = k+i,color = 'b')
            no_plummets +=1
        
    print 'highs =', no_highs
    print 'plummets =', no_plummets
    show()
    return 0
    

def orbitz():
    import requests
    
    name = "http://www.orbitz.com/shop/airsearch?type=air&search=Search&ar.type=multiCity&ar.mc.slc[0].date=3%2F19%2F15&ar.mc.slc[2].date=3%2F23%2F15&ar.mc.slc[1].date=3%2F21%2F15&ar.mc.narrowSel=false&ar.mc.slc[0].time=Anytime&ar.mc.slc[1].time=Anytime&ar.mc.slc[2].time=Anytime&ar.mc.numAdult=1&ar.mc.cabin=C&ar.mc.onlyShowRefundable=false&ar.mc.numChild=0&ar.mc.slc[0].orig.key=ORD&ar.mc.slc[1].orig.key=PHX&ar.mc.slc[2].orig.key=SFO&ar.mc.nonStop=false&ar.mc.slc[0].dest.key=PHX&ar.mc.slc[2].dest.key=CHI&ar.mc.slc[1].dest.key=SFO&ar.mc.numSenior=0&recentSearch=True&ar.mc.slc[0].orig.dl=33123&ar.mc.slc[0].dest.dl=3652&ar.mc.slc[1].orig.dl=3652&ar.mc.slc[1].dest.dl=4468&ar.mc.slc[2].orig.dl=4468&ar.mc.slc[2].dest.dl=7840&strm=true"
            
    response = urlopen(name)
    
 
    url = 'http://www.orbitz.com/flights'
    payload = {'q':'python'}
    r = requests.get(url, params=payload)
    with open("/home/chris/Desktop/requests_results.html", "w") as f:
        f.write(r.content)
        f.close()
    with open('/home/chris/Desktop/orbitz.txt','wb') as f:
        f.write(str(response.read()))
        f.close()
    return 0
    
            
        
def mds():
    
    subplot_i = 0
    array_list = []
    
    for company in watchlist:
        name = 'http://www.accesstoinsight.org/tipitaka/mn/'
        response = urlopen(name)
        html= str(response.read())  
    return html
    
def md2():
    with open('/home/chris/Desktop/suttas/main.html', 'rb') as f:
        a = f.read()
    f.close()
    final = len(a)
    print 'final', final
    first = 0
    i =0
    while first<final-100:
        i+=1
        first  = a.find('<li><a id=',first) + 10
        if first== -1:
            print 'couldnt find next'
            break
        if i>1000:
            print 'over 1000'
            break
        last = a.find('>', first)
        addname =  a[first+1:last-1]
        print addname
        number = addname.split('.')[1]
        name = 'http://www.accesstoinsight.org/tipitaka/mn/'+addname+'.html'
        response = urlopen(name)
        html= str(response.read())  
        z =  open('/home/chris/Desktop/suttas/'+number+addname, 'wb')
        
        z.write(html)
        z.close()
    return 0
        
def md3():
    
    ld = os.listdir('/home/chris/Desktop/suttas')
    for name in ld:
        if 'main.html' in name or 'TOC' in name:
            continue
        
        with open('/home/chris/Desktop/suttas/'+name) as f:
            x = f.read()
            f.close()
        first = x.find('<!-- /robots -->')+16
        z = open('/home/chris/Desktop/suttas/'+name, 'wb')
        z.write('<body>\n')
        z.write(x[first:])
        z.close()
    return 0
    
def md4():
    
    ld = os.listdir('/home/chris/Desktop/suttas')
    for name in ld:
        if 'main.html' in name or 'TOC' in name:
            continue
        print name
        number= name[0:3]
        
        if '.' in name:
            
            
            with open('/home/chris/Desktop/suttas/'+name) as f:
                x = f.read()
                f.close()
            
            first = x.find('<div id="H_docTitle">')+21
            first = x.find(':',first)+1
            end = x.find('\t',first)
            title = x[first:end]
            title.replace('\t','')
            
            print number+title
            os.rename('/home/chris/Desktop/suttas/'+name, '/home/chris/Desktop/suttas/'+number+title)
            
            
        
    return 0

def md5():
    
    ld = os.listdir('/home/chris/Desktop/suttas')
    ld.sort()
    toc = open('/home/chris/Calibre Library/suttas/TOC.html','wb')
    toc.write('<html>\n\t<body>\n\t\t<h1>Table of Contents</h1>\n\t\t<p style="text-indent:0pt">\n')
    for name in ld:
       
        if 'main.html' in name or 'TOC' in name:
            continue
        
        toc.write('\t\t\t'+'<a href="/home/chris/Calibre Library/suttas/'+name+'.html">'+name+'</a><br/>\n')
        
        
        
    print '\t\t</p>\n\t</body>\n</html>'
    toc.write('\t\t</p>\n\t</body>\n</html>')
    toc.close()
            
        
    return 0

def md6():
    for i in os.listdir('/home/chris/Calibre Library/suttas'):
        print i
        if '.html'  not in i:
            os.rename('/home/chris/Calibre Library/suttas/'+i, '/home/chris/Calibre Library/suttas/'+i+'.html')
    return 0

    
