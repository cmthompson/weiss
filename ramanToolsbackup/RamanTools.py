# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 11:37:39 2014

@author: chris
"""



from numpy import *#float64,arange,zeros
import scipy.optimize
import pandas
from Tkinter import *
import Tkinter
import tkFileDialog, tkSimpleDialog, tkMessageBox
from matplotlib.pyplot import *
from matplotlib.axes import *
from SFGMeFiles import SFG_Notebook
import matplotlib.figure 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import os
pandas.options.display.mpl_style = None# 'default'
from copy import copy

import pdb
from matplotlib.widgets import SpanSelector
from collections import deque
from matplotlib.colors import ColorConverter

from ramanTools.RamanSpectrum import *

colordict= ColorConverter()

list_of_display_windows = []

def RGBtohex(rgbtuple): return '#%02x%02x%02x'%  (rgbtuple[0]*255,rgbtuple[1]*255,rgbtuple[2]*255)



class DisplayWindow(object):
        global CdMeOTPRef, MeOTPRef
        color_list = deque(['b','g','r','c','m','y','k'])
        current_checker = None
        

        def __init__(self, master):
                
                self.rootref = master
                self.master = Toplevel()
                #self.masterframe= PanedWindow(master = self.master,showhandle=True)
               # self.masterframe.pack()
                        
                        
                self.frame = Frame(master = self.master)
                self.Plot = Figure(figsize=(6,3))               
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
                #self.scroll = Tkinter.Scrollbar(self.frame)
                #self.scroll.pack(side  = Tkinter.RIGHT, fill = Tkinter.BOTH)
               
                
                self.checker_frame=Tkinter.Frame(master = self.master)#,yscrollcommand=self.scroll.set)
                #self.scroll.config(command=self.checker_frame.yview)                
                
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
                self.filemenu.add_command(label="Fitting window", command = lambda:FittingWindow(Toplevel(),ramanspectrum=self.current_checker.spectrum))#, kwargs = {'ramanspectrum':self.current_checker.channel.spec_array})
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
                self.refsmenu.add_command(label = "ClTP", command = lambda:self.AddChannel(ClTPRef))
                self.refsmenu.add_command(label = "BrTP", command = lambda:self.AddChannel(BrTPRef))
                self.refsmenu.add_command(label = "FTP", command = lambda:self.AddChannel(FTPRef))
                self.refsmenu.add_command(label = "MethylTP", command = lambda:self.AddChannel(MethylTPRef))
                self.refsmenu.add_command(label = "CdODPA", command = lambda:self.AddChannel(CdODPARef))
                self.refsmenu.add_command(label = "toluene", command = lambda:self.AddChannel(tolueneRef))
                self.refsmenu.add_command(label = "CdMethylTP", command = lambda:self.AddChannel(CdMethylTPRef))
                self.menubar.add_cascade(label = 'References', menu = self.refsmenu)
                
                
                self.master.config(menu= self.menubar)
                
                #self.masterframe.add(self.frame)
                self.frame.pack(side = TOP, expand=1, fill=BOTH)#(row = 0, column = 0, padx = 25, pady = 25)
                self.legendbox.pack(side=BOTTOM)
                self.statusbar.pack(side = BOTTOM,expand=1,fill=X)
                #self.masterframe.add(self.checker_frame)
                self.checker_frame.pack(side=BOTTOM,expand = 1,fill=X)#(row=1,column=0)
                self.canvas._tkcanvas.pack( expand = 1, fill = BOTH)
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
                
                print os.path.dirname(self.current_checker.name)
                try:
                    SFG_Notebook.SFG_NotebookWindow(target_dir = os.path.dirname(self.current_checker.name))
                except IOError:
                    tkSimpleDialog.Message('no file found')
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
                self.frame.pack(side=BOTTOM,expand=1, fill=X)
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
                self.NameLabel.pack(side=RIGHT,expand=1, fill=X)#.grid(row=0,column = 1)
                
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
##############################################################  ############################################################## ############################################################## ############################################################## ############################################################## 
                ############################################################## ############################################################## ############################################################## ############################################################## 
                ############################################################## ############################################################## ############################################################## ############################################################## ############################################################## 
       
class FittingWindow:
    
    
    def __init__(self, master,ramanspectrum =None):
        global guessplot,dataplot
        
        self.master  = master
        self.textframe= Frame(master = self.master)
        
        self.scroll = Tkinter.Scrollbar(self.textframe)
        self.scroll.grid(row=0,column=1)
        self.t = Tkinter.Text(self.textframe,yscrollcommand=self.scroll.set,width=30)
        self.scroll.config(command=self.t.yview)
        self.t.grid(row=0,column=0)
        
        self.plotframe = Frame(master = self.master)
        
        self.frame = Frame(master = self.master)
        
        self.textframe.grid(row=0,column=0,columnspan=3)
        self.plotframe.grid(row = 0, column = 3, columnspan = 11,sticky = 'ew')
        self.frame.grid(column = 1, row = 1,columnspan = 11, rowspan = 3,sticky = 'snew')
        self.buttonframe = Frame(master = self.master)
        self.buttonframe.grid(column=0, row =1)
        ##############################
        self.menubar = Menu(self.master)
        
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New window", command = lambda: FittingWindow(Toplevel()))
        self.filemenu.add_command(label="Open", command = self.open_data)
        self.filemenu.add_command(label="Save",command = None)
        self.filemenu.add_command(label="SaveFig",command = None)
        self.filemenu.add_command(label="ViewNotebook",command = None)
        self.filemenu.add_command(label="Exit", command = self.quitproc)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.master.config(menu= self.menubar)
        ##############################
        
        self.fit_button = Tkinter.Button(master = self.buttonframe, command = self.fit_and_draw, width  = 5, text = 'FitNow')
        self.fit_button.grid(row = 3, column = 0)
        self.open_button =  Tkinter.Button(master = self.buttonframe, command = self.open_data, width  = 5, text = 'open')
        self.open_button.grid(row = 4, column = 0)
#        self.open_ref_button =  Tkinter.Button(master = self.buttonframe, command = self.open_ref, width  = 5, text = 'Choose reference')
#        self.open_ref_button.grid(row = 5, column = 0)
        
#        self.open_bkg_button =  Tkinter.Button(master = self.buttonframe, command = self.open_bkg, width  = 5, text = 'Choose background')
#        self.open_bkg_button.grid(row = 6, column = 0)
#        
#        self.ref_label =  Tkinter.Label(master = self.buttonframe, text = '')
#        self.ref_label.grid(row = 7, column = 0)
#        
#        self.bkg_label =  Tkinter.Label(master = self.buttonframe, text = '')
#        self.bkg_label.grid(row = 8, column = 0)
        
        self.smoothbutton = Tkinter.Button(master = self.buttonframe, command = self.smoothdata, width  = 5, text = 'Smooth')
        self.smoothbutton.grid(row = 5, column = 0)
 
       
        
        self.function_list=[
                              'OneGaussian',
                              'TwoGaussian',
                              'ThreeGaussian',
                              'FourGaussian',
                              'FiveGaussian']
        
        self.var_func = StringVar()
        self.var_func.set(self.function_list[0])
        
        
       
       
        self.MotorMenu = OptionMenu(self.buttonframe,self.var_func, *self.function_list, command = self.init_function)
        self.MotorMenu.grid(row = 3,column =1,sticky = W)
        
        self.normalization_constant = 1
        self.scale_list = []
        self.var_list = []
        
        self.fig = Figure(figsize=(5,3))
        self.ax1  = self.fig.add_subplot(111)
        dataplot = self.ax1.plot(arange(2800,3605,5),zeros((161,)),animated = True)[0]#(ax = self.ax1).lines[-1]
        
        guessplot = self.ax1.plot(arange(2800,3605,5),zeros((161,)),animated = True)[0]
        
        
        self.canvas = FigureCanvasTkAgg(self.fig,master = self.plotframe)
        
        self.canvas.show()
        
        
        self.canvas._tkcanvas.pack(side=TOP, fill = BOTH,expand =True)
        
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.plotframe)
        self.toolbar.update()
        self.toolbar.pack(side= BOTTOM, fill = BOTH,expand =True)#,expand = True)#fill=BOTH)#, expand=1)
        
        self.canvas.draw()
        self.canvas.show()
        self.background = self.canvas.copy_from_bbox(self.ax1.bbox)
            
         
        self.reference = numpy.ndarray((161,))
        self.reference[:] = 1
        self.reference_name  = ''
        self.guess = list()

        self.name = ['']
        if ramanspectrum is None:
            self.a = pandas.Series(zeros(161),arange(2800,3605,5))
        else:
            self.a = copy(ramanspectrum)
            print self.a
           
            self.t.insert(END,'data multiplied by'+str(1/max(self.a)))
            self.a[:]/=max(self.a.values)
            
        self.startfreq_text = Entry(self.buttonframe,width = 5)
        self.startfreq = min(array(self.a.index))
        self.startfreq_text.insert(END,str(self.startfreq))
        self.startfreq_text.bind("<Return>", self.update_limits)
        self.startfreq_text.grid(row = 0 , column =1,sticky = W)
        
        
        self.endfreq_text = Entry(self.buttonframe,width = 5)
        self.endfreq = max(array(self.a.index))
        self.endfreq_text.insert(END,str(self.endfreq))
        self.endfreq_text.bind("<Return>", self.update_limits)
        self.endfreq_text.grid(row = 1 , column =1,sticky = W)
        
        if self.init_function(0) == -1:
            self.t.insert(END, 'error initializing fit function')
        
        self.ax1.cla()
        self.canvas.show()
        self.background = self.canvas.copy_from_bbox(self.ax1.bbox)
        

        dataplot = self.ax1.plot(array(self.a.index),self.a.values,animated=True)[0]
        x= array(self.a.index)
        guessplot = self.ax1.plot(x,zeros(self.a.size),animated=True)[0]
        self.ax1.set_xlim(min(self.a.index),max(self.a.index))
        self.ax1.set_ylim(min(self.a.values),1)
        
        self.canvas.show()

        
        
       
        self.raw = self.a.copy   
        self.startidx = 0
        self.endidx = -1
           
        self.update_limits(0)
        return None
        
    def nothing(self):
        return 0
    def quitproc(self):
            self.master.destroy()
            return 0
        
        
    def init_function(self,functiontype):
        global function
        import inspect
        
        if functiontype == None:
            functiontype = self.var_func.get()
        
        self.functiontype = functiontype
        
      
                    
        if functiontype == 'OneLorentzian':
            def function(x,A1,w1,G1,m,b): return m*x/1000+b + A1**2/((x-w1)**2+G1**2)
        elif functiontype == 'TwoLorentzian':
            def function(x,A1,A2,w1,w2,G1,G2,m,b): return m*x/1000+b + A1**2/((x-w1)**2+G1**2) +A2**2/((x-w2)**2+G2**2)
    
        elif functiontype == 'ThreeLorentzian':
            def function(x,A1,A2,A3,w1,w2,w3,G1,G2,G3,m,b): return m*x/1000+b + A1**2/((x-w1)**2+G1**2) +A2**2/((x-w2)**2+G2**2) +A3**2/((x-w3)**2+G3**2)
        elif functiontype == 'FourLorentzian':
            def function(x,A1,A2,A3,A4,w1,w2,w3,w4,G1,G2,G3,G4,m,b): return m*x/1000+b + A1**2/((x-w1)**2+G1**2) +A2**2/((x-w2)**2+G2**2) +A3**2/((x-w3)**2+G3**2) +A4**2/((x-w4)**2+G4**2)
             
        elif functiontype == 'FiveLorentzian':
            def function(x,A1,A2,A3,A4,A5,w1,w2,w3,w4,w5,G1,G2,G3,G4,G5,m,b): return m*x/1000+b + A1**2/((x-w1)**2+G1**2) +A2**2/((x-w2)**2+G2**2) +A3**2/((x-w3)**2+G3**2) +A4**2/((x-w4)**2+G4**2)+A5**2/((x-w5)**2+G5**2)
        elif functiontype == 'OneGaussian':
            def function(x,A1,w1,G1,m,b): return m*x/1000+b + A1*exp(-(x-w1)**2/G1)
        elif functiontype == 'TwoGaussian':
            def function(x,A1,A2,w1,w2,G1,G2,m,b): return A1*exp(-(x-w1)**2/G1) +A2*exp(-(x-w2)**2/G2) +m*x/1000+b 
    
        elif functiontype == 'ThreeGaussian':
            def function(x,A1,A2,A3,w1,w2,w3,G1,G2,G3,m,b): return m*x/1000+b + A1*exp(-(x-w1)**2/G1) +A2*exp(-(x-w2)**2/G2) +A3*exp(-(x-w3)**2/G3) 
        elif functiontype == 'FourGaussian':
            def function(x,A1,A2,A3,A4,w1,w2,w3,w4,G1,G2,G3,G4,m,b): return m*x/1000+b +A1*exp(-(x-w1)**2/G1) +A2*exp(-(x-w2)**2/G2)  +A3*exp(-(x-w3)**2/G3) +A4*exp(-(x-w4)**2/G4) 
             
        elif functiontype == 'FiveGaussian':
            def function(x,A1,A2,A3,A4,A5,w1,w2,w3,w4,w5,G1,G2,G3,G4,G5,m,b): return m*x/1000+b + (A1/G1*numpy.sqrt(2*pi))*exp(-(x-w1)**2/(2*G1**2)) +(A2/G2*numpy.sqrt(2*pi))*exp(-(x-w2)**2/(2*G2**2))  +(A3/G3*numpy.sqrt(2*pi))*exp(-(x-w3)**2/(2*G3**2))  +(A4/G4*numpy.sqrt(2*pi))*exp(-(x-w4)**2/(2*G4**2)) +(A5/G5*numpy.sqrt(2*pi))*exp(-(x-w5)**2/(2*G5**2)) 
        else:
            tkMessageBox.showerror('Not regconized function')
            def function(x,m,b): return m*x/1000+b
       
         

#==============================================================================
        self.w_name = list() 
        self.w_name = inspect.getargspec(function).args[1:]
        
        self.guess= []
       
        for w in self.w_name:
            if 'A' in w:
                self.guess.append(0.1)
            elif 'w' in w:
                self.guess.append(1000)
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
                self.scale_list[i].grid(row = int(i/8), column = i%8)
                
                if self.w_name[i][0] == 'A':
                     self.scale_list[i].config(from_ =0, to =  5,resolution = 0.1)
                     
                     self.scale_list[i].set(1)
                elif self.w_name[i][0] == 'w':
                    self.scale_list[i].config(from_ = self.startfreq-20, to =  self.endfreq+20,resolution = 1)
                    self.scale_list[i].set(2800)
                elif self.w_name[i][0] == 'G':
                    self.scale_list[i].config(from_ = 1, to =  50)
                    self.scale_list[i].set(7)
                elif self.w_name[i][0] == 'm':
                    self.scale_list[i].config(from_ = -5, to =  5, resolution = 0.05)
                    self.scale_list[i].set(0)
                elif self.w_name[i][0] == 'b':
                    self.scale_list[i].config(from_ = -5, to =  5, resolution = 0.05)
                    self.scale_list[i].set(0)
                else:
                    self.t.insert(END, "Variable not recognized:", self.w_name[i] )
                self.scale_list[i].bind('<B1-Motion>',self.guessdraw)
        return 0
        
        
    def smoothdata(self):
        self.a.smoooth()
        self.guessdraw(0)
        return 0
        
        
    def update_limits(self,extra):
        functiontype = self.var_func.get()
        
        self.startfreq = max(float(self.startfreq_text.get()),min(array(self.a.index)))
        self.endfreq = min(float(self.endfreq_text.get()),max(array(self.a.index)))
        
        
        
        self.startidx = self.a.nearest(self.startfreq)
        self.endidx =  self.a.nearest(self.endfreq)        
        
        
        for i in range(len(self.guess)):
            self.guess[i] = self.scale_list[i].get()

        self.ax1.cla()
        self.canvas.show()
        self.background = self.canvas.copy_from_bbox(self.ax1.bbox)
        

        dataplot = self.ax1.plot(array(self.a.index[self.startidx:self.endidx]),self.a.values[self.startidx:self.endidx],animated=True)[0]#(ax = self.ax1).lines[-1]
        x= array(self.a.index[self.startidx:self.endidx])
        guessplot = self.ax1.plot(x,zeros(x.size),animated=True)[0]
        
        
        #self.ax1.set_xlim(min(self.a.index),max(self.a.index))
        #self.ax1.set_ylim(min(self.a.values),1)
        
        self.canvas.show()
        self.guessdraw(0)

        
        
        return 0
            
    def open_data(self): 
        global dataplot,guessplot
        self.name = self.DisplaySpectrum()
       
        if self.name == -1:
            return 0
        try:
            self.a = RamanSpectrum(self.name)
            self.normalization_constant= 1/max(self.a)
            self.startfreq = min(array(self.a.index))
            self.startfreq_text.insert(END,str(self.startfreq))
            self.endfreq = max(array(self.a.index))
            self.endfreq_text.insert(END,str(self.endfreq))
            
        except:
            self.t.insert(END, 'error opening spectrum')
            return -1
        
        
        self.raw = self.a.copy
        self.ax1.cla()
        self.canvas.show()
        self.background = self.canvas.copy_from_bbox(self.ax1.bbox)
        

        dataplot = self.ax1.plot(array(self.a.index),self.a.values,animated=True)[0]#(ax = self.ax1).lines[-1]
        x= array(self.a.index)
        guessplot = self.ax1.plot(x,zeros(self.a.size),animated=True)[0]
        self.ax1.set_xlim(min(self.a.index),max(self.a.index))
        self.ax1.set_ylim(min(self.a.values),1)
        
        self.canvas.show()

        self.update_limits(0)
        
        
       
        
        return 0
    
    def open_ref(self):

        pass
        
        return 0 
        
    def open_bkg(self):

        pass
        return 0 
        
            
        
    def recalc_data(self):
        if self.raw.shape == self.reference.shape:
            self.a= SG_Smooth(self.raw,width = 11,order = 3)/self.reference/self.normalization_constant
            self.ax1.cla()
            plot(self.a[0],self.raw/self.reference)
            plot(self.a[0],self.a[1])
        else:
            self.t.insert(END, "reference invalid")
            self.reference_name = "No IR Reference"
            
            self.ax1.cla()
            self.ax1.plot(self.a[0],self.a[1])
            self.canvas.draw()
        
        return 0
        

    def guessdraw(self,ex):
        global function,guessplot,dataplot
        
        
        x = array(self.a.index[self.startidx:self.endidx+1])
        
        
        for i in range(len(self.guess)):
            self.guess[i] = self.scale_list[i].get()
        
        self.canvas.restore_region(self.background)
        self.ax1.lines[-1].set_xdata(x)
        self.ax1.lines[-1].set_ydata(function(x,*self.guess))
        
        
        for l in self.ax1.lines:

            self.ax1.draw_artist(l)
           
        self.canvas.blit(self.ax1.bbox)
        
            
        

        return 0
    def fit_and_draw(self):
        
        global function
        print type(self.a)
        if type(self.a) == pandas.core.series.Series:
            self.a = RamanSpectrum(self.a)
        #result = fitspectrum(self.a, (float(self.a.index[self.startidx]),float(self.a.index[self.endidx+1])),'Custom',self.guess,function = function)
        print self.guess
        result = fitspectrum(self.a, (self.startfreq,self.endfreq),'Custom',self.guess,function = function)
        fittingparameters = result[0]
        xfit = result[1]
        yfit = result[2]
        if result == -1:
            tkMessageBox.showerror('Fit Failed')
            return 0

        z = list(fittingparameters[0])            
        self.canvas.restore_region(self.background)
        self.ax1.lines[-1].set_xdata(xfit)
        self.ax1.lines[-1].set_ydata(yfit)
        
        
        for l in self.ax1.lines:

            self.ax1.draw_artist(l)
        for i in range(len(self.w_name)):
            #self.scale_list[i].set(result[0][i])
            if "w" in self.w_name[i]:
                self.ax1.axvline(x = z[i], ymin = 0, ymax = 1 ,color = 'r')
           
        self.canvas.blit(self.ax1.bbox)

        self.t.insert(END, "  \nResult Found for " + str(self.name))
        self.t.insert(END, " \nReferenced to IR spectrum " +self.reference_name)
        self.t.insert(END, "  \nNormalized by constant "+str(self.normalization_constant))
        for i in range(len(self.w_name)):
            self.t.insert(END, ' \n'+self.w_name[i]+': '+str(z[i]))
        
                
        
        return 0
    def DisplaySpectrum(self):
        import re
        global name_list, str_name_list
        file_opt = options = {}
        options['defaultextension'] = '.spe'
        options['filetypes'] = [('all files', '.*'),('SPE files', '.SPE'), ('csv files','.csv'),('text files','.txt')]
        options['title'] = 'Open Spectrum...'
        options['initialdir'] = '/home/chris/Documents/DataWeiss'

        str_name_list = tkFileDialog.askopenfilename(**options)
        if str_name_list == '':
            return -1
        return str_name_list                        
     



