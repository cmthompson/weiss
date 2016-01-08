from scipy import optimize
from SFG_Analysis import *
import inspect
import time

cla()
x = linspace(0,30,100)

raw = ndarray((2,100))

def peak(x,A,G,w):return A/((x-w)+j*G)
    
    
def guess_gen(function):
    from numpy import random
    import inspect
    guess = [] 
    for w in inspect.getargspec(function):
        if 'A' in w:
            guess.append(0.1)
        elif 'w' in w:
            guess.append(random.random()*200+2800)
        elif 'G' in w:
            guess.append(10)
        else:
            guess.append(0)
    return guess
    
def perform_fit(a,name,functiontype, params = None):
   
    if functiontype == '100':
            w_name = ('A1','w1','G1','b')
            def function(x,A1,w1,G1,b): return abs(b + A1/((x-w1)+G1*j))**2
            guess =guess_gen(w_name)             
 
    elif functiontype == '320':
        w_name = ('A1','A2','A3','w1','w2','w3','G1','G2','G3','m','b')
        def function(x,A1,A2,A3,w1,w2,w3,G1,G2,G3,m,b): return abs(m*x/1000+b + peak(x,A1,G1,w1) + A2/((x-w2)+j*G2)+A3/((x-w3)+j*G3))**2
        guess = guess_gen(w_name)   
    elif functiontype == '301':
        w_name = ('A1','A2','A3','w1','w2','w3','G1','G2','G3')
        def function(x,A1,A2,A3,w1,w2,w3,G1,G2,G3): return abs( A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2)+A3/((x-w3)+j*G3))**2
        guess = guess_gen(w_name)     
        
    elif functiontype == '501':
        
        w_name = ('A1','A2','A3','A4','A5','w1','w2','w3','w4','w5','G1','G2','G3','G4','G5')
        def function(x,A1,A2,A3,A4,A5,w1,w2,w3,w4,w5,G1,G2,G3,G4,G5,m,b): return abs( A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+ A5/((x-w5)+j*G5))**2
        guess = guess_gen(w_name)    
                
   
   
       
        
    elif functiontype == '520':
        
        w_name = ('A1','A2','A3','A4','A5','w1','w2','w3','w4','w5','G1','G2','G3','G4','G5','m','b')
        def function(x,A1,A2,A3,A4,A5,w1,w2,w3,w4,w5,G1,G2,G3,G4,G5,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+ A5/((x-w5)+j*G5))**2
        guess = [3.09 ,  3.68,  -9.91,   9.35754873e+00,7.57248996e+00  ,
                  2853 ,2875, 2890 ,   2928,  2950,
                -1.36035884e+01, -1.43962348e+01,   -1.60710854e+01, 2.94587669e+01,   1.36613007e+01, 
                 2.5, -7]# guess_gen(w_name)  
        #guess = [3.68 ,  3.09,  -9.91,   9.35754873e+00,7.57248996e+00  , 14/50,  10/50 , 25/50,  38/50,   20/50,  1/50,  1/50, 1/50,   1/50,   1/50,  -2.10583537e-02/50, 5.66202100e-01]# guess_gen(w_name)  
    elif functiontype == '521':
        w1 = 2890
        w2= 2853
        w3=2928
        w4 = 2990
        w5 = 2855
        
        w_name = ('A1','A2','A3','A4','A5','G1','G2','G3','G4','G5','m','b')
        def function(x,A1,A2,A3,A4,A5,G1,G2,G3,G4,G5,m,b): return abs(m*x+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+ A5/((x-w5)+j*G5))**2
        guess = [3.68 ,  3.09,  -9.91,   9.35754873e+00,7.57248996,
                 -1.43962348e+01,  -1.36035884e+01, -1.60710854e+01,   2.94587669e+01,
                 1.36613007e+01,  -2.10583537e-01, 5.66202100e-01]# guess_gen(w_name)  
    
    elif functiontype == '620':  #6 peaks w linear background
       
        w_name = ('A1','A2','A3','A4','A5','A6','w1','w2','w3','w4','w5','w6','G1','G2','G3','G4','G5','G6','m','b')
        def function(x,A1,A2,A3,A4,A5,A6,w1,w2,w3,w4,w5,w6,G1,G2,G3,G4,G5,G6,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+A5/((x-w5)+j*G5)+A6/((x-w6)+j*G6))**2
        guess =[3.68 ,  3.09,  -9.91,   9.35,7.57 ,-6,
                2890,  2853 ,2890,  2928,  2950, 2970,
                 -14.3,  -13.6,15, -16.1 ,29.5,15,
                  -2.10583537e-01, 5.66202100e-01]
    elif functiontype == '600':  #6 peaks w no background
       
        w_name = ('A1','A2','A3','A4','A5','A6','w1','w2','w3','w4','w5','w6','G1','G2','G3','G4','G5','G6')
        def function(x,A1,A2,A3,A4,A5,A6,w1,w2,w3,w4,w5,w6,G1,G2,G3,G4,G5,G6): return abs(A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+A5/((x-w5)+j*G5)+A6/((x-w6)+j*G6))**2
        guess =[3.68 ,  3.09,  -9.91,   9.35,7.57 ,-6,
                2890,  2853 ,2890,  2928,  2950, 2970,
                 -14.3,  -13.6,15, -16.1 ,29.5,15]# guess_gen(w_name)
    elif functiontype == 'SixSFGFixedAmps':
       
        w_name = ('A1','A2','A3','A4','A5','A6','w1','w2','w3','w4','w5','w6','G1','G2','G3','G4','G5','G6','m','b')
        def function(x,A1,A2,A3,A4,A5,A6,w1,w2,w3,w4,w5,w6,G1,G2,G3,G4,G5,G6,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+A5/((x-w5)+j*G5)+A6/((x-w6)+j*G6))**2
        guess =[3.68 ,  3.09,  -9.91,   9.35,7.57 ,-6,
                2890,  2853 ,2890,  2928,  2980, 3000,
                 -14.3,  -13.6,15, -16.1 ,29.5,15,
                  -2.10583537e-01, 5.66202100e-01]
    elif functiontype == 'SixSFGFixedFreqsWidths':
        if params == None:
            
            w1 = 2890
            w2= 2853
            w3=2928
            w4 = 2990
            w5 = 2855
            w6 = 2960
        else:
            w1 = params[0]
            w2 = params[1]
            w3 = params[2]
            w4 = params[3]
            w5 = params[4]
            w6 = params[5]
            G1 = params[6]
            G2= params[7]
            G3 = params[8]
            G4 = params[9]
            G5 = params[10]
            G6 = params[11]
            
            
        
       
        w_name = ('A1','A2','A3','A4','A5','A6','m','b')
        def function(x,A1,A2,A3,A4,A5,A6,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+A5/((x-w5)+j*G5)+A6/((x-w6)+j*G6))**2
        guess =[3.68 ,  3.09,  -9.91,   9.35,7.57248996e+00 ,-6, -2.10583537e-01, 5.66202100e-01]# guess_gen(w_name) 
    #guess_gen(w_name)  
    elif functiontype == 'ThreeSFGFixedParams':
            
            w1= 2845
            
            w2= 2856
            w3= 2895
            
            #w4= 2981
            #G1=17
            #G2=20
            #G3=15
            #G4=14
            w_name = ('A1','A2','A3','G1','G2','G3','m','b')
            def function(x,A1,A2,A3,G1,G2,G3,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3))**2
            guess = guess_gen(w_name)  
            
            
                  
            
    else:
        return 0
        
    cla()
   
    #if result_array.shape[0] >1:
       # guess = result_array[1]
        
    #x = a[0][0:50]
    x = a[0][0:40]
    y = a[1][0:40]
    plot(x,y,'bs')
    #guess = [0.5,0.5,0.5,0.5,0.5,0.5,2850,2870,2900,2930,2950,2975,10,10,10,10,10,10,0.01,0.01]
    try:
        result = optimize.curve_fit(function,x,y,guess,maxfev = 10000)
    except:
        print "error", name
        print len(w_name)
        return zeros((2,len(w_name)))
    if True:        
        if len(w_name) == 7:
            plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6]))
        elif len(w_name) == 8:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7]))
        elif len(w_name) == 10:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9]))
        elif len(w_name) == 4:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3]))
        elif len(w_name) == 14:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9],result[0][10],result[0][11],result[0][12],result[0][13]))
        elif len(w_name) == 12:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9],result[0][10],result[0][11]))
        
        elif len(w_name) == 11:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9],result[0][10]))
        elif len(w_name) == 6:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5]))
        elif len(w_name) == 9:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8]))
        elif len(w_name) == 20:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],
                             result[0][9],result[0][10],result[0][11],result[0][12],result[0][13],result[0][14],result[0][15],result[0][16],result[0][17],
                               result[0][18],result[0][19]))
        elif len(w_name) == 17:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],
                             result[0][9],result[0][10],result[0][11],result[0][12],result[0][13],result[0][14],result[0][15],result[0][16]))
        elif len(w_name) == 15:
             plot(x,function(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],
                             result[0][9],result[0][10],result[0][11],result[0][12],result[0][13],result[0][14]))
    if int(functiontype[1]) > 0:   
        plot(x,(result[0][-2]*x/1000+result[0][-1])**2)
    if False:     
        print "Result Found for" , name
        #print "Referenced to IR spectrum" , reference_name
        #print "Normalized by constant", normalization_constant
        for i in range(len(w_name)):
        
            print w_name[i], result[0][i]
    for i in range(len(w_name)):
        if "w" in w_name[i]:
            axvline(x = result[0][i], ymin = 0, ymax = 1 ,color = 'r')
                
    #print result[0]    
    return result
    




