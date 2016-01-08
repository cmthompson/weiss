from Tkinter import *
from ctypes import *
import threading
import tkMessageBox
import time
import logging
import Queue
import Flow_Notebook

mx = windll.nicaiu
DAQmx_Val_GroupByChannel = c_ulong(0)
DAQmx_Val_ChanForAllLines = c_ulong(0)
DAQmx_Val_ChanPerLine = c_ulong(1)
DAQmx_Val_ChanForAllLines = c_ulong(1)                                         
DAQmx_Val_Volts = c_ulong(10348)
data_array = (c_ulong * 4)(0,1,0,0)
cast(data_array, POINTER(c_ulong))

ENABLEALL =1
DISABLEALL = 2
UNHIGHLIGHT  = 3
HIGHLIGHT = 4
MFC3SET = 5
MFC4SET = 6


logging.basicConfig(filename='Flowlog.log',level=logging.INFO)


class ParamEntryLine:

        def __init__(self,master):
                self.master = master
                self.frame=Frame(master = master.P1, bd =2, relief =FLAT)
                self.frame.grid()
                
                self.O2_Label = Label(self.frame,width=20, height = 1, text = "O2 (ccm)")
                self.O2_Label.grid(row=0,column=0)
                self.O2_Var = StringVar()
                self.O2_Entry = Entry(self.frame,width=5,textvariable =self.O2_Var)
                self.O2_Entry.insert(END,"0")
                self.O2_Entry.grid(row=0,column=1)

                self.N2_Label = Label(self.frame,width=20, height = 1, text = "N2 (ccm)")
                self.N2_Label.grid(row=0,column=2)
                
                self.N2_Var = StringVar()
                self.N2_Entry = Entry(self.frame,width=5,textvariable = self.N2_Var)
                self.N2_Entry.insert(END,"0")
                self.N2_Entry.grid(row=0,column=3)

                self.Time_Label = Label(self.frame,width=20, height = 1, text = "Time (hr)")
                self.Time_Label.grid(row=0,column=4)
                
                self.Time_Var = StringVar()
                self.Time_Entry = Entry(self.frame,width=5,textvariable = self.Time_Var)
                self.Time_Entry.insert(END,"0")
                self.Time_Entry.grid(row=0,column=5)

                self.Delete_Button = Button(self.frame,
                        text = "Delete",
                        command = lambda: self.master.DeleteLine(self),
                        width=7,height=1)
                self.Delete_Button.grid(row= 0, column = 6, padx=10)

                self.menubar = Menu(root)
                

                self.filemenu = Menu(self.menubar, tearoff=0)
                self.filemenu.add_command(label="Log", command = lambda: Flow_Notebook.Flow_LogWindow())
                self.menubar.add_cascade(label="File", menu=self.filemenu)
                root.config(menu= self.menubar)
                return None
        def Disable(self):
                self.O2_Entry.config(state = DISABLED)
                self.N2_Entry.config(state = DISABLED)
                self.Time_Entry.config(state = DISABLED)
                self.Delete_Button.config(state=DISABLED)
                return 0
        
        def Enable(self):
                self.O2_Entry.config(state = NORMAL)
                self.N2_Entry.config(state = NORMAL)
                self.Time_Entry.config(state = NORMAL)
                self.Delete_Button.config(state = NORMAL)
                return 0 

class ParamEntryWindow:
        LineList = []
        running = 0
        ParamList = []

        def __init__(self,master):
                self.queue = Queue.Queue()
                self.master = master
                self.P1 = Toplevel()
                self.frame=Frame(master = self.P1)
                self.frame.grid(row=0,column=0, padx = 20,pady =5)
                
                for i in range(2):
                        self.Addline()

                self.ParamButton = Button(self.frame,
                    text = "Start Program",
                    command=self.go,height=1)
                self.ParamButton.grid(row=1,column=0,sticky=W)

                self.AddButton = Button(self.frame,
                    text = "Add line",
                    command=self.Addline,width=7,height=1)
                self.AddButton.grid(row=0,column=0,sticky=W)
               
                
                return None
        def Queue_Callback(self):
                
                
                
                ##"""Handle all messages currently in the queue, if any."""
                while self.queue.qsize(  ):
                        try:
                                msg = self.queue.get()
                                
                                
                                if msg[0] ==ENABLEALL:
                                        self.EnableAll()
                                elif msg[0] == DISABLEALL:
                                        self.DisableAll()

                                elif msg[0] == HIGHLIGHT:                              
                                        self.LineList[msg[1]].frame.config(relief = RAISED,background = "green")

                                elif msg[0]== UNHIGHLIGHT:
                                         self.LineList[msg[1]].frame.config(relief = FLAT ,background = "SystemButtonFace")
                                       
                                    
                        except Queue.Empty:
                                pass

                
                return 0       

        def Addline(self):
                self.LineList.append(ParamEntryLine(self))
                
                
                return 0
        def UpdateLines(self):
                for item in self.LineList:
                        item.frame.grid()
                return 0
        
        def go(self):
                global SSthread
                self.ParamList = []
                duration = float(0)
                self.DisableAll()
                for a in self.LineList:
                        
                        self.ParamList.append((float(a.O2_Var.get()),float(a.N2_Var.get()),float(a.Time_Var.get())))
                        duration+= float(a.Time_Var.get())
                
                
                if self.master.running == 0:
                        self.master.running = 1
                        SSthread = threading.Thread(target = self.master.ProgramRun)
                        SSthread.daemon = True
                        SSthread.start()
                        
                        logging.info("Program to last " + str(duration)+ " hours.")
                elif self.master.running == 1:
                        tkMessageBox.showwarning("Warning", "Program is already running.  Please press stop before restarting.")
                        
                
                return 0

        
                
        
        def DeleteLine(self,lParamEntry):
                lParamEntry.frame.grid_forget()
                self.LineList.remove(lParamEntry)
                
                return 0
        def EnableAll(self):
                for a in self.LineList:
                                a.Enable()
                                a.frame.config(relief = FLAT ,background = "SystemButtonFace")
                self.AddButton.config(state =NORMAL)
                self.ParamButton.config(state= NORMAL)
                return 0
        
        def DisableAll(self):
                
                for a in self.LineList:
                                
                                a.Disable()
                                
                self.AddButton.config(state =DISABLED)
                self.ParamButton.config(state= DISABLED)
                return 0


