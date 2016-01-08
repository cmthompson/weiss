

from Tkinter import *
import tkFileDialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg

from SFG_Analysis import SG_Smooth
import threading
import Queue
import pickle
import pdb

from matplotlib.pyplot import plot, legend, ioff,gcf,clf,cla,show
from matplotlib.figure import Figure
from numpy import *
import numpy
import pandas
import time

from EthanolDesorptionSuccessForPub import *

Pt = 0
Ethoxy = 1
Al = 2
OH = 3
Oads = 4
Pt_ss = 5
SO = H= 6
EtOH = 7
Ox = 8


PLOT = 0
UPDATE_PROGRESS = 1
RESET_MENU =2

endall = 0





class ThreadControl:
        global endall
       
       
        def __init__(self,master,control_window,model = 'Jelemensky'):
                
                self.master = master
                self.c_window = control_window
                self.model = model
                self.periodicCall()
                print self.c_window.endflag
                return None
        def KinModelJelemensky(self, clear = True):
            global endall
    
            
            initial_conc = array([[0.5,0,0,0,0,0.1,0,1,0.001]])
            etohliq = 1
            

            if self.model == 'Simple Langmuir-Hinshelwood' :
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                for h in arange(0,1.25,0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o+h),e,al,oh,o,0,h,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            elif 'L-H' in self.model: 
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                for h in arange(0,1.25,0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o+h),e,al,oh,o,0,h,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            elif self.model == 'Jelemensky' or self.model == 'JelemenskyMod':
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                for so in arange(0,1.25,0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o),e,al,oh,o,1-so,so,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            elif self.model == 'JelemenskyNoSO':
                for e in arange(0,1.25,0.25):
                    for al in arange(0,1.25,0.25):
                        for oh in arange(0,1.25,0.25):
                            for o in arange(0,1-(e+al+oh),0.25):
                                    for o2 in [1E-6,1E-4,1E-2,1]:
                                        temp = array([[1-(e+al+oh+o),e,al,oh,o,1,0,etohliq,o2]])
                                        if all(temp>=0):
                                            initial_conc = append(initial_conc,temp,axis = 0)
            else:
                print "Model not recognized:", self.model
                return 0
            print "Number of Initial Conditions", initial_conc.shape
            self.Command_GUI((UPDATE_PROGRESS,("0/"+str(initial_conc.shape[0]))))
            
            if clear == True:
                self.c_window.RR_list = []
                self.c_window.groups_list = []
                self.c_window.groups_name_list = []
           
                     
            for i in range(len(self.c_window.RR_list),initial_conc.shape[0]): 
                self.Command_GUI((UPDATE_PROGRESS,(str(i)+"/"+str(initial_conc.shape[0]))))
                RR = RateRunout(inits = initial_conc[i])
               
                RR.RunOut(self.model,slope_limit = 1E-3,break_param = self.c_window.endflag)
                
                
                self.Command_GUI((PLOT,RR))
                
                self.c_window.RR_list.append(RR)
#                if CheckForInduction(RR.conc[Al],time_array = RR.time_array, _plot = False) == True:
#                    
#                    
#                    
#                    temp_array = array([])
#                    if len(self.c_window.groups_list) == 0:
#                        RR.SetType(len(self.c_window.groups_list))
#                        self.c_window.groups_list.append(RR)
#                        self.c_window.groups_name_list.append(str(len(self.c_window.groups_list)))
#                        self.Command_GUI((RESET_MENU,))
#                        print "NEW TYPE FOUND. Group type " + str(RR._type)
#                       
#                    else:
#                        for group in self.c_window.groups_list:
#                            
#                            temp_array = append(temp_array,_correlate(RR.conc[Al],group.conc[Al]))
#                            
#                        if max(temp_array) > 0.8:
#                            group = self.c_window.groups_list[where(temp_array == max(temp_array))[0]]
#                            
#                            RR.SetType(group._type)
#                            
#                        
#                        else:
#                            
#                            RR.SetType(len(self.c_window.groups_list))
#                            self.c_window.groups_list.append(RR)
#                            self.c_window.groups_name_list.append(str(len(self.c_window.groups_list)))
#                            self.Command_GUI((RESET_MENU,))
#                            print "NEW TYPE FOUND. Group type " + str(RR._type)
                
                
                    
                self.c_window.PauseFlag.wait()
                
                
                if self.c_window.endflag == True:
                    print "Thread Control Received end commande"
                    break
                if endall == 1:
                    break
    
                
                
            
            print "progam finished"
            return 0
            
        
        def SpanParameters(self):
            global endall
    
            
            
            etohliq = 1
            

            return 0
           
        def Command_GUI(self,msg):
                
                
                self.c_window.queue.put(msg)
               
                
                return 0
        
        

        def periodicCall(self):
               
                if endall == 1:
                    time.sleep(0.1)
                    self.master.destroy()
                    return 0
                else:
                    self.c_window.Queue_Callback()
                    self.master.after(50,self.periodicCall)
                
                
                        
                return 0




