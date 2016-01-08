from Tkinter import *
import tkFileDialog
import numpy
import csv
import numpy
import SFG_Notebook
import matplotlib.axes
import matplotlib.figure
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from SFG_Error import *
import os
import SFG_Analysis
import time

channel_type_list = ['SFG','IR','Stdev','Norm','AvgSFG','AvgIR','TotStdev','AvgNorm']
current_checker = None

class SFG_DisplayWindow(object):

        current_checker = None
        
        
        checker_list = []

        def __init__(self, master  = None):
                
                if master  == None:
                        self.master = Toplevel()
                else:
                        self.master = master

               
                self.master.title(string = "SFGViewer")
               
                
                self.checker_frame=Frame(master = self.master, width =500)
                self.checker_frame.grid(row=1,column=0)

                self.menubar = Menu(self.master)
                

                self.filemenu = Menu(self.menubar, tearoff=0)
                self.filemenu.add_command(label="New window", command = SFG_DisplayWindow)
                self.filemenu.add_command(label="Open", command = self.DisplaySpectrum)
                self.filemenu.add_command(label="Save",command = self.SaveSpectrum)
                self.filemenu.add_command(label="SaveFig",command = self.SaveFigure)
                self.filemenu.add_command(label="ViewNotebook",command = self.ViewNotebook)
                self.filemenu.add_command(label="Exit", command = self.quitproc)
                self.menubar.add_cascade(label="File", menu=self.filemenu)
                # create more pulldown menus
                self.editmenu = Menu(self.menubar, tearoff=0)
                self.editmenu.add_command(label="Smooth", command = self.SmoothSpectrum)
                self.editmenu.add_command(label="Time Series", command = self.TimeSeries)
                self.editmenu.add_command(label="Copy")
                self.editmenu.add_command(label="Paste")
                self.menubar.add_cascade(label="Edit", menu=self.editmenu)
                
                self.menubar.add_command(label = "Notes", command = self.ViewNotebook)
                
                
                
                self.master.config(menu= self.menubar)
                
                self.Plot= MultichannelPlot(self.master,row = 0 , column = 0,update_prot = 'draw')#, width = 1, height = 3)
                
                self.master.protocol("WM_DELETE_WINDOW", self.quitproc)
                              
                return None
       
        
        def DisplaySpectrum(self):
            import re
            options = {}
            options['defaultextension'] = '.csv'
            options['filetypes'] = [('all files', '.*')]
            options['initialdir'] = 'C:\sfg\data'
            options['multiple'] = True
            options['title'] = 'Open Spectrum...'
            options['parent'] = self.master
            
    
    
            
            str_name_list = tkFileDialog.askopenfilenames(**options)
           
            if type(str_name_list) == tuple:
                if str_name_list == '':
                        pass
                else:
                    for name in str_name_list:
                        if 'notes' in name:
                            SFG_Notebook.SFG_NotebookWindow(target_file = name)
                        elif name =='':
                            break
                        else:
                            newspectrum = OpenSpectrum(name)
                            self.AddChecker(self.Plot.AddChannel(newspectrum,'AvgSFG'))
                            self.current_checker = self.checker_list[-1]
            else:
                if str_name_list == '':
                    pass
                else:
                    name_list = re.split(' ',str_name_list)
                    for name in name_list:
                        newspectrum = OpenSpectrum(name)
                        self.AddChecker(self.Plot.AddChannel(newspectrum,'AvgSFG'))
                        self.current_checker = self.checker_list[-1]
                       

               
            return 0

        def SaveSpectrum(self):
                
                file_opt = options = {}
                options['defaultextension'] = '.csv'
                options['filetypes'] = [('all files', '.*')]
                options['initialdir'] = 'C:\\sfg\\data'
                options['title'] = 'Open Spectrum...'
                options['initialfile'] = current_checker.channel.spec_array.Name
                options['parent'] = self.master

                if self.current_checker  == None:
                        return 0
                str_filename = tkFileDialog.asksaveasfilename(**options)
               
                if str_filename == '':
                        return 0
                else:
                        SaveSpectrum(self.current_checker.channel.spec_array,str_filename)

                return 0
        def ViewNotebook(self):
                
                tar = 'C:\\sfg\\data\\'+self.current_checker.channel.channel_name[:-2]
                if self.current_checker.channel == None:
                    return 0
                SFG_Notebook.SFG_NotebookWindow(target_dir = tar)
                return 0 
        def SmoothSpectrum(self):

                if self.current_checker == None:
                    return 0
                
                
                
                new_spec_array = self.current_checker.channel.spec_array.Duplicate()
                new_spec_array.Array[1,:,0]= SFG_Analysis.SG_Smooth(new_spec_array.Array[1,:,0])
                
                
                self.AddChecker(self.Plot.AddChannel(new_spec_array,'AvgSFG',''))
                
                channel = self.checker_list[-1].channel
      
                return 0
        def TimeSeries(self):
                
                if self.current_checker == None:
                        return 0

                width =1
                interval = 2
                
                win = SFG_DisplayWindow()
                time_series_spec = self.current_checker.channel.spec_array.Array
                
                
                freq = time_series_spec[0,:,0]
                
                size= time_series_spec.shape[0]
                averaged = numpy.ndarray((0,26))
                legend_list = list()
                for i in range(2,size-width,interval):


                        
                        ys =  numpy.mean(time_series_spec[i:i+width,:,0], axis = 0)

                        
                        ys = SFG_Analysis.SG_Smooth(ys)
                        
                        if i > 20:
                            char_str = 's'
                        else: 
                            char_str = '-'
                        win.Plot.gca().plot(freq,ys,char_str,label = str(i), )
                        legend_list.append(str(i))
                
                win.Plot.gca().legend(legend_list)
                win.Plot.canvas.draw()
                
                return 0
                        


                
         
        def AddChecker(self,channel):
                self.checker_list.append(checker(self,channel))
                
                return 0 

       

        def RemoveSpectrum(self,checker):
                
                self.Plot.RemoveChannel(checker.channel)
                checker.frame.grid_forget()
                self.checker_list.remove(checker)
               
                return 0
      
                        
                        
        def SaveFigure(self):
                os.chdir("C:\\sfg\\data")
                self.Plot.savefig('figure.png')
                return 0
        def quitproc(self):
                self.master.destroy()
                return 0



                                             