class ProgramControl:
        running = 0
        
        def __init__(self,master):
                self.master = master
                self.mainwin = MainWindow(self)
                self.Window = ParamEntryWindow(self)
                self.Window.P1.withdraw()
                self.Window.P1.protocol("WM_DELETE_WINDOW",self.Window.P1.withdraw)
                
                self.master.after(100,self.PeriodicCall)
                return None
        
        def ProgramRun(self):
                
                
                self.Window.queue.put((DISABLEALL,))
                
               
                i = 0
                for line in self.Window.ParamList:
                       
                        if i != 0:
                                self.Window.queue.put((UNHIGHLIGHT,i-1))#PEntryWin.LineList[i-1].frame.config(relief = FLAT ,background = "SystemButtonFace")
                        self.Window.queue.put((HIGHLIGHT,i))#PEntryWin.LineList[i].frame.config(relief = RAISED,background = "green")
                        i+=1
                        StepTime = int(line[2]*3600)
                        
                        self.UpdateMFCs((0,0,line[0],line[1]))
                        for secs in range(StepTime):
                                time.sleep(1)
                                if self.running == 0:
                                        logging.info("program terminated")
                                        self.Stop()
                                        self.Window.queue.put((ENABLEALL,))
                                        return 0
                                else:
                                        pass
                self.running=0
                self.Stop()
                self.Window.queue.put((ENABLEALL,))
 
                return 0

        def UpdateDig(self,dig):
                
                
                data = c_ulong(dig)
                written = c_ulong()
                TH0 = c_ulong()

               

                CHK(mx.DAQmxCreateTask("",byref(TH0)))
                
                CHK(mx.DAQmxCreateDOChan(TH0,"Dev1/port1","",DAQmx_Val_ChanForAllLines))
          
                
                CHK(mx.DAQmxStartTask(TH0))
                
               
                
                CHK(mx.DAQmxWriteDigitalU16(TH0,1,1,c_double(10.0),DAQmx_Val_GroupByChannel,byref(data),byref(written),None));

                                             
                mx.DAQmxStopTask(TH0)
        
        

                mx.DAQmxClearTask(TH0)

                             

               
                return 0
        

 
        def UpdateVoltage(self, volts,MFC):
                
                data = c_double(volts)
                written = c_ulong()
                TH0 = c_ulong()
                

                if MFC == 3:
                        s = "Dev1/ao0"
                elif MFC  ==4:
                       s= "Dev1/ao1"
                else:
                        pass



                                        
               

                CHK(mx.DAQmxCreateTask("",byref(TH0)))
                
                CHK(mx.DAQmxCreateAOVoltageChan(TH0,s,"",c_double(0),c_double(5),DAQmx_Val_Volts,""))
                
                
                CHK(mx.DAQmxStartTask(TH0))
                
               
                
                CHK(mx.DAQmxWriteAnalogF64(TH0,1,1,c_double(10.0),DAQmx_Val_GroupByChannel,byref(data),None,None));

                                             
                mx.DAQmxStopTask(TH0)
        
        

                mx.DAQmxClearTask(TH0)
                
                
                
               
                
                
                        
                
                
                return 0

        def UpdateMFCs(self,MFC_flow):

                volts_3 = float(MFC_flow[2]*0.1428)
                volts_4 = float(MFC_flow[3]*0.13)

                dig = 15
                for i in range(len(MFC_flow)):
                        if MFC_flow[i] > 0:
                                dig-=2**i
                
                self.UpdateDig(dig)
                
               
                if volts_3 > 5:
                        volts_3 = 5
                if volts_4 > 5:
                        volts_4 = 5
                


                self.UpdateVoltage(volts_3,3)
                self.UpdateVoltage(volts_4,4)
                time_of_update = time.localtime()
                self.mainwin.queue.put((MFC3SET,"MFC3 Setting:" + str(MFC_flow[2])))
                self.mainwin.queue.put((MFC4SET,"MFC4 Setting:" + str(MFC_flow[3])))
                
                logging.info("Updated MFC 3 to " + str(MFC_flow[2])+" mL/min " "and MFC 4 to " + str(MFC_flow[3])+" mL/min at " + (str(time_of_update.tm_hour)+":"+str(time_of_update.tm_min)+"."))
             
                return 0
        def Stop(self):
                self.UpdateMFCs((0,0,0,0))
                self.running = 0
                
                return 0
        
        def PeriodicCall(self):
                global mainwin
                self.Window.Queue_Callback()
                self.mainwin.Queue_Callback()
                self.master.after(500,self.PeriodicCall)
                return 0
        