class Window(object):
    endflag = bool(False)
    control_thread = None
    def __init__(self, master  = None, upload = True):
        global saved
            
        if master  == None:
                self.top = Toplevel()
        else:
                self.top = master

        self.queue = Queue.Queue(maxsize = 2)
        
        self.frame = Frame(master = self.top)
        self.frame.grid()
        self.plotframe = Frame(master = self.frame)
        self.plotframe.grid(row = 0,column = 0, columnspan = 10)
       

        self.menubar = Menu(self.top)
        

       
        self.init_idx = 0

        self.nextbutton = Button(self.frame, text = 'next', command = self._next)
        
        self.nextbutton.grid(row = 1, column = 5)

        self.lastbutton= Button(self.frame, text ='last', command = self.last)
        self.lastbutton.grid(row = 1, column = 4)
        self.skiptenbutton= Button(self.frame, text ='print_inits', command = self.print_inits)
        self.skiptenbutton.grid(row = 1, column = 7)
        #self.inquirebutton= Button(self.frame, text ='')
        #self.inquirebutton.grid(row = 2, column = 7)
        self.RR_Entry = Entry(self.frame,width=5)
        self.RR_Entry.insert(END,"0")
        self.RR_Entry.grid(row=1,column=6)
        self.RR_Entry.bind("<Return>",self.Goto)
        
        self.clearRRbutton = Button(self.frame, text = 'clear', command = self.clearRR)
        self.clearRRbutton.grid(row = 1, column = 0)
        self.save = Button(self.frame, text = 'save',command = self.save)
        self.save.grid(row = 1,column = 1)
        self.loadbutton = Button(self.frame, text = 'load',command = self.loadwindow)
        self.loadbutton.grid(row = 3,column = 1)
        
        self.prog_label = Label(self.frame,width=20, height = 1, text = "0/0")
        self.prog_label.grid(row=2,column=6)
        self.lastbutton= Button(self.frame, text ='delete', command = self.delete)
        self.lastbutton.grid(row = 2, column = 5)
        
        self.types_label = Label(self.frame,width=20, height = 1, text = "0")
        self.types_label.grid(row=3,column=5)
        
        self.var_plot = IntVar()
        self.var_plot.set(0)
        self.plotbox = Checkbutton(self.frame, text = "plot", variable=self.var_plot)
        self.plotbox.grid(row = 3, column =6)
        
        self.startbutton= Button(self.frame, text ='start', command = self.start)
        self.startbutton.grid(row = 2, column = 0)
        self.pausebutton= Button(self.frame, text ='pause', command = self.pause)
        self.pausebutton.grid(row = 2, column = 1)
        self.quitbutton= Button(self.frame, text ='stop', command = self.stop)
        self.quitbutton.grid(row = 2, column = 2)
        self.show_list = list()
        
        self.groups_name_list = ['all']
        
        self.var_curr_group = StringVar()
        self.var_curr_group.set('all')
        self.groupMenu = OptionMenu(self.frame,self.var_curr_group, *self.groups_name_list, command = self.updategroup)
        self.groupMenu.grid(row = 5,column =6,sticky = W)
       
        self.groups_list = list()
        self.RR_list = list()
        self.show_list = list()
        
        
           
                    
            
        
        
        
        self.PauseFlag = threading.Event()
        self.PauseFlag.set()
        
        self.figure = Figure(figsize = (5,5))
        self.canvas = FigureCanvasTkAgg(self.figure,master = self.plotframe)
        self.canvas.show()
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.plotframe)
        self.toolbar.update()
        self.toolbar.grid()
        
        self.canvas._tkcanvas.grid()
        
       
        
        self.canvas.draw()
        
        self.top.config(menu= self.menubar)
        
      
        print 'at beginning', self.init_idx               
        return None
    def Queue_Callback(self):
            
            
        while self.queue.qsize():
            try:
                msg = self.queue.get()
                
                
                if msg[0] == PLOT:
                    
                    if self.var_plot.get() == 1:
                        msg[1].PlotRunOut(_fig = self.figure)
                        self.canvas.draw()
                        
                        
                            
                        
                elif msg[0] == UPDATE_PROGRESS:
                    self.prog_label.config(text = msg[1])
                elif msg[0] == RESET_MENU:
                    self._reset_option_menu(*self.groups_name_list)
                    
                       
                else:
                    print "unidentified msg"
                
                    
                            

                        
            except Queue.Empty:
                pass
            except:
                print "exception in queue"

        
        return 0
    
    
    def _reset_option_menu(self, *options):
        '''reset the values in the option menu

        if index is given, set the value of the menu to
        the option at the given index
        '''
        menu = self.groupMenu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                 self.updategroup(value))
       
        return 0
                
    def delete(self):
        self.RR_list.pop(self.init_idx)
        self.init_idx-=1
        self._next()
        return 0          
    def clearRR(self):
        self.RR_list = []
        self.groups_list = []
        self.groups_name_list = []    
        self.prog_label.config(text = '0/0')
        return 0
        
    def _next(self):
        
        clf()
        
        print self.init_idx
        if self.init_idx<len(self.RR_list)-1:
            self.init_idx+=1
            self.RR_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.canvas.draw()
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.RR_list)))
        
        else:
            print self.init_idx
            print "last file to show"
                    
            
        return 0
    def last(self):
        
        clf()
        if True:#self.init_idx>=0:
            self.init_idx-=1
            self.RR_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.canvas.draw()
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.RR_list)))
        
        else:
            
            print "already on first file"
                    
            
        return 0
    def Goto(self,extra):
         self.init_idx = int(self.RR_Entry.get())
         if self.init_idx in range(len(self.RR_list)):
            self.init_idx-=1
            self.show_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.canvas.draw()
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.RR_list)))
        
         else:
            
             print "invalid RR number"
         return 0
    def skipten(self):
        
        clf()
        if self.init_idx<len(self.show_list)-10:
            self.init_idx+=10
            self.show_list[self.init_idx].PlotRunOut(_fig = self.figure)
            self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
            self.canvas.draw() 
        else:
           
            print "can't go that high"
                   
            
        return 0
    def print_inits(self):
        
        if self.init_idx in range(len(self.RR_list)):
            output = pandas.Series(self.RR_list[self.init_idx].initials)
            output.index = ['Pt','Ethoxy','Al','OH','Oads','Pt_ss', 'SOorH','CH3OHliq','O2liq']
            print output
            output = pandas.Series(self.RR_list[self.init_idx].parameters)
            output.index = ['ka','_ka','kb','_kb','kc','kd','ke','kf','kg','kh']
            print output
        else:
            print "invalid RR number"
        return 0
    def remember(self,filename):
        import pickle
        print "Saving..."
        fh      = open(filename, 'wb') 
        pickler = pickle.Pickler(fh)
        
 
        pickler.dump(self.RR_list)
        fh.close()
        print "saved to", filename
        print len(self.RR_list), "runouts."
        
        return 0
    def save(self):
         
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*')]
        options['title'] = 'Save RRResults...'
        options['parent'] = self.top
     
        
        filename = tkFileDialog.asksaveasfilename(**options)
        
        athread = threading.Thread(target = self.remember, args = (filename,) )
        athread.daemon = True 
        athread.start()
        
        return 0
    def loadwindow(self):    
        import re
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*')]
        options['multiple'] = False
        options['title'] = 'Open RRResults...'
        options['parent'] = self.top
        
        filename = tkFileDialog.askopenfilename(**options)
        
        athread = threading.Thread(target = self.load, kwargs = {'filename':filename} )
        athread.daemon = True 
        athread.start()
        return 0

        
        
       
        
    def load(self, filename = 'RRresults.txt'):
        print "Loading from", filename , "..."
        
        
        fh = open(filename, 'rb')