raw[0] = 0.3*exp(-(x-10)**2/30)+ -0.1*exp(-(x-15)**2/20)
raw[1] = 0.3*exp(-(x-10)**2/30) + -0.1*exp(-(x-15)**2/20)#0.1*exp(-(arange(0,30)-10)**2/30) #+ 0.2*exp(-(arange(0,30)-15)**2/20))



    
def model(_x,A1,A2,w1,w2,G1,G2): return A1*exp(-(_x-w1)**2/G1) + A2*exp(-(_x-w2)**2/G2)
    
def model_sub(var):
    global raw
    global x
    
    A1 = var[0]
    A2 = var[1]
    w1 = var[2]
    w2 = var[3]
    G1 = var[4]
    G2 = var[5]
    _x =  x
    
    
    return sum(abs(model(_x,A1,A2,w1,w2,G1,G2) - raw[0]))



if False:
    y = raw[0]
    
    
    
    if x.shape != y.shape:
        print "shape error"
        print x.shape, 'not equal to', y.shape
    guess = [1,0.1,10,10,30,30]
    
    try:
        result = optimize.curve_fit(model,x,y,guess)
    
        
        plot(x,y,'bs')
        plot(x,model(x,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5]))
         
        print result[0]
        
        result2 = optimize.minimize(model_sub,guess)
        print result2.x
        print result2.success
        print result2.message
        
        plot(x,model(x,result2.x[0],result2.x[1],result2.x[2],result2.x[3],result2.x[4],result2.x[5]))
    except:
        print "error of"