class checker:
         
        def __init__(self,master,channel):
                self.master = master
                #self.index = index
                self.frame = Frame(master = self.master.checker_frame)
                self.frame.grid()
                
                #self.namevar = StringVar()
                #self.namevar.set(channel.channel_name)                                     
                self.channel = channel                                     
                self.visible_var = IntVar()
                self.visible_var.set(1)
                self.box = Checkbutton(self.frame,
                                       variable=self.visible_var,
                                       command=self.cb)
                self.box.grid(row=0,column = 5)
                

                self.DeleteButton = Button(self.frame,
                                        text = "Delete",
                                        command = lambda: self.master.RemoveSpectrum(self),
                                        width=5,
                                        height=1)
                self.DeleteButton.grid(row=0,column = 7)

                self.NameLabel =  Label(self.frame,width=30, height = 1, text = channel.channel_name)
                self.NameLabel.bind("<Button-1>",self.set_current)
                self.NameLabel.grid(row=0,column = 1)

                self.var_channel_type = StringVar()
                self.var_channel_type.set(self.channel.channel_type)
                
               
                self.ChannelTypeMenu = OptionMenu(self.frame,self.var_channel_type, *channel_type_list, command =  self.SetChannelType)
                self.ChannelTypeMenu.grid(row = 0,column =2,sticky = W)

                
                return None        
                 
        def set_current(self,event):
                
                if self.master.current_checker == None:
                        pass
                else:
                        self.master.current_checker.NameLabel.config(relief = FLAT)
                self.master.current_checker = self
                
                self.NameLabel.config(relief = SUNKEN)
                return 0 
                
                
        def cb(self):
                
                if self.visible_var.get() == 0:
                        self.master.Plot.HideChannel(self.channel)
                        
                else:
                        self.master.Plot.ShowChannel(self.channel)
                
                return 0
       
        def SetChannelType(self,channel_type):
                self.channel.SetChannelType(channel_type)
                return 0                
      
                

