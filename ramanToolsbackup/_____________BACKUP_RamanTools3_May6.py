# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 11:37:39 2014

@author: chris
"""


import numpy
from numpy import *
import scipy.optimize
import pandas
from Tkinter import *
import Tkinter
import tkFileDialog, tkSimpleDialog, tkMessageBox
from matplotlib.pyplot import *
from matplotlib.axes import *
from SFGMeFiles import SFG_Notebook
import time
from copy import copy

import matplotlib.figure 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import csv, os
pandas.options.display.mpl_style = None# 'default'


import pdb
from matplotlib.widgets import SpanSelector
from collections import deque
from matplotlib.colors import ColorConverter

import RamanTools.FittingWindow
from RamanTools.RamanSpectrum import *

colordict= ColorConverter()

list_of_display_windows = []

def RGBtohex(rgbtuple): return '#%02x%02x%02x'%  (rgbtuple[0]*255,rgbtuple[1]*255,rgbtuple[2]*255)

class RamanSpectrum(pandas.Series):

    def __init__(self,filename,avg = True):
        
      
        if filename.__class__ == pandas.Series:
           
            obj = pandas.Series.__init__(self,filename.values,array(filename.index))
            self.info = str()
            self.num_frames = 0
            self.accum_time = float()
            
            
        elif filename[-4:] == '.SPE' or filename[-4:] == '.spe':
            
                
                fid = File(filename)
                fid._load_size()
                x_offset = fid.read_at(3103, 1, float64)
                a = fid.read_at(3263, 6, float64)# wavelengths in nm
                wl = fid.read_at(3311,1, float64)  ## laser wavelength
                spectrum = fid.load_img()
                
                if avg== True:
                    
                    if fid._numframes>1:
                        
                        spectrum=sum(spectrum,axis=0)
                        spectrum=spectrum.flatten()
                    elif fid._numframes==1:
                        spectrum=spectrum.flatten()
                        

                a = list(a)
                a.reverse()
                a = polyeval(a,arange(len(spectrum))+x_offset)
                a = -(1E7/a-1E7/wl)
                
                
                obj = pandas.Series.__init__(self,spectrum,a)
                self.info = fid.get_info()
                self.accum_time=fid.get_accum_time()
                self.num_frames = fid._numframes
                self.name = filename
                fid.close()
            
        else:    
            try:
                a= loadtxt(filename,
                          delimiter = ',',
                          usecols = (0,1),
                          unpack = True)
                
            except:
                try:
                    a= loadtxt(filename,
                              delimiter = '\t',
                              usecols = (0,1),
                                unpack = True)

                  
                except:
                    try:
                        a= loadtxt(filename,
                                  delimiter = '\t',
                                  usecols = (0,1),
                                    skiprows = 35,
                                    unpack = True)
    
                      
                    except:
                        obj = pandas.Series.__init__(self,array([0]),array([0]))
                        self.info = str()
                        self.accum_time=-1
                        self.num_frames = -1
                        self.name = filename
                        print 'error opening Raman Spectrum File', filename
                        return obj
            
            if any(abs(diff(a[0]))>100):   
                    cutoff = argmax(abs(diff(a[0])))
                    a[1][0:cutoff] = (a[1][0:cutoff]+a[1][cutoff:cutoff*2])/2
                    a = a[:,0:cutoff]
                    
            else:
                    cutoff = a[1].size
                        
 
            obj = pandas.Series.__init__(self,a[1],a[0],dtype = float)#pandas.Series.__init__(self,a[1][0:cutoff],a[0][0:cutoff],dtype = float)
            self.info = str()
            self.accum_time=-1
            self.num_frames =-1
            self.name = filename
        
        return obj
        
    def __array_finalize__(self,obj):
        if obj is None: return
   
        
    def closest_x(self,x): return argmin(abs(array(self.index)-x))
        
        
    def smooth(self,window_len=3,window='flat'):
        
        
        self[:] = smooth(self,window_len=window_len,window=window)
       
        
        return 0

        
    def set_name(self,filename):
        self.name = filename
        return 0

    
    def nearest(self, x):
        return argmax(diff((array(self.index)-x)>0))
        
    def _copy(self):
        
       
        r = copy.deepcopy(self)
        r.set_name(self.name)
        r.info = self.info
        r.accum_time=self.accum_time
        r.num_frames =self.num_frames
    
        
        return r
        
    def calc_noise(self,rnge,rnge_type = 'data'):
        return calc_noise(self,rnge,rnge_type = rnge_type)
        
    def calc_area(self,rnge):
        return calc_area(self,rnge)

    def autobaseline(self,rnge,order = 1,specialoption = None):
        autobaseline(self,rnge,order = order,specialoption = specialoption)   
        return 0


class DisplayWindow(object):
        global CdMeOTPRef, MeOTPRef
        color_list = deque(['b','g','r','c','m','y','k'])
        current_checker = None
        

        def __init__(self, master):
                
                self.rootref = master
                self.master = Toplevel()
                        
                        
                self.frame = Frame(master = self.master)
                self.Plot = Figure()#, width = 1, height = 3)               
                self.channel_list = []
                self.array_list = []
                self.Plot.a  = self.Plot.add_subplot(111)
                self.Plot.a.set_xlabel('Raman Shift (cm$^{-1}$)')
                self.Plot.a.set_ylabel('Intensity (a.u.)')
                self.Plot.a.legend([])
                self.Plot.a.get_legend().set_visible(False)
                self.checker_list = self.Plot.a.lines
                self.legend_var = IntVar()
                self.legend_var.set(1)
                self.legendbox = Checkbutton(self.frame,
                                       variable=self.legend_var,
                                       command=self.update_legend)
                
                
                
                self.statusbar = Label(self.master, bd=1, relief=SUNKEN, anchor=W)
                self.statusbar.config(text = "Ready")
                
                
                
 
                self.canvas = FigureCanvasTkAgg(self.Plot,master = self.frame)
                self.canvas.show()
                
               
                
                self.master.protocol("WM_DELETE_WINDOW", self.quitproc)

               
                self.master.title(string = "RamanViewer")
                self.checker_frame=Frame(master = self.master, width =500)
                
                self.menubar = Menu(self.master)
                
                self.filemenu = Menu(self.menubar, tearoff=0)
                self.filemenu.add_command(label="New window", command = lambda: DisplayWindow(self.rootref))
                self.filemenu.add_command(label="Open", command = self.DisplaySpectrum)
                self.filemenu.add_command(label="Save",command = self.SaveSpectrum)
                self.filemenu.add_command(label="SaveFig",command = self.SaveFigure)
                self.filemenu.add_command(label="ViewNotebook",command = self.ViewNotebook)
                self.filemenu.add_command(label="Exit", command = self.quitproc)
                self.menubar.add_cascade(label="File", menu=self.filemenu)
                # create more pulldown menus
                self.editmenu = Menu(self.menubar, tearoff=0)
                self.editmenu.add_command(label="Smooth", command = self.SmoothSpectrum)
                self.filemenu.add_command(label="Fitting window", command = lambda:RamanTools.FittingWindow.FittingWindow(Toplevel(),ramanspectrum=self.current_checker.spectrum))#, kwargs = {'ramanspectrum':self.current_checker.channel.spec_array})
                self.editmenu.add_command(label="Calc Noise", command = self.start_calc_noise)
                self.editmenu.add_command(label="Calc Area", command = self.start_calc_area)
                self.editmenu.add_command(label="Basline", command = self.start_autobaseline)
                self.editmenu.add_command(label="disconnect", command = self.disconnect)
                self.editmenu.add_command(label='Quick Scan',command = self.open_next_spectrum_in_folder)
                self.editmenu.add_command(label='Normalize All',command = self.normalizeall)
                self.editmenu.add_command(label='Zero All',command = self.zeroall) 
                self.editmenu.add_command(label = 'FFT process', command=self.FFT)
                self.editmenu.add_command(label = 'Remove noise', command = self.removenoise)
                self.editmenu.add_command(label="Copy")
                self.editmenu.add_command(label="Paste")
                self.menubar.add_cascade(label="Edit", menu=self.editmenu)
                
                self.correctionmenu = Menu(self.menubar,tearoff=0)
                self.correctionmenu.add_command(label='SPID633', command = self.SPIDcorrect633)
                self.correctionmenu.add_command(label='SPID785', command = self.SPIDcorrect785)
                
                self.menubar.add_cascade(label = 'Corrections', menu = self.correctionmenu)
                
                self.notesmenu =Menu(self.menubar, tearoff=0)
                self.notesmenu.add_command(label = "Notes", command = self.ViewNotebook)
                self.notesmenu.add_command(label = "Spectrum Info", command = self.showinfo)
                self.menubar.add_cascade(label = 'Info', menu = self.notesmenu)
                
                self.refsmenu =Menu(self.menubar, tearoff=0)
                self.refsmenu.add_command(label = "chloroform", command = None)
              
                self.refsmenu.add_command(label = "CdMeOTP", command = lambda:self.AddChannel(CdMeOTPRef))
                self.refsmenu.add_command(label = "MeOTP", command = lambda:self.AddChannel(MeOTPRef))
                self.refsmenu.add_command(label = "CdODPA", command = lambda:self.AddChannel(CdODPARef))
                self.refsmenu.add_command(label = "toluene", command = lambda:self.AddChannel(tolueneRef))
                self.menubar.add_cascade(label = 'References', menu = self.refsmenu)
                
                
                self.master.config(menu= self.menubar)
                
                self.frame.pack(side=TOP, expand = 1, fill = BOTH)#(row = 0, column = 0, padx = 25, pady = 25)
                self.legendbox.pack(side=BOTTOM)
                self.statusbar.pack(side = BOTTOM)
                self.checker_frame.pack(side=BOTTOM,expand = 1)#(row=1,column=0)
                self.canvas._tkcanvas.pack(side=TOP, expand = 1, fill = BOTH)
                self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
                self.toolbar.update()
                self.toolbar.pack(side= BOTTOM,expand =True)
                self.canvas.draw()
                
                list_of_display_windows.append(self)
                              
                return None
        
        def update_legend(self):
            
            if self.legend_var.get() == 0:
                self.Plot.a.get_legend().set_visible(False)
            else:
                l = list()
                for entry in self.checker_list:
                    if True:#entry.get_visible():
                        l.append(entry.commentbox.get())
                        self.Plot.a.legend(l)
                   
          
            self.Plot.canvas.draw()
            return 0
        def showinfo(self):
            tkMessageBox.showinfo('Spectrum info',self.current_checker.spectrum.info)
            return 0
            
        def getcolor(self): 
            self.color_list.rotate(1)
            return self.color_list[0]
                
       
        def DisplaySpectrum(self):
            import re
            options = {}
            #options['defaultextension'] = '.SPE'
            options['filetypes'] = [('all files','.*'),('SPE','.spe'),('txt', '.txt'),('csv','.csv')]
            options['multiple'] = True
            options['title'] = 'Open Spectrum...'
            options['parent'] = self.master
         
            str_name_list = tkFileDialog.askopenfilenames(**options)
           
            if type(str_name_list) == tuple:
                for name in str_name_list:
                    if 'notes' in name:
                        SFG_Notebook.SFG_NotebookWindow(target_file = name)
                    elif name =='':
                        continue
                    else:
                        newspectrum = RamanSpectrum(name)                            
                        self.Plot.a.add_line(checker(self,newspectrum,color = self.getcolor()))
                        self.Plot.a.relim()
                        self.Plot.a.autoscale_view(tight = False)
                        self.Plot.canvas.draw()
                        self.current_checker = self.Plot.a.lines[-1]
            elif str_name_list == '':
                    return 0
            elif type(str_name_list) == list:
                for name in re.split(' ',str_name_list):
                    newspectrum = RamanSpectrum(name)
                    self.Plot.a.add_line(checker(self,newspectrum,color = self.getcolor()))
                    self.Plot.a.relim()
                    self.Plot.a.autoscale_view(tight = False)
                    self.Plot.canvas.draw()
                    

                    self.current_checker = self.Plot.a.lines[-1]
                       
            os.chdir(os.path.dirname(str_name_list[0]))
               
            return 0

        def SaveSpectrum(self):
                
                file_opt = options = {}
                options['defaultextension'] = '.txt'
                options['filetypes'] = [('all files', '.*')]
                
                options['title'] = 'Open Spectrum...'
                options['initialfile'] = os.path.basename(self.current_checker.name)
                options['parent'] = self.master

                if self.current_checker  == None:
                        return 0
                str_filename = tkFileDialog.asksaveasfilename(**options)
               
                if str_filename == '':
                        return 0
                else:
                        data = transpose([self.current_checker.get_xdata(),self.current_checker.get_ydata()])
                        
                        savetxt(str_filename,data,delimiter = ',',comments = '#'+str(self.current_checker.spectrum.info))#SaveSpectrum(self.current_checker.channel.spec_array,str_filename)
                os.chdir(os.path.dirname(str_filename))
                return 0
        def ViewNotebook(self):
           
                SFG_Notebook.SFG_NotebookWindow(target_dir = os.listdir(os.path.dirname(self.current_checker.name)))
               
                return 0 
        def zeroall(self):
                for c in self.Plot.a.lines:
                    c.set_ydata(c.get_ydata()-min(c.get_ydata()))
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.Plot.canvas.draw()
                return 0
                
                        
        def SmoothSpectrum(self):

                if self.current_checker == None:
                    return 0
                newspectrum = smooth(self.current_checker.spectrum)
                                                        
                self.Plot.a.add_line(checker(self,newspectrum,color = self.getcolor(),operations = 'sp = smooth(sp)\n'))
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.Plot.canvas.draw()
                self.current_checker = self.Plot.a.lines[-1]
                
      
                return 0
        def SPIDcorrect785(self):
            if self.current_checker == None:
                return 0
            else:
                newspectrum = SPIDcorrect785(self.current_checker.spectrum)
                                                        
                self.Plot.a.add_line(checker(self,newspectrum,color = self.getcolor(),operations = 'sp = SPIDcorrect785(sp)\n'))
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.Plot.canvas.draw()
                self.current_checker = self.Plot.a.lines[-1]
                
  
            return 0
        def SPIDcorrect633(self):
            if self.current_checker == None:
                return 0
            else:
                newspectrum = SPIDcorrect633(self.current_checker.spectrum)
                                                        
                self.Plot.a.add_line(checker(self,newspectrum,color = self.getcolor(),operations = 'sp = SPIDcorrect633(sp)\n'))
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.Plot.canvas.draw()
                self.current_checker = self.Plot.a.lines[-1]
                
  
            return 0
        def open_next_spectrum_in_folder(self):
                self.Plot.canvas.mpl_connect('key_press_event',self.open_next_spectrum)
                for c in self.checker_list[1:]:
                    self.RemoveSpectrum(self.checker)
                self.checker_list[0].set_current(0)
                
                return 0
        def open_next_spectrum(self,event):
                
                directory_index = os.listdir(os.path.dirname(os.path.abspath(self.current_checker.channel.spec_array.name)))
                for x in directory_index:
                    if 'txt' not in x:
                        directory_index.remove(x)
                directory_index.sort()
                i=directory_index.index(os.path.basename(self.current_checker.channel.spec_array.name))

                if i>len(directory_index)-2:
                    i=-1
                if 'txt' not in directory_index[1+1]:
                    i+=1
                if event.key == 'right':
                    i+=1
                elif event.key == 'left':
                    i-=1

                try:
                    newspectrum = RamanSpectrum(directory_index[i])
                except:
                    print 'error'
                    print 'i=',i
                    
                    return -1
                self.RemoveSpectrum(self.current_checker)
                self.AddChannel(self.newspectrum)
               
                self.checker_list[0].set_current(0)
                return 0
                
                
        def normalizeall(self):
            for check in self.checker_list:
                data = check.get_ydata()
                data[:]-=min(data)
                data/=max(data)
                check.set_ydata(data)
            self.Plot.a.relim()
            self.Plot.a.set_ylim(-0.5,1.5)
            self.Plot.a.autoscale_view(tight = False)
            self.Plot.canvas.draw()
            return 0
                
        def start_calc_noise(self):
              
                self.span = SpanSelector(self.Plot.a, self.calc_noise, 'horizontal')
                self.span.connect_event('pick_event',self.calc_noise)
                gcf().canvas.mpl_connect('button_press_event',self.disconnect)
                return 0
        def start_calc_area(self):
               
                self.span = SpanSelector(self.Plot.a, self.calc_area, 'horizontal')
                self.span.connect_event('pick_event',self.calc_area)
                gcf().canvas.mpl_connect('button_press_event',self.disconnect)
                
                return 0
        def start_autobaseline(self):
                
                self.span = SpanSelector(self.Plot.a, self.autobaseline, 'horizontal')
                self.span.connect_event('pick_event',self.autobaseline)
                gcf().canvas.mpl_connect('button_press_event',self.disconnect)
                
                return 0
        def autobaseline(self,start,end):
                order = int(tkSimpleDialog.askinteger('Fit order', 'Choose the polynomial order.'))
                if order == None:
                    return 0
                if self.current_checker == None:
                    return 0
                newspectrum = autobaseline(self.current_checker.spectrum,(start,end),order = order)
                                                        
                self.Plot.a.add_line(checker(self,newspectrum,color = self.getcolor(),operations = 'sp = autobaseline(sp), ('+str(start)+','+str(end)+'), order ='+str(order)+')\n'))
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.Plot.canvas.draw()
                self.current_checker = self.Plot.a.lines[-1]
                self.span.disconnect_events()
                
                return 0
                
        def calc_noise(self,start,end):
                try:
                    print "STD =", calc_noise(pandas.Series(self.current_checker.channel.get_ydata(),self.current_checker.channel.get_xdata()),(start,end))
                 
                except:
                    print 'error'
                return 0
        def calc_area(self, start,end):
                try:
                    print "Area =", calc_area(pandas.Series(self.current_checker.channel.get_ydata(),self.current_checker.channel.get_xdata()),(start,end)) 
                except:
                    print 'error'
                return 0
        def disconnect(self):
            #print event.button#gcf().canvas.mpl_disconnect(self.cid)
            self.span.disconnect_events()
            return 0
        def removenoise(self):
            newspectrum = removecorrelatednoise(self.current_checker.spectrum)
                                                        
            self.Plot.a.add_line(checker(self,newspectrum,operations = 'sp = removecorrelatednoise(sp)',color=self.getcolor()))
            self.Plot.a.relim()
            self.Plot.a.autoscale_view(tight = False)
            self.Plot.canvas.draw()
            self.current_checker = self.Plot.a.lines[-1]
            return None


                
        def AddChannel(self,spectrum):
                
                
                self.Plot.a.add_line(checker(self,spectrum))
                self.Plot.a.lines[-1].set_color(self.getcolor())
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.Plot.canvas.draw()
                self.current_checker = self.Plot.a.lines[-1]
                return 0 

       

        def RemoveSpectrum(self,checker):
                
                
                self.Plot.a.lines.remove(checker)
                self.Plot.a.relim()
                self.Plot.a.autoscale_view(tight = False)
                self.canvas.draw()
                checker.frame.pack_forget()
                return 0   
                
        def SaveFigure(self):
                os.chdir('/home/chris/Desktop')
                self.Plot.savefig('figure.png')
                f = open('/home/chris/Desktop/figure.py','wb')
                for line in self.Plot.a.lines:
                    f.write(line.operations)
                f.close()
                return 0
        def FFT(self):
                return 0
                
        def quitproc(self):
                self.master.destroy()
                list_of_display_windows.remove(self)
                if len(list_of_display_windows)==0:
                   self.rootref.destroy() 
                return 0



                                             
class checker(matplotlib.lines.Line2D):
        
        def __init__(self,master,ramanspectrum,operations = '',*args,**kwargs):
                self.master = master
                self.spectrum = ramanspectrum  
                self.name = ramanspectrum.name
                self.frame = Frame(master = self.master.checker_frame)
                self.frame.pack(side=BOTTOM)
                matplotlib.lines.Line2D.__init__(self,ramanspectrum.index,ramanspectrum.values,*args,**kwargs)
                                 
                                            
                self.visible_var = IntVar()
                self.visible_var.set(1)
                self.box = Checkbutton(self.frame,
                                       variable=self.visible_var,
                                       command=self.change_visible)
                
                
                
                self.DeleteButton = Tkinter.Button(self.frame,
                                        text = "Delete",
                                        command = lambda: self.master.RemoveSpectrum(self),
                                        width=5,
                                        height=1)
                
                self.NameLabel =  Label(self.frame, height = 1, width=20,text = ramanspectrum.name[-30:])
                self.NameLabel.bind("<Button-1>",self.set_current)
                
                self.commentbox = Entry(master = self.frame, width = 20)
                
                self.box.pack(side=LEFT)#grid(row=0,column = 5)
                self.DeleteButton.pack(side=LEFT)#(row=0,column = 7)
                self.commentbox.pack(side=LEFT)#.grid(row = 0, column = 6)
                self.NameLabel.pack(side=RIGHT)#.grid(row=0,column = 1)
                
                self.operations = str('sp = RamanSpectrum('+self.name+')\n'
                                +operations)
              
                w = Canvas(master = self.frame,width = 20,height=20)
                w.pack(side = LEFT,padx=10)
               
                fillcolor = RGBtohex(colordict.colors[self.get_color()])
                
                w.create_rectangle(0,0,100,100,  fill=fillcolor)
                
               
                
                return None
        
                 
        def set_current(self,event):
                self.master.current_checker = self
                for c in self.master.checker_list:
                    if c == self.master.current_checker:
                        c.NameLabel.config(relief = SUNKEN)
                    else:
                        c.NameLabel.config(relief = FLAT)
                self.master.statusbar.config(text = self.name)
                
                
                return 0 
                
                
        def change_visible(self):
                
                if self.visible_var.get() == 0:
                        self.set_visible(False)
                else:
                        self.set_visible(True)
                self.master.Plot.a.relim()
                self.master.Plot.a.autoscale_view(tight = False)
                self.master.Plot.canvas.draw()
                
                return 0
       
       
                      
      
       

def SGsmooth(x,y, width=11,order = 2):#data,rnge,rnge_type = 'data'):
    
    retval = ndarray(y.shape)

    for i in range(y.size):

        i_min = max(0,i-width/2)
        i_max = min( i+width/2-1, y.size)
        fit = polyfit(x[i_min:i_max+1],y[i_min:i_max+1],order)
        retval[i] = polyeval(fit,x[i])
    return retval


def polyeval(constants,x):
    n = 0 
    for i in range(len(constants)):
       
        n+= constants[i]*x**(len(constants)-i-1)
    return n
    
def add_RamanSpectra(_x,_y):
    
    xmax = min(max(array(_x.index)),max(array(_y.index)))
    xmin = max(min(array(_x.index)),min(array(_y.index)))
   
    _x2 = _x.truncate(xmin,xmax)
    _y2 = _y.truncate(xmin,xmax)
    _y2 = _y2.reindex(_x2.index,method = 'ffill')
    
    output = _x2+_y2
    if any(output.isnull()):
        output = output.fillna(method = 'bfill')
    
    return RamanSpectrum(output)
    
    

    
    
def FourierFilter(input_array,width =900,demo = False):
    

    
    r = fft.fft(input_array)
    if demo == True:
        plot(1/input_array.index,r.real)
        plot(r.imag)
        vlines(1/(r.size/2-width),0,100)
        vlines(1/(r.size/2+width),0,100)

    r[r.size/2-width:r.size/2+width]=0
    s = fft.ifft(r).real
    output = pandas.Series(s,array(input_array.index))
    if demo==True:
        pass
    
    

    return RamanSpectrum(output)
    
    
def calc_area(spectrum,rnge):
    start = spectrum.nearest(rnge[0])#argmin(abs(array(spectrum.index)-rnge[0]))
    end = spectrum.nearest(rnge[1])#argmin(abs(array(spectrum.index)-rnge[1]))+1
 
    xs = array(spectrum.index[start:end])
    ys= spectrum.values[start:end]
    try:
        slope =(ys[-1]-ys[0])/(xs[-1]-xs[0])
        baseline = slope*(xs-xs[0])+ys[0]
    except:
        print 'error'
        print ys,xs, start, end
        return 0
        
    
    return sum((ys-baseline)[1:]*diff(xs))
    
def autobaseline(spectrum,rnge,order = 0,join=None,leaveout=None,specialoption = None):
    spectrum = copy(spectrum)
    start = spectrum.nearest(rnge[0])#argmin(abs(array(spectrum.index)-rnge[0]))
    end = spectrum.nearest(rnge[1])#argmin(abs(array(spectrum.index)-rnge[1]))+1
    
    if start == end:
        return spectrum
    xs = array(spectrum.index[start:end])
    ys= spectrum.values[start:end]
    if leaveout!=None:
        print 'leaving out', leaveout
        lo_start = spectrum.nearest(leaveout[0])
        lo_end = spectrum.nearest(leaveout[1])
        xfits = delete(xs,range(lo_start,lo_end))
        yfits = delete(ys,range(lo_start,lo_end))
        
    else:
        xfits = xs
        yfits = ys

    if order == 0:
        slope =(yfits[-1]-yfits[0])/(xfits[-1]-xfits[0])
        b = yfits[0]-slope*xfits[0]
        baseline = slope*(xs)+b
        spectrum.values[start:end] = spectrum.values[start:end]-baseline
    else:

        r = polyfit(xfits,yfits,order)
        spectrum.values[start:end] = spectrum.values[start:end]-polyeval(r,xs)
    if join == 'start':
        offset = spectrum.iloc[start]-spectrum.iloc[start-1]
        print start, start-1, offset
        spectrum.values[start:] -= offset
    elif join == 'end':
        offset = spectrum.iloc[end+1]-spectrum.iloc[end]
        spectrum.values[end:] -= offset
    else:
        pass
    return spectrum
    


def smooth(spectrum,window_len=3,window='flat'):
    
    spectrum =copy(spectrum)
    if spectrum.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if spectrum.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return spectrum
 
    if not window in ['flat','SG']:
        raise ValueError, "Window is on of 'flat', 'SG"


    s=r_[spectrum.values[window_len-1:0:-1],spectrum,spectrum.values[-1:-window_len:-1]]
   
    if window == 'SG':
        order = 2
        y=spectrum.values
        x=array(spectrum.index)
        retval = ndarray(y.shape)
        for i in range(y.size):

            i_min = max(0,i-window_len/2)
            i_max = min( i+window_len/2-1, y.size)
            fit = polyfit(x[i_min:i_max+1],y[i_min:i_max+1],order)
            retval[i] = polyeval(fit,x[i])
        

            
        return RamanSpectrum(pandas.Series(retval,spectrum.index))
        
            
    elif window == 'flat': #moving average
        w=ones(window_len,'d')
        spectrum.values[:] =convolve(w/w.sum(),s,mode='valid')[(window_len-1)/2:-(window_len-1)/2]
    else:
        w=eval(window+'(window_len)')
        spectrum.values[:] =convolve(w/w.sum(),s,mode='valid')[(window_len-1)/2:-(window_len-1)/2]
   
    
    return spectrum 
    
def calc_noise(spectrum,rnge,rnge_type = 'data'):
    start = argmin(abs(array(spectrum.index)-rnge[0]))
    end = argmin(abs(array(spectrum.index)-rnge[1]))
 
    xs = array([spectrum.index[start:end]]).flatten()
    
    ys= spectrum.values[start:end]
   
    r = polyfit(xs,ys,2)
    average = r[0]*xs**2+r[1]*xs + r[2]
    
    standarddev = sqrt(mean((ys-average)**2) - mean(ys-average)**2)
    
    return standarddev

def removespikes(spectrum):
    spectrum = copy(spectrum)
    start = int(min(array(spectrum.index)))
    end = int(max(array(spectrum.index)))
    for s in range(start,end,64):
        e = min(s+63,end)
        for threshold in [10,5]:
            noise = calc_noise(spectrum, (s,e))
            change = append(0,diff(spectrum.values[s:e]))
            spikes_x = where(abs(change)>noise*threshold)[0]+s
            for i in spikes_x:
                spectrum.values[i] = mean(spectrum.values[array([i-4,i-3,i-2,i+2,i+3,i+4])])
    return spectrum

def normalize(spectrum,rnge):
    start = argmin(abs(array(spectrum.index)-rnge[0]))
    end = argmin(abs(array(spectrum.index)-rnge[1]))
 
    ys = copy(spectrum)
    ys-=min(ys.iloc[start:end])
    ys/= max(ys.iloc[start:end])
    
    
    
    return ys


    
    
            


class File(object):
    num_frames = 1
    accum_time = 1
    def __init__(self, fname):
        self._fid = open(fname, 'rb')
        self._load_size()
        self._load_date_time()
        self.get_info()
       
        
    def _load_size(self):
        
        self._xdim = self.read_at(42, 1, uint16)[0]
        self._ydim = self.read_at(656, 1,  uint16)[0]
        self._numframes = int(self.read_at(1446, 1, int32))
        
    def _load_date_time(self):
        
        try:
            rawdate = self.read_at(20, 9,  int8)
            rawtime = self.read_at(172, 6,  int8)
            
            strdate = ''
            
            for ch in rawdate:
                strdate += chr(ch)
            
            for ch in rawtime:
                strdate += chr(ch)
            
            self._date_time = time.strftime("%b %d %Y %H:%M:%S",time.strptime(strdate,"%d%b%Y%H%M%S"))
        except:
            self._date_time = 'no date info'
        
    def get_size(self):
        return (self._xdim, self._ydim)
   
        

    def read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return  fromfile(self._fid, ntype, size)

    def load_img(self):
        img = self.read_at(4100,self._xdim * self._ydim* self._numframes,  float32)
        img = img.reshape((self._numframes,self._ydim, self._xdim))
        
        return img
   
    def get_info(self):
        
       # print 'datatype', self.read_at(108, 1, uint16)
        infostring = str()
       
        infostring+=  str(self._date_time)+'\n'
        infostring+=  'frames:'+ str(int(self.read_at(1446, 1, int32)))+'\n'
        
         
       # infostring+=  'readout time'+ str(self.read_at(672,1, int32))+'\n'
        infostring+=  'accumulations:'+ str(self.read_at(668,1, int32))+'\n'+ str(int(self.read_at(10,1, float32)))+ 'seconds'+'\n'
        infostring+=  'excitation wavelength:'+ str(self.read_at(3311,1, float64))+ 'nm'+'\n'
        infostring+= 'gain setting:'+ str(int(self.read_at(198,1, uint16)))+'\n'
        infostring+= 'detector temp' + str(self.read_at(36, 1, float32))+ 'degree C \n'
        
        self.info = infostring 
        return self.info
    def get_accum_time(self):
        
        return float(self.read_at(10,1, float32))
        
        
    def close(self):
        self._fid.close()

    
def import_calcd_spectrum(orca_output_file, normalize = False,color='k'):
    import re
    
    f = open(orca_output_file).read()
    r = f.find('RAMAN SPECTRUM')
    start =  f.find(':', r)-4
    end = f.find('\n\n', start)#r.find('The first', start)
    table = f[start:end]
    
    table = re.split('\n',table)
    for i in range(len(table)):
        line = table[i]
        table[i] = [int(line[0:4]),float(line[6:18]),float(line[18:32]),float(line[32:45])]
    table = transpose(table)
    if normalize == True:
            table[2]/=max(table[2])
   
    
    
    return vlines(table[1],0,table[2],linewidth = 2,color=color)

def etchegoin_analysis(folder):
    from RamanTools3 import RamanSpectrum
    os.chdir(folder)
    data = zeros((0,1024))
    frequency = zeros(data.shape)
    l = os.listdir(os.curdir)
    l.sort()
    for x in l:
        if 'notes' not in x and '.txt' in x:
            a = RamanSpectrum(x)
            a = removespikes(a)
            data = append(data,array([a.values]), axis = 0)
            frequency = append(frequency, array([a.index]),axis = 0)
    print data.shape[0], 'spectra averaged'
    #plot(frequency[:,512], 's')
   
    ##########now the data is in the proper form.
    
    tup = copy(data)
   
    pad = zeros((tup.shape[0],512))
    tup = append(pad,tup,axis = 1)
    tup = append(tup,pad,axis = 1)   #### pad with zeroes
    Snoise = array([mean(tup,axis = 0)]*tup.shape[0])

    tup2 = copy(tup)
    for i in range(tup.shape[0]):
        
        z = mean(tup[i])/mean(Snoise[0])
        
        tup[i]-=z*Snoise[0]
        tup[i] = roll(tup[i],i)  ###### correct the pixel offset
        tup2[i] = roll(tup2[i],i)  # rolling tup2 but not subtracting noise

    tup_av = mean(tup[:,512:1536],axis = 0)
    tup2_av = mean(tup2[:,512:1536],axis = 0)
    tup2_av-=8800
    
    tup_av = SGsmooth(arange(1024),tup_av, width = 11, order = 3)
    
    
#    plot(frequency[0],tup_av,label='etchegoin') 
#    plot(frequency[0],tup2_av,label='averaged') 
#    
#    figure()
#    plot(frequency[0],tup_av,label='etchegoin') 
#    
#    legend()
    return RamanSpectrum(pandas.Series(tup_av,frequency[0]))
    
def SPIDcorrect633(spectrum):
    c = copy(spectrum)
    for i in range(len(c)):
        s = argmin(abs(c.index[i]-array(Table_SPIDcorrect633.index)))
        c.iloc[i]/=Table_SPIDcorrect633.values[s]
    return c    

def SPIDcorrect785(spectrum):
    
    c = copy(spectrum)
 
    for i in range(len(c)):
        
        s = argmin(abs(c.index[i]-array(Table_SPIDcorrect785.index)))
        c.iloc[i]/=Table_SPIDcorrect785.values[s]
    
    return c    
    
    
FTPRef =  RamanSpectrum('/home/chris/Documents/DataWeiss/150430/150430_08.txt')
BrTPRef = RamanSpectrum('/home/chris/Documents/DataWeiss/150430/150430_14.txt')
ClTPRef = RamanSpectrum('/home/chris/Documents/DataWeiss/150424/150424_06.txt')
MeOTPRef = RamanSpectrum('/home/chris/Documents/DataWeiss/141014/4_methoxythiophenol.spe')
MethylTPRef = RamanSpectrum('/home/chris/Documents/DataWeiss/141007/1_methylbenzenethiol.spe')
CdMeOTPRef = RamanSpectrum('/home/chris/Documents/DataWeiss/140918/9_CdMeOTP.SPE') -18000
CdODPARef =  RamanSpectrum('/home/chris/Documents/DataWeiss/150121/1_reference CdODPA.spe') 
tolueneRef =  RamanSpectrum('/home/chris/Documents/DataWeiss/141007/Liquid sample corrected-spectrum of toluene.txt') 
ODPARef =  RamanSpectrum('/home/chris/Documents/DataWeiss/140908/OPDA 100s collection time on glass_bendregion_50xObj.spe')

#create wavelength dependent correction for SPID RamanMicroscope.  Then remove these artifacts from spectrum.
a = RamanSpectrum('/home/chris/Documents/DataWeiss/150417/cellphone/cellphone_04.txt')
a = removespikes(a)
a.values[:]= SGsmooth(array(a.index), a.values,width = 54, order = 5)[:]
r = polyfit(array(a.index[20:]), a.values[20:], 8)
b = polyeval(r,array(a.index))
b= (a.values/b)
Table_SPIDcorrect633 = pandas.Series(b,array(a.index))


a = RamanSpectrum('/home/chris/Documents/DataWeiss/150423b/150423_09.txt').iloc[100:]

a = removespikes(a)

a.values[:]= SGsmooth(array(a.index), a.values,width = 33, order = 5)[:]
r = polyfit(array(a.index), a.values, 4)
b = polyeval(r,array(a.index))
b= (a.values/b)
Table_SPIDcorrect785 = pandas.Series(b,array(a.index))

a = RamanSpectrum('/home/chris/Documents/DataWeiss/150423b/150423_10.txt').iloc[141:600]
a = removespikes(a)
a=smooth(a)
r = polyfit(array(a.index), a.values, 4)
b = polyeval(r,array(a.index))
b= (a.values/b)
Table_SPIDcorrect785 = pandas.concat([Table_SPIDcorrect785,pandas.Series(b,array(a.index))],join='outer')