###########################################
#os.chdir("C:\Users\Chris\My Documents\\Data\131105")

file_list05 =["C:\\Users\\Chris\\My Documents\\Data\\131105\\13110503.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110504.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110505.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110506.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110507.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110508.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110509.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110510.csv",
            "C:\\Users\\Chris\\My Documents\\Data\\131105\\13110511.csv"
            ]
            
file_list06 = ["C:\\Users\\Chris\\My Documents\\Data\\131106\\13110602.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110603.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110604.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110605.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110606.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110607.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110608.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110613.csv",
               "C:\\Users\\Chris\\My Documents\\Data\\131106\\13110614.csv"
                ]
functiontype = '520'           
l = int(functiontype[0])*(3-int(functiontype[2]))+int(functiontype[1]) 
result_array = ndarray((1,l)  )    
result_array2 = ndarray((1,(l-2)/3+2)) 


def one():
    global result_array, functiontype,result, sfg
    i = 1
    for spectrum in file_list05[3:6]:
        subplot(330+i)
        i+=1
        
        raw_sfg = OpenSFG(spectrum)
        
        smoothed_sfg = array(raw_sfg, copy = True)
        
        #smoothed_sfg[1][:] = SG_Smooth(smoothed_sfg[1],width = 5, order = 2)
        
      
        yy = perform_fit(smoothed_sfg,spectrum,functiontype)
        
        result_array = append(result_array,[yy[0]], axis =0)
        title(spectrum[-10:-4])
    print result_array
    savetxt("C:\\Users\\Chris\\My Documents\\Data\\fittingresults.csv",result_array)
        
        
        
    return 0 

def replot():
        global b,sfg,xs,x_len,result
        for i in range(b.shape[0]):
            subplot(330+i)
            plot(xs,b[i])
            plot(xs,sfg[i])
            
            baseline = abs(polyn(xs-i*5*x_len,*result[0][i*7+5:i*7+8]))**2
            plot(xs,baseline)
            for k in range(5):
                axvline(x = result[0][-(k+6)], ymin = 0, ymax = 1 ,color = 'r')
        return 0
        