class SpectrumArray:
    #SpectrumArray class is a 3D object containing spectrum data from 4 channels: SFG, IR, Norm, Stdev
    FrequencyList = []
    Array = numpy.array([])
    StartFreq = 0
    EndFreq = 0
    StepSize=0
    FilePath = ''
    
    
    def __init__(self,startfreq =2800,endfreq = 3600,stepsize = 5, name = "Current"):
        
        self.StartFreq = startfreq
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



class Channel(matplotlib.lines.Line2D):
        channel_name = None
        channel_type = None
        
        spec_array = None
        
        def __init__(self,
                     xdata,
                     ydata,
                     master_plot,
                     spec_array,
                     channel_type,
                     color = 'k',
                     marker = '.',
                     linestyle = '-',
                     animated = False):
                
                matplotlib.lines.Line2D.__init__(self,
                                                 spec_array.Array[0,:,0].tolist(),
                                                 spec_array.Array[-1,:,0].tolist())
                                                 
                self.set_animated(animated)
                self.set_linestyle(linestyle)
                self.set_marker(marker)   
                                                          
                self.set_color(color)
                self.spec_array = spec_array
                self.channel_type = channel_type
                self.SetChannelType(self.channel_type)
                self.channel_name = spec_array.Name
                
                return None
        def SetChannelType(self,channel_type):
                if self.channel_type in ['SFG','IR','Stdev','Norm','AvgSFG','AvgIR','TotStdev','AvgNorm']:
                        self.channel_type = channel_type
                else:
                        return -1
                self.ChannelUpdate()
                return 0
        def ChannelUpdate(self):
                c_dict = {'Freq':self.spec_array.Array[0,:,0],
                             'SFG': self.spec_array.Array[-1,:,0],
                             'IR' : self.spec_array.Array[-1,:,1],
                             'Stdev': self.spec_array.Array[-1,:,2],
                             'Norm': self.spec_array.Array[-1,:,3],
                             'AvgSFG': self.spec_array.Array[1,:,0],
                             'AvgIR': self.spec_array.Array[1,:,1],
                             'TotStdev': self.spec_array.Array[1,:,2],
                             'AvgNorm': self.spec_array.Array[1,:,3]}
                if self.channel_type in ['SFG','IR','Stdev','Norm','AvgSFG','AvgIR','TotStdev','AvgNorm']:
                        try:
                                self.set_xdata(c_dict['Freq'])
                                self.set_ydata(c_dict[self.channel_type])
                        except KeyError:
                                pass
                else:
                        return -1
                
                return 0


class MultichannelAxis(matplotlib.axes.Subplot):
        #Multichannel Plot class used to display data from SpectrumArray instance.  Channel_type should be one of eight SpectrumArray Channels            
    
  
        def __init__(self,fig,loc):
                
                matplotlib.axes.Subplot.__init__(self,fig,111)
                
                self.color_list = ['r','b','g','c','m','y','k']
                self.grid(b=True,which = 'major',axis = 'x')
              
                
             
                
                return None
        
        
                
        
        
       
        
                
