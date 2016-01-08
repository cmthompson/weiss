
import numpy
import matplotlib.pyplot as plt
import tkFileDialog
import csv
from matplotlib.widgets import Cursor,SpanSelector

import os.path
from Tkinter import *
import time
import threading
from matplotlib.widgets import SpanSelector
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg


        

class GC_Window(object):
        peak_area = 0
        results = zeros((100,))
        file_index = 1
        def __init__(self, master  = None):
                
               
                
                if master  == None:
                        self.master = Toplevel()
                else:
                        self.master = master

                
                self.master.title(string = "GCViewer")
               
                self.plot_frame = Frame(master = self.master)
                self.plot_frame.grid (row = 0, column = 0)
                
                self.command_frame = Frame(master= self.master)
                self.command_frame.grid(row = 1, column = 0)

                self.filebase_Entry = Entry(self.command_frame,width=20)
                self.filebase_Entry.insert(END,"Nov12_FID_")
                self.filebase_Entry.grid(row=1,column=2)

                self.filenum_Entry = Entry(self.command_frame,width=5)
                self.filenum_Entry.insert(END,"1,1")
                self.filenum_Entry.grid(row=2,column=2)

                self.loadwaves_button = Button(master = self.command_frame, text = "load", width = 20,command = self.loadwaves)
                self.loadwaves_button.grid(row = 3, column = 2)

                self.run_button = Button(master = self.command_frame, text = "integrate", width = 20,command = self.program_run)
                self.run_button.grid(row = 4, column = 2)
                
                self.accept_button = Button(master = self.command_frame, text = "accept", width = 20,command = self.accept_baseline)
                self.accept_button.grid(row = 5, column = 2)
                
                self.menubar = Menu(self.master)
                

                self.filemenu = Menu(self.menubar, tearoff=0)
                self.filemenu.add_command(label="New window")
                self.filemenu.add_command(label="Open")
                self.filemenu.add_command(label="Save")
                
                self.filemenu.add_command(label="Exit", command = quitproc)
                self.menubar.add_cascade(label="File", menu=self.filemenu)
                # create more pulldown menus
                self.editmenu = Menu(self.menubar, tearoff=0)
                self.editmenu.add_command(label="Smooth")
                self.editmenu.add_command(label="Copy")
                self.editmenu.add_command(label="Paste")
                self.menubar.add_cascade(label="Edit", menu=self.editmenu)
                
                
                
                self.master.config(menu= self.menubar)
                self.f = figure()
               
                self.a  = self.f.add_subplot(111)
                self.a.plot([])
                self.a.plot([])
                self.redraw()
                
                
           
                self.files = [array([])]
                
                
                
                
                
                
               
               
                
                self.master.protocol("WM_DELETE_WINDOW",quitproc)
                              
                return None
       
        
        def DisplaySpectrum(self):
                import re
                file_opt = options = {}
                options['defaultextension'] = '.csv'
                options['filetypes'] = [('all files', '.*')]
                options['initialdir'] = 'C:\\sfg\\data'
                options['title'] = 'Open Spectrum...'
                options['parent'] = self.master
        
        
                
                str_name_list = tkFileDialog.askopenfilenames(**options)
                
                if str_name_list == '':
                        pass
                else:
                        name_list = re.split(' ',str_name_list)
                        for name in name_list:
                                loadGCfile(name)
                            
                        
                       
                return 0
        def loadwaves(self):
                import re
               
                filebase = self.filebase_Entry.get()
                filenum = self.filenum_Entry.get()

                filenum0 = int(re.split(',',filenum)[0])
                filenum1 = int(re.split(',',filenum)[1])
                self.files=[array([])]*(filenum1+1)
                
                
                for i in range(filenum0,filenum1+1):
                        if i<10:
                                
                                name = filebase + "0"+ str(i)+".asc"
                        else:
                                name = filebase+ str(i)+".asc"
                       
                        self.files[i] = loadGCfile(name)
               # self.a.plot(range(self.files[filenum0].size)
                self.a.lines[0].set_ydata(self.files[filenum0])
                self.a.lines[0].set_xdata(arange(self.files[filenum0].size))
                self.redraw()
                
                return 0 
                        
        def redraw(self):
            self.a.relim()
            self.a.autoscale()
            gcf().canvas.draw()
            self.span = SpanSelector(self.a, self.onselect, 'horizontal')
            return 0                
                
        def program_run(self):
                global baseline_end, baseline_start
                filebase = self.filebase_Entry.get()
                filenum = self.filenum_Entry.get()

                self.filenum0 = int(re.split(',',filenum)[0])
                self.filenum1 = int(re.split(',',filenum)[1])
                
               
                
              
               
                self.peak_area = 0
                baseline_start= 80
                baseline_end = 100
                self.file_index = self.filenum0
                
                self.onselect(baseline_start,baseline_end)
                
               # self.a_curs= DraggableRectangle(0,0)
                #self.b_curs = DraggableRectangle(10,0)
                

                return 0
        def accept_baseline(self):
            global baseline_start, baseline_end
            
            self.results[self.file_index] = self.peak_area
            self.file_index +=1
            if self.file_index>self.filenum1:
              pass
             
            else:
                self.onselect(baseline_start,baseline_end)
                

            
            return 0
      
            
            
        def onselect(self, vmin,vmax):
            global baseline_start, baseline_end
            cgram = self.files[self.file_index]
            time_array = arange(cgram.size)
     
            baseline_start = vmin
            baseline_end = vmax
            
            x1= baseline_start
            x2=baseline_end
            y1 = cgram[x1]
            y2 = cgram[x2]
            slope =(y2-y1)/(x2-x1)
            baseline = slope*(time_array-x1)+ y1
            cgram_bl = cgram - baseline
            
            self.a.lines[0].set_ydata(cgram)
            self.a.lines[0].set_xdata(time_array)
            self.a.lines[1].set_ydata(baseline)
            self.a.lines[1].set_xdata(time_array)
            
            
            self.peak_area = sum(cgram_bl)/5000
            self.redraw()
            
            return 0
        
            
        
 
def loadGCfile(file_name):
    os.chdir("C:\\Users\\Chris\\Google Drive")
    try:
        a = numpy.loadtxt(file_name,
                          dtype = str,
                          delimiter = ",",
                          usecols = [0],
                          skiprows = 26)
        c = numpy.array([])
        for i in numpy.arange(a.size):
            if a[i][0] == "I" or a[i][0] == "d" :
                c= numpy.append(c,i)
        
        a = numpy.delete(a,c)
        a = numpy.array(a, dtype = int)
    except:
        
        return -1
    return a






        
        

          




        
        
def quitproc():
    
    
    root.destroy()
    return 0

root = Tk()
root.protocol("WM_DELETE_WINDOW", quitproc)
win = GC_Window(root)
def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
  

gcf().canvas.mpl_connect('pick_event', onpick)

root.mainloop()