def polyn(x,a,b,c): return a/1000000*x**2 + b/1000*x +c
     
     
def three(x_axis_range = (0,31),_plot = True,option = "optimize"):
    global result_array, functiontype,b, result, sfg
   
    cla()
    
    i = 1
    sfg = array([])
    sfg_list = []
    guess=()
    file_list = file_list05[:]
    x_len = x_axis_range[1]-x_axis_range[0]
    numpeaks = 5
    for spectrum in file_list:
        #subplot(330+i)
        i+=1
        
        guess += (-1,-1,9,3,1,0.1,0.1,0.1)   
        raw_sfg = OpenSFG(spectrum)
        #plot( raw_sfg[1])
        sfg = append(sfg,raw_sfg[1][x_axis_range[0]:x_axis_range[1]])
        #smoothed_sfg = array(sfg, copy = True)
        
    
        #smoothed_sfg[1][:] = SG_Smooth(smoothed_sfg[1],width = 5, order = 2)
   
    def function(x,_a,_b,_c,_d,_e,_f,_g,_h,_i,_j,_k,_l,_m,_n,_o,_p,_q,_r,_s,_t,_u,_v,_w,_y,_z,
                 _aa,_ab,_ac,_ad,_ae,_af,_ag,_ah,_ai,_aj,_ak,_al,_am,_an,_ao,_ap,_aq,_ar,_as,_at,_au,_av,_aw,_ay,_az,
                 _ba,_bb,_bc,_bd,_be,_bf,_bg,_bh,_bi,_bj,_bk,_bl,_bm,_bn,_bo,_bp,_bq,_br,_bs,_bt,_bu,_bv,
                 w1,w2,w3,w4,w5,
                     G1,G2,G3,G4,G5):
                 
            frame = inspect.currentframe()
            ArgInfo = inspect.getargvalues(frame)
            args = ArgInfo.args
            values = [ArgInfo.locals[s] for s in args]
            
            out = array([])
            num_vars = numpeaks + 3
            for i in range(len(file_list)):
                
                out = append(out, abs(polyn(x,*values[i*num_vars+6:i*num_vars+9])+
                                        values[i*num_vars+1]/(x-values[-10]+j*values[-5])+
                                       values[i*num_vars+2]/(x-values[-9]+j*values[-4])+
                                      values[i*num_vars+3]/(x-values[-8]+j*values[-3])+
                                     values[i*num_vars+4]/(x-values[-7]+j*values[-2])+
                                    values[i*num_vars+5]/(x-values[-6]+j*values[-1]))**2)
                
                                      
            return out                               
                
          
    print x_len
    xs =  arange(x_len)*5+2800                                                                              
    x_range = arange(sfg.size)*5+2800
    
    
    y_range = empty_like(sfg)
    copyto(y_range,sfg)
   
    
                                        
    guess+= (2840,2860 ,2890,  2925,  2951,
                10,10,10,10,10)
                
  
    a_range = function(xs,*guess)
    print a_range.size, x_range.size
    plot(x_range,y_range)
    plot(x_range,a_range)
    
    start_time = time.time()
    tup_result = ()
    if option == "optimize":
        result = optimize.curve_fit(function,xs,y_range,guess,maxfev = 1000000)
                
       
        
        
        for i in result[0]:
            tup_result += (i,)
    elif option == "minimize":
        result = optimize.minimize(function(xs)-y_range,*guess,method = 'nelder-mead')
        tup_result = ()
        
        for i in result[0]:
            tup_result += (i,)
    else:
        for i in result[0]:
            tup_result += (i,)
    print "result obtained in", (time.time()-start_time)    
    b = function(xs,*tup_result)
    #for i in range(len(file_list)):
       
        #result[0][i*7+6]-=i*5*result[0][i*7+5]*x_len/1000
       
   
    
    end_As = len(file_list)*8
    value_result = reshape(insert(result[0],[end_As+5,end_As+5,end_As+5,end_As+10,end_As+10,end_As+10],[0,0,0,0,0,0]),(-1,8))
    
   
    
    
    savetxt("C:\\Users\\Chris\\Desktop\\fittingresults.csv",value_result,delimiter =',')
    
    b = reshape(b,(-1,x_len))
    sfg = reshape(sfg,(-1,x_len))
    cla()
    
    replot()
    return 0

        
figure()       