class MultichannelPlot(matplotlib.figure.Figure):
        
        def __init__(self,master,row = 0, column =0, rowspan = 5, columnspan = 5,width = 5, height =3,update_prot = 'blit'):
                matplotlib.figure.Figure.__init__(self,figsize = (width,height))
                self.update_prot = update_prot
                self.frame = Frame(master = master)
                self.frame.config(bd = 5)
                
                self.frame.grid(row = row, column = column, padx = 5, pady = 5)
                self.channel_list = []
                self.array_list = []
                self.color_list = ['r','b','g','c','m','y','k']
                
               
                
               
                
                self.a  = self.add_subplot(MultichannelAxis(self,111))
                
                
                
                
                
                
                
                
               
                self.canvas = FigureCanvasTkAgg(self,master = self.frame)
                self.canvas.show()
                
                self.canvas._tkcanvas.pack(side=TOP, fill = BOTH,expand =True)
                
                self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
                self.toolbar.update()
                self.toolbar.pack(side= BOTTOM, fill = BOTH,expand =True)#,expand = True)#fill=BOTH)#, expand=1)
                self.canvas.draw()
                self.background = self.canvas.copy_from_bbox(self.a.bbox)
                
                
                
                return None

        def AddChannel(self,spec_array,channel_type, color = None):

                if color == None or color == '':
                        self.a.add_line(Channel([],[],self,spec_array,channel_type, color = self.color_list[0]))
                        self.color_list.append(self.color_list[0])
                        del(self.color_list[0])
                
                else:
                        self.a.add_line(Channel([],[],self,spec_array,channel_type, color = color))
                #self.Update()     
                self.Redraw()
                return  self.a.lines[-1]
        def RemoveChannel(self,channel):
                self.a.lines.remove(channel)
                self.Redraw()
                
                return 0
        
        
        def SetChannelColor(self,channel,clr):
                if clr != '':
                        channel.color = clr
                        
                else:
                        channel.color = self.color_list[0]
                        self.color_list.append(self.color_list[0])
                        del(self.color_list[0])
                

        
                return 0

        def ShowChannel(self,channel):
                channel.set_visible(True)
                
                self.Update()
                return 0

        def HideChannel(self,channel):
                channel.set_visible(False)
                self.Update()
                return 0
       
                
        
                
                
                                            
        
                        
        def Redraw(self):
                
                self.a.relim()
                self.a.autoscale_view(tight = False)
                                       
                self.canvas.draw()
                self.canvas.restore_region(self.background)
                for line in self.a.lines:
                        self.a.draw_artist(line)
                        
       
                self.canvas.blit(self.a.bbox)
                
                
                return 0

        def SaveFigure(self,filename):
                
                self.f_copy = self.a
                self.f_copy.savefig('a.png')
                
                return 0

        def Update(self):
                if self.update_prot == 'draw':
                        self.canvas.draw()
                        return 0
              
                (lower_y_lim, upper_y_lim) = self.a.get_ylim()
                (lower_x_lim, upper_x_lim) = self.a.get_xlim()
                scaley_bool = False
                scalex_bool = False
                scaley_down_bool = True

                
                for channel in self.a.lines:
                        if channel.get_visible() == True:
                                channel.ChannelUpdate()
                                scaley_bool = scaley_bool or max(channel.get_ydata()) > upper_y_lim  or min(channel.get_ydata()) < lower_y_lim
                                scaley_down_bool =  scaley_down_bool and max(channel.get_ydata()) < upper_y_lim*0.6
                                scalex_bool = scalex_bool or max(channel.get_xdata())!= upper_x_lim or min(channel.get_xdata()) != lower_x_lim
                                
                if scaley_bool or scalex_bool or scaley_down_bool:
                          
                          self.Redraw()
                       
                              
                        
                else:
                        
                        self.canvas.restore_region(self.background)
                        for line in self.a.lines:
                                self.a.draw_artist(line)
                                
               
                        self.canvas.blit(self.a.bbox)
            
                return 0
                          
                
                

def OpenSpectrum(file_name):#def OpenSpectrum():
        # opens a spectrum from data in "file_name" and returns a SpectrumArray instance.
        with open(file_name,"rb") as f:
                    
                CSV_READER = csv.reader(f,dialect = 'excel')
        
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
                
                
                
        SpecArray = SpectrumArray(startfreq = input_array[0,0,0],endfreq = input_array[0,-1,0],stepsize =input_array[0,1,0]-input_array[0,0,0], name = file_name[-12:-4])
        SpecArray.Array = input_array
        SpecArray.FilePath = os.curdir
   
        
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




       

        
       
                        