class MainWindow:
        
       
        

        
        def __init__(self,master):
           
                
                self.frame=Frame(master = root,width=200, height=300)
                self.frame.grid(row=0,column=0, padx = 20,pady =5, columnspan = 10)
                self.master = master

                self.queue = Queue.Queue()
        
               
                

                
                
                self.StartButton = Button(self.frame,
                    text = "Start",
                    command=lambda: self.master.UpdateMFCs((0,0,float(self.Speed_Entry.get()),float(self.MaxRPM_Entry.get()))),width=7,height=1)
                self.StartButton.grid(row=1,column=0,sticky=W)
                self.StopButton = Button(self.frame,
                    text = "Stop",
                    command=self.master.Stop,
                    width=7,
                    height=1)
                self.StopButton.grid(row=2,column=0,sticky=W)

                  
                

                self.ProgramButton = Button(self.frame,
                    text = "Program",
                    command=lambda: FlowControl.Window.P1.deiconify(),
                    width=7,height=1)
                self.ProgramButton.grid(row=4,column=0,sticky=W)

                

                self.Speed_Label = Label(self.frame,width=20, height = 1, text = "MFC3 (ccm)")
                self.Speed_Label.grid(row=1,column=2)
                
                self.Speed_Entry = Entry(self.frame,width=5)
                self.Speed_Entry.insert(END,"0")
                self.Speed_Entry.grid(row=1,column=3)

                self.MaxRPM_Label = Label(self.frame,width=20, height = 1, text = "MFC4 (ccm)")
                self.MaxRPM_Label.grid(row=2,column=2)

                self.MaxRPM_Entry = Entry(self.frame,width=5)
                self.MaxRPM_Entry.insert(END,"0")
                self.MaxRPM_Entry.grid(row=2,column=3)

                #self.StepAir_Label = Label(self.frame,width=20, height = 1, text = "Air step size (ccm)")
                #self.StepAir_Label.grid(row=3,column=2)

                #self.StepAir_Entry = Entry(self.frame,width=5)
                #self.StepAir_Entry.insert(END,"5")
                #self.StepAir_Entry.grid(row=3,column=3)

                #self.StepTime_Label = Label(self.frame,width=20, height = 1, text = "Time between steps (hr)")
                #self.StepTime_Label.grid(row=4,column=2)

                #self.StepTime_Entry = Entry(self.frame,width=5)
                #self.StepTime_Entry.insert(END,"1")
                #self.StepTime_Entry.grid(row=4,column=3)

                self.MFC3_Set = StringVar()
                self.MFC3_Set.set('0')
                self.MFC3Setting_Label = Label(self.frame,width=20, height = 1, textvariable = self.MFC3_Set)
                self.MFC3Setting_Label.grid(row=1,column=4)

                self.MFC4_Set = StringVar()
                self.MFC4_Set.set('0')
                self.MFC4Setting_Label = Label(self.frame,width=20, height = 1, textvariable = self.MFC4_Set)
                self.MFC4Setting_Label.grid(row=2,column=4)
               

                return None

        def Queue_Callback(self):
                
                
                
                ##"""Handle all messages currently in the queue, if any."""
                while self.queue.qsize(  ):
                        try:
                                msg = self.queue.get()
                                
                                
                                if msg[0] ==MFC3SET:
                                        self.MFC3_Set.set(msg[1])
                                elif msg[0] == MFC4SET:
                                        self.MFC4_Set.set(msg[1])

                                
                                       
                                    
                        except Queue.Empty:
                                pass

                
                return 0       

       
                



def CHK(err):
        mx = windll.nicaiu
        if err<0:
                buf_size =400
                buf = create_string_buffer('\000' * buf_size)
                mx.DAQmxGetErrorString(err,byref(buf),buf_size)
                logging.warning("nidaq error")
                raise RuntimeError('nidaq called error %d: %s'%(err,repr(buf.value)))
        return None

def quitproc():
        
        FlowControl.Stop()
        
        root.quit()
        root.destroy()

        return None




                                
                        
                                     
             

root = Tk()
root.protocol("WM_DELETE_WINDOW", quitproc)

FlowControl = ProgramControl(root)
root.title("MFC Control")

root.mainloop()
