# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 12:03:49 2013

@author: Chris
"""

from Tkinter import *
import Tkinter
import tkFileDialog, tkSimpleDialog
import tkMessageBox
import matplotlib.axes
import matplotlib.figure
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import csv, os
import numpy

from scipy import optimize
from numpy import *
from matplotlib.pyplot import *




j = complex(0,1)

class SpectrumArray:
    #SpectrumArray class is a 3D object containing spectrum data from 4 channels: SFG, IR, Norm, Stdev
    FrequencyList = []
    Array = numpy.array([])
    StartFreq = 0
    EndFreq = 0
    StepSize=0
    FilePath = ''
    
    
    def __init__(self,startfreq =2800,endfreq = 3600,stepsize = 5, name = "Current"):
        
        self.EndFreq = endfreq
        self.StepSize = stepsize
        self.FrequencyList = numpy.arange(startfreq,endfreq+stepsize,stepsize)
        self.Name = name
        
        self.Array = numpy.array([[numpy.zeros(4)]*len(self.FrequencyList)]*3)
        ##logging.debug("initialized array" + str(self.Array.shape))
        self.Array[0,:,0] = self.FrequencyList
        self.Array[0,:,1] = self.FrequencyList
        self.Array[0,:,2] = self.FrequencyList
        self.Array[0,:,3] = self.FrequencyList
        
      
        return None
    

    def reset(self,startfreq =2800,endfreq = 3600,stepsize = 5):
        self.StartFreq = startfreq
        self.EndFreq = endfreq
        self.StepSize = stepsize
        self.FrequencyList = numpy.arange(startfreq,endfreq+stepsize,stepsize)
        
        self.Array = numpy.array([[numpy.zeros(4)]*len(self.FrequencyList)]*3)
        #logging.debug("reset array "+ str(self.Array.shape))
        self.Array[0,:,0] = self.FrequencyList
        self.Array[0,:,1] = self.FrequencyList
        self.Array[0,:,2] = self.FrequencyList
        self.Array[0,:,3] = self.FrequencyList

        return 0

    def insertpoint(self,column,frequency,data):
        
        if len(data)!= self.Array.shape[2]:
            #logging.warning("Data input failed")
            return -1
        if frequency>self.EndFreq or frequency<self.StartFreq:
            #logging.warning("Data input failed.  Frequency out of range.")
            return -1
        if column+1 >= self.Array.shape[0]:
            #logging.debug("added column to array")
            self.Array = numpy.append(self.Array,[[numpy.zeros(4)]*len(self.FrequencyList)],axis =0)
        
        self.Array[column+1,(frequency-self.StartFreq)/self.StepSize]=data
             
        self.Array[1,(frequency-self.StartFreq)/self.StepSize] = numpy.mean(self.Array[2:,(frequency-self.StartFreq)/self.StepSize], axis = 0)
        
        #logging.debug("inserted point to spectrum array")
        return 0

    def ContDatainsertpoint(self,data):  #data in the form of a 1dimensional numpy array
        if len(data)!= self.Array.shape[2]:
            #logging.warning("Data input failed. Not the right length")
            return -1
        self.Array[2,69]=data
       
        self.Array[2] = numpy.append(numpy.delete(self.Array[2,:,:],0,axis =0),[[0,0,0,0]],axis = 0)
        
        return 0

    def Duplicate(self, name = ''):
        
        x = SpectrumArray()
        if name == '':
            x.Name = self.Name = self.Name+'1'
        x.Array = numpy.array(self.Array, copy = True)
        return x
    
def SG_Smooth(y_array, width = 9, order = 3, plot_val =False):
    
    if order>5:
        return -1
    ret_val = ndarray(y_array.shape)
    for x in range(y_array.shape[0]):
        x_max = x+width/2
        x_min = x-width/2
        if x<width/2:
            x_min = 0
            
            
           
        if x > y_array.shape[0]-width/2-1:
            x_max = y_array.shape[0]-1
            
            
       
        x_fit  = arange(x_min-x,x_max+1-x ) 
        
       
        
        #try:
        fit = polyfit(x_fit,y_array[x_min:x_max+1],order)
        #except:
            #print "failed fit"
            #fit=[0]
        
      
        y = fit[-1]
        ret_val[x] = y
        
   
        
    if plot_val ==True:
        
        plot(y_array, 'bs')
        plot(ret_val,'r-')
        

    return ret_val

def OpenSFG(file_name, channel = 'AvgSFG'):
   
    if channel == 'AvgSFG':
        chan_no = 1
    elif channel == 'AvgIR':
        chan_no = 2
    
    
    if file_name == []:
        
        return -1
    if  type(file_name) is list:
        file_name = file_name[0]
    
    a = loadtxt(file_name,
            dtype = float, 
            delimiter = ',',
            skiprows = 1,
            usecols = (0,chan_no),
            unpack  = True)
   
    return a
        
        
        
  
    

def ConsolidateFiles(file_list, smooth = False, normalize = True):
    global x, dirname, kNorm 
    
    x = ndarray((0,161))    
    
    for file_name in file_list: 
        a = OpenSFG(file_name)
        
       
        
            
        
    if smooth == True:
        a[1][0:60] = SG_Smooth(a[1][0:60], width = 9, order = 2)
        a[1][60:] = SG_Smooth(a[1][60:], width = 17, order = 2)
    
    plot(a[0],a[1])
    
    #a[1] = a[1]/kNorm         
    x = append(x,a, axis = 0)
                 
            
           
    dirname = os.path.dirname(file_list[0])
            

            
    return 0

def SaveSpectrum(master,file_list,x):
        os.chdir(dirname)
    
        try:
                with open('consolidatedspectra.csv',"wb") as f:
                        CSV_FILE = csv.writer(f,dialect = 'excel')
                        header_list = []
                        for file_name in file_list:
                            header_list.append('Freq')
                            header_list.append("'"+os.path.basename(file_name)[0:-4])
                        
                        
                        
                        
                        for row in range(x.shape[1]-1):
                                flat = x[:,row]
                                
                                CSV_FILE.writerow(flat)
                       
                    
                    
                    
                        f.close()

                                
                       
        except:
                print 'error'
                return -1
               
    
        return 0

def DisplaySpectrum(master):
    import re
    global name_list, str_name_list
    file_opt = options = {}
    options['defaultextension'] = '.csv'
    options['filetypes'] = [('all files', '.*')]
    options['initialdir'] = 'C:\\Users\\Chris\\Desktop\\131105'
    options['title'] = 'Open Spectrum...'
    options['parent'] = master


    
    str_name_list = tkFileDialog.askopenfilename(**options)
    
    
    
    
    if str_name_list == '':
        return None
   
 
    #else:
        #name_list = re.split('{',str_name_list)
        #name_list.remove('')
        
        #for item in name_list:
            #item = item.encode('unicode_escape')
            #item.remove('}')
        
        
        
        
        
                         
    print str_name_list
    return str_name_list
    

        

        

                
        
def go():

    
    root = Tk()
    name_list = DisplaySpectrum(root)
    
    if name_list !='':
        normalize = True
        if normalize == True:
            kNorm = tkSimpleDialog.askfloat('normalization constant', 'norms')
            if kNorm == '':
                kNorm = 1
        else:
            kNorm = 1
               
        view_only = False
        if view_only:
            ConsolidateFiles(name_list, smooth = False)
            i = 5
            plot(arange(2800,3605,5),x[1], 'ks')
        
            plot(arange(2800,3605,5),SG_Smooth(x[1], width = 11,plot = False))
        else:
            
            ConsolidateFiles(name_list, smooth = True)
            SaveSpectrum(root, name_list, x)
    root.destroy()
    
    
    
    root.mainloop()   
    return None



class FittingWindow:
    
    
    def __init__(self, master):
        
        self.master  = master
        
        self.plotframe = Frame(master = self.master)
        self.plotframe.grid(row = 0, column = 0, columnspan = 20)
        
        self.frame = Frame(master = self.master)
        self.frame.grid(column = 1, rowspan = 10)
        
        self.fit_button = Tkinter.Button(master = self.master, command = self.fit_and_draw, width  = 5, text = 'FitNow')
        self.fit_button.grid(row = 3, column = 0)
        self.open_button =  Tkinter.Button(master = self.master, command = self.open_data, width  = 5, text = 'open')
        self.open_button.grid(row = 4, column = 0)
        self.open_ref_button =  Tkinter.Button(master = self.master, command = self.open_ref, width  = 5, text = 'Choose reference')
        self.open_ref_button.grid(row = 5, column = 0)
        
        self.open_bkg_button =  Tkinter.Button(master = self.master, command = self.open_bkg, width  = 5, text = 'Choose background')
        self.open_bkg_button.grid(row = 6, column = 0)
        
        self.ref_label =  Tkinter.Label(master = self.master, text = '')
        self.ref_label.grid(row = 7, column = 0)
        
        self.bkg_label =  Tkinter.Label(master = self.master, text = '')
        self.bkg_label.grid(row = 8, column = 0)
        
        self.smoothbutton = Tkinter.Button(master = self.master, command = self.smoothdata, width  = 5, text = 'Smooth')
        self.smoothbutton.grid(row = 9, column = 0)
        
        
        
        
        self.startfreq_text = Entry(self.master,width = 5)
        self.startfreq_text.insert(END,'2800')
        self.startfreq_text.bind("<Return>", self.update_limits)
        self.startfreq_text.grid(row = 1, column =0,sticky = W)
        self.startfreq = 2800
        
        self.endfreq_text = Entry(self.master,width = 5)
        self.endfreq_text.insert(END,'3600')
        self.endfreq_text.bind("<Return>", self.update_limits)
        self.endfreq_text.grid(row = 2, column =0,sticky = W)
        self.endfreq = 3600
        
        self.function_list = ['OneSFGwConstBkg',
                              'TwoSFGwConstBkg',
                              'TwoSFGwLinBkg',
                              'TwoSFGwAvgBkg',
                              'ThreeSFGwConstBkg',
                              'ThreeSFGwLinBkg',
                              'ThreeSFGwAvgBkg',
                              'FourSFGwLinBkg',
                              'SixSFGwLinBkg',
                              'FourSFGFixedParams']
        
        self.var_func = StringVar()
        self.var_func.set(self.function_list[0])
        
        
       
       
        self.MotorMenu = OptionMenu(self.frame,self.var_func, *self.function_list, command = self.init_function)
        self.MotorMenu.grid(row = 5,column =0,sticky = W)
        
        self.normalization_constant = 1
        self.scale_list = []
        self.var_list = []
        
        self.fig = Figure()
        self.ax1  = self.fig.add_subplot(111)
       
        self.canvas = FigureCanvasTkAgg(self.fig,master = self.plotframe)
        self.canvas.show()
        
        self.canvas._tkcanvas.pack(side=TOP, fill = BOTH,expand =True)
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.plotframe)
        self.toolbar.update()
        self.toolbar.pack(side= BOTTOM, fill = BOTH,expand =True)#,expand = True)#fill=BOTH)#, expand=1)
        #self.background = self.canvas.copy_from_bbox(self.a.bbox)

       
        self.background = (arange(2800,3605,5),ndarray((161,)))
        self.background[1][:] = 0
            
         
        self.reference = ndarray((161,))
        self.reference[:] = 1
        self.reference_name  = ''
        self.guess = list()
        if self.open_data() ==-1:
            tkMessageBox.showwarning("Open_data failed")
            self.name = ['']
            self.a = [arange(2800,3605,5), zeros(161)]
            self.raw = zeros(161)   
        
        if self.init_function(0) == -1:
            pass    
        
        
        self.update_limits(0)
        self.guessdraw(0)
        return None
        
        
       
        
        
        
        
        
    def init_function(self,functiontype):
        global function
        import inspect
        
        if functiontype == None:
            functiontype = self.var_func.get()
        
        self.functiontype = functiontype
        

#        self.func_dict={'TwoSFGwConstBkg':(lambda x,A1,A2,w1,w2,G1,G2,b: abs(b + A1/((x-w1)+j*G1) + A2/((x-w2)+j*G2))**2),
#                    'TwoSFGwLinBkg':(lambda x,A1,A2,w1,w2,G1,G2,m,b: abs(m*x/1000+b + A1/((x-w1)+j*G1) + A2/((x-w2)+j*G2))**2),
#                      'ThreeSFGwConstBkg': (lambda x,A1,A2,A3,w1,w2,w3,G1,G2,G3,b :  abs(b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2)+A3/((x-w3)+j*G3))**2),
#                      'OneSFGwConstBkg':(lambda x,A1,w1,G1,b:  abs(b + A1/((x-w1)+G1*j))**2)}
#       
                    
        if functiontype == 'OneSFGwLinBkg':
            def function(x,A1,w1,G1,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j))**2
             
        elif functiontype == 'TwoSFGwLinBkg':
            def function(x,A1,A2,w1,w2,G1,G2,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2))**2
         
        elif functiontype == 'ThreeSFGwLinBkg':
             def function(x,A1,A2,A3,w1,w2,w3,G1,G2,G3,m,b): return abs(abs(m*x/1000+b) + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2)+A3/((x-w3)+j*G3))**2
            
        elif functiontype == 'FourSFGwLinBkg':
            def function(x,A1,A2,A3,A4,w1,w2,w3,w4,G1,G2,G3,G4,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4))**2
               
        elif functiontype == 'SixSFGwLinBkg':
            def function(x,A1,A2,A3,A4,A5,A6,w1,w2,w3,w4,w5,w6,G1,G2,G3,G4,G5,G6,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4)+A5/((x-w5)+j*G5)+A6/((x-w6)+j*G6))**2
        elif functiontype == 'FourSFGFixedParams':
         
             w1= 2863
             
             w2= 2921
             w3= 2955
             
             w4= 2981
             G1=17
             G2=20
             G3=15
             G4=14
         
             def function(x,A1,A2,A3,A4,m,b): return abs(m*x/1000+b + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2) + A3/((x-w3)+j*G3)+ A4/((x-w4)+j*G4))**2

        elif functiontype == 'TwoSFGwAvgBkg':
             x = self.a[0][self.startidx:self.endidx+1]
             y = self.a[1][self.startidx:self.endidx+1]
             poly_param = polyfit(x,y,2)
             self.poly_bkg = poly_param[0]*x**2 + poly_param[1]*x + poly_param[2]
     
             def function(x,A1,A2,w1,w2,G1,G2): return abs(sqrt(self.poly_bkg) + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2))**2
   
        elif functiontype == 'ThreeSFGwAvgBkg':
             x = self.a[0][self.startidx:self.endidx+1]
             y = self.a[1][self.startidx:self.endidx+1]
             poly_param = polyfit(x,y,2)
             self.poly_bkg = poly_param[0]*x**2 + poly_param[1]*x + poly_param[2]
         
             def function(x,A1,A2,A3,w1,w2,w3,G1,G2,G3): return abs(sqrt(self.poly_bkg) + A1/((x-w1)+G1*j) + A2/((x-w2)+j*G2)+A3/((x-w3)+j*G3))**2
             
        else: 
             
             def function(x,A1): return abs(x*A1)
#==============================================================================
        self.w_name = list() 
        self.w_name = inspect.getargspec(function).args[1:]
        
        self.guess= []
       
        for w in self.w_name:
            if 'A' in w:
                self.guess.append(0.1)
            elif 'w' in w:
                self.guess.append(random.random()*200+2800)
            elif 'G' in w:
                self.guess.append(10)
            else:
                self.guess.append(0)
#================================================================================
        
        for i in range(len(self.scale_list),len(self.w_name)):
                self.scale_list.append(Scale(master  = self.frame,command = self.guessdraw))
                
        for i in range(len(self.w_name),len(self.scale_list)):
                self.scale_list[i].grid_forget()
           
        for i in range(len(self.w_name)):
                self.scale_list[i].config(label = self.w_name[i])
                self.scale_list[i].grid(row = 1, column = i + 3)
                
                if self.w_name[i][0] == 'A':
                     self.scale_list[i].config(from_ =-5, to =  5,resolution = 0.1)
                     self.scale_list[i].set(1)
                elif self.w_name[i][0] == 'w':
                    self.scale_list[i].config(from_ = self.startfreq-20, to =  self.endfreq+20,resolution = 1)
                    self.scale_list[i].set(2800)
                elif self.w_name[i][0] == 'G':
                    self.scale_list[i].config(from_ = 1, to =  100)
                    self.scale_list[i].set(15)
                elif self.w_name[i][0] == 'm':
                    self.scale_list[i].config(from_ = -1, to =  1, resolution = 0.05)
                    self.scale_list[i].set(0)
                elif self.w_name[i][0] == 'b':
                    self.scale_list[i].config(from_ = -1, to =  1, resolution = 0.05)
                    self.scale_list[i].set(0)
                else:
                    print "Variable not recognized:", self.w_name[i] 
        return 0
        
        
    def smoothdata(self):
        self.a[1] = SG_Smooth(self.a[1])
        self.guessdraw(0)
        return 0
        
        
    def update_limits(self,extra):
        functiontype = self.var_func.get()
        
        self.startfreq = int(self.startfreq_text.get())
        
        self.endfreq = int(self.endfreq_text.get())
        self.startidx = (abs(self.a[0]-self.startfreq)).argmin()
        self.endidx = (abs(self.a[0]-self.endfreq)).argmin()
        if functiontype == 'ThreeSFGwAvgBkg' or functiontype == 'TwoSFGwAvgBkg':
            x = self.a[0][self.startidx:self.endidx+1]
            y = self.a[1][self.startidx:self.endidx+1]
            poly_param = polyfit(x,y,2)
           
            self.poly_bkg = poly_param[0]*x**2 + poly_param[1]*x + poly_param[2]
           
        
        self.guessdraw(0)
        return 0
            
    def open_data(self): 
        
        self.name = DisplaySpectrum(root)
        
        if self.name == None:
            return -1
        self.a = OpenSFG(self.name)
        
        self.raw = array(self.a[1],copy = True)
        
        
        self.update_limits(0)
       
       
    
        self.guessdraw(0)    
        
        return 0
    
    def open_ref(self):
        self.reference_name = DisplaySpectrum(root)
        if self.reference_name == None:
            self.ref_label.config(text = self.name)
            self.reference = ndarray((161,))
            self.reference[:] = 1
            return 0
        self.reference = OpenSFG(self.reference_name,channel = 'AvgIR')[1]
        
        
        
        self.reference[:] = SG_Smooth(self.reference[:], width = 101, order = 3,plot_val = False)
        
        self.ref_label.config(text = self.name[0][-12:-4])
        self.recalc_data()
        self.guessdraw(0)
        
        return 0 
        
    def open_bkg(self):
        self.name = DisplaySpectrum(root)
        if self.name == None:
            self.bkg_label.config(text = self.name)
            self.background = (arange(2800,3605,5),zeros((161,)))
            
            return 0
        self.background = OpenSFG(self.name,channel = 'AvgSFG')
        self.ax1.cla()
        
        self.background[1][:] = SG_Smooth(self.background[1][:], width = 101, order = 3)
        self.bkg_label.config(text = self.name[0][-12:-4])
        return 0 
        
            
        
    def recalc_data(self):
        if self.raw.shape == self.reference.shape:
            self.a[1] = SG_Smooth(self.raw,width = 11,order = 3)/self.reference/self.normalization_constant
            self.ax1.cla()
            plot(self.a[0],self.raw/self.reference)
            plot(self.a[0],self.a[1])
        else:
            print "reference invalid"
            self.reference_name = "No IR Reference"
            
            self.ax1.cla()
            self.ax1.plot(self.a[0],self.a[1])
            self.canvas.draw()
        return 0
        

    def guessdraw(self,ex):
        global function
        
    
        
        x = self.a[0][self.startidx:self.endidx+1]
       
      
        for i in range(len(self.guess)):
            self.guess[i] = self.scale_list[i].get()

        self.ax1.cla()
        self.ax1.plot(self.a[0],self.a[1])
  
        
        self.ax1.plot(x,function(x,*self.guess))
        self.canvas.draw()
           
       
        return 0
    def fit_and_draw(self):
        
        global function
        
        x = self.a[0][self.startidx:self.endidx+1]
        y = self.a[1][self.startidx:self.endidx+1]
       
        try:
            result = optimize.curve_fit(function,x,y,self.guess)
        except RuntimeError:
            tkMessageBox.showerror('Fit Failed')
            return 0
        self.ax1.cla()
        self.ax1.plot(self.a[0],self.a[1])
        z = list(result[0])
        self.ax1.plot(x,function(x,*z))
        
        for i in range(len(self.w_name)):
            #self.scale_list[i].set(result[0][i])
            if "w" in self.w_name[i]:
                axvline(x = z[i], ymin = 0, ymax = 1 ,color = 'r')
        self.canvas.draw()         
        
       
      
             
        print "Result Found for" , self.name
        print "Referenced to IR spectrum" , self.reference_name
        print "Normalized by constant", self.normalization_constant
        for i in range(len(self.w_name)):
        
            print self.w_name[i], result[0][i]
        
                
        
        return 0
        
def fits():
    global root 
    ioff()    
    root = Tk()
    FittingWindow(root)

    root.mainloop()
    return None

  
def measure_back():
    import os
    
    
   
    list_of_constants = []
    name_list = [u'C:/Users/Chris/My Documents/Data/130627/13062701.csv',
                 u'C:/Users/Chris/My Documents/Data/130628/13062802.csv',
                 u'C:/Users/Chris/My Documents/Data/130702/13070203.csv',
                 u'C:/Users/Chris/My Documents/Data/130703/13070302.csv']
    ref_list = ['C:/Users/Chris/My Documents/Data/130627/13062707.csv',
                'C:/Users/Chris/My Documents/Data/130628/13062801.csv',
                'C:/Users/Chris/My Documents/Data/130702/13070202.csv',
                'C:/Users/Chris/My Documents/Data/130703/13070301.csv']
    leg_list = ()
    for i in range(4):
        #os.chdir("C:/Users/Chris/My Documents/Data/"+item)
        #print 'choose IR for', item
        #name = DisplaySpectrum(root)
        (x,y) =  OpenSFG(name_list[i],channel = 'AvgSFG')    
        reference = OpenSFG(ref_list[i],channel = 'AvgIR')[1]    
        y[:] = SG_Smooth(y[:], width = 13, order = 3,plot = False)          
        reference[:] = SG_Smooth(reference[:], width = 101, order = 3,plot = False)
        y[:]/= reference[:]
        plot(x,y)
        leg_list+=(name_list[i][33:39],)
        
        
        
        
        #print 'choose d2o reference for ', item
        #name = DisplaySpectrum(root)
        #d2o_spec = OpenSFG(name,channel = 'AvgSFG')[1]              
        list_of_constants.append(mean(y))
    print list_of_constants
    legend(leg_list)
    
    return 0
       

                                                

                                                   
def OpenSpectrum_flat(file_name, channel = 'AvgSFG'):
   
    if channel == 'AvgSFG':
        chan_no = 1
    elif channel == 'AvgIR':
        chan_no = 2
    
    
    if file_name == []:
        
        return -1
    if  type(file_name) is list:
        file_name = file_name[0]
    
    a = loadtxt(file_name,
            dtype = float, 
            delimiter = ',',
            skiprows = 1,
            unpack  = True)
   
    return a                                           

                                            
def TimeSeries(filename,width = 1,interval = 5, _plot = True,smooth = True,_from = 0, to = -1, _legend = True):
    
    legend_list = list()   
      
    
    time_series_spec = OpenSpectrum(filename).Array[:,:,0]
    freq = time_series_spec[0,_from:to]
    return_val = [freq]
    size= time_series_spec.shape[0]-1
    
    averaged = ndarray((0,26))
    for i in range(2,size+2-width,interval):  # start with 2, becuase first column is average
        
        
        
        ys =  mean(time_series_spec[i:i+width,_from:to], axis = 0)
        
        if smooth == True:
            ys = SG_Smooth(ys)
        return_val.append(ys)
        if i > 20:
            char_str = 's'
        else: 
            char_str = '-'
        if _plot == True:
            plot(freq,ys,char_str,label = str(i))
            legend_list.append(str(i-1))
    if _legend ==True:
        gca().legend(legend_list)
    
    return return_val
                
def OpenSpectrum(file_name, old_way = True):#def OpenSpectrum():
     # opens a spectrum from data in "file_name" and returns a SpectrumArray instance.
     if old_way:
         with open(file_name,"rb") as f:
                     
                 CSV_READER = csv.reader(f)
         
                 rownum = 0
                 s =0
                 for row in CSV_READER:
                         if rownum == 0:
                                 rownum = 1
                         else:
                             
                             
                                 temp_array = numpy.array([])
                                 for i in range(len(row)):
                                     
                                         temp_array = numpy.append(temp_array,float(row[i]))
                                         if i == 0:
                                                  temp_array = numpy.append(temp_array,[0,0,0])
                                    
                                 temp_array = temp_array.reshape((-1,4))
                             
                             
                     
                                 if s == 0 :
                                         array = temp_array
                                         s=1
                             
                                 else:
                                         array = numpy.append(array,temp_array,axis = 1)
                                       
                 
                
                 c = 4
                 a = (temp_array.shape[0])
                 
                         
                         
                 input_array = numpy.reshape(array,(a,-1,c))
     else:
         input_array = numpy.loadtxt(file_name,delimiter = ',', skiprows = 1 )
         for i in range(3):
             
             input_array = numpy.insert(input_array,0,input_array[:,0],axis = 1)
         
         size_tuple = (input_array.shape[0], -1, 4)
         
         input_array = numpy.reshape(input_array,size_tuple)
           
    
     
     SpecArray = SpectrumArray(startfreq = input_array[0,0,0],endfreq = input_array[0,-1,0],stepsize =input_array[0,1,0]-input_array[0,0,0], name = file_name[-12:-4])
     SpecArray.Array = input_array

     SpecArray.FilePath = os.path.abspath(file_name)
     SpecArray.Directory = os.path.dirname(SpecArray.FilePath)
   
    
     return SpecArray


def SaveSpectrum(Array,file_name):
        
        # Saves data from a SpectrumArray object into a csv file.  
        import csv
        
                
         
                        
        
        try:
                with open(file_name,"wb") as f:
                        CSV_FILE = csv.writer(f,dialect = 'excel')
                        header_list = []
                        header_list.append('Freq')
                        header_list.append('AvgSFG')
                        header_list.append('AvgIR')
                        header_list.append('TotSTDEV')
                        header_list.append('AvgNORM')
                        for column in range(Array.shape[0]-2):
                            
                                header_list.append('SFG_'+str(column+1))
                                header_list.append('IR_'+str(column+1))
                                header_list.append('STDEV_'+str(column+1))
                                header_list.append('NORM_'+str(column+1))
                        
                        CSV_FILE.writerow(header_list)
                        for row in range(Array.shape[1]):
                                flat = Array[:,row,:].flatten()[3:]
                                
                                CSV_FILE.writerow(flat)
                       
                    
                    
                    
                        f.close()

                                
                       
        except IOError:
                CallError(SPECTRUM_SAVE_ERROR)
                return SPECTRUM_SAVE_ERROR
               
    
        return 0
        
        