# Creating the unpickler object.
        unpk = pickle.Unpickler(fh)
        
# Re-load the eggs object from our dumpfile.
        self.RR_list = unpk.load()
       
        fh.close()
        
        #self._reset_option_menu(*self.groups_name_list)
        print "loaded from", filename
        print len(self.RR_list), "runouts."
            
        
        self.queue.put((UPDATE_PROGRESS,"0/"+str(len(self.RR_list))))
        self.init_idx = 0
#        for item in self.RR_list:
#            item.initials = item.conc[:,0]
        
        return 0
    
    def pause(self):
        if self.PauseFlag.is_set() == True:
            self.PauseFlag.clear()
            print "program Paused"
        else:
            self.PauseFlag.set()
            print "program unpaused"
        return 0
    def stop(self):
        print "Stopping program..."
        self.endflag = True
        return 0
    def start(self):
        
        self.endflag = False
        threading.Thread(target = self.control_thread.KinModelJelemensky, kwargs = {'clear':False}).start()
        return 0
    def updategroup(self, value):
    
        self.init_idx = 0
        self.var_curr_group.set(value)
        
       
        if self.var_curr_group.get() == 'all':
            self.show_list = list(self.RR_list)
            print "showing all groups"
            
        else:
            self.show_list = list()
            target_type = int(self.var_curr_group.get())
            for rr in self.RR_list:
                if rr._type == target_type:
                    
                    self.show_list.append(rr)
            print len(self.show_list), "schemes of this type."
        self.show_list[0].PlotRunOut()
        self.prog_label.config(text = str(self.init_idx+1)+"/"+str(len(self.show_list)))
        self.canvas.draw()
            
            
        return 0
        
def quitproc():
        global endall
        endall = 1     
        return 0
    
            
        

  




    
    
        