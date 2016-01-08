# SFG4_Queue3.py the top level control program for SFG instrument.  Defines two windows, the main spectrum taking window and the optimization window.  Operations of
# both of these windows utilize threading and queues.
import pdb


from Tkinter import *
import tkMessageBox
import threading
import ctypes
import numpy
from ctypes import *
import tkFileDialog
import tkSimpleDialog
import time
import os
import logging
import Queue
from scipy import optimize
from SFG_axes_XPSQ8 import *
import SFG_axes_XPSQ8 as SFG_axes
import SFG_Run_Status
import SFG_Notebook
from SFG_Display import *
from SFG_Error import *
import numpy

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg





SFGMAIN_STATUS_STOPPED = 0
SFGMAIN_STATUS_RUNNING = 1
SFGMAIN_STATUS_PAUSED  = 2 




CurrentFreq=0
StartFreq =0
EndFreq = 0
StepSize = 5
No_of_Scans = 2
ScanNo = 0
NumShots = 5


DISPLAY_ERROR_MESSAGE = -1
PARAM_UPDATE = 0
UPDATE_FREQ = 1
UPDATE_SCANNO = 2
UPDATE_STATUS = 3
UPDATE_PLOTS = 4
UPDATE_TIME_REMAINING = 5
SAVE_SPECTRUM = 6
PAUSE_SPECTRUM = 7
STOP_SPECTRUM = 8
KILL_QUEUE = 9
UPDATE_FILENAME = 10
WARNING = 11
NOTEBOOK = 12
DISABLE_ALL = 13
ENABLE_ALL = 14
UPDATE_MOTOR_POS = 101
DISPLAY_HISTOGRAM  = 200
DISPLAY_CALIB  = 201
wSFGWIN = 1
wOPTWIN = 2

end_program = False






class SFG_Control(object):
        global  str_motor_list,DAQ1,sfgwin,errorhandler
        Current_Window = wSFGWIN
        
        boxcar_width = 1  # averaging width used for optimize window
        
        status = SFGMAIN_STATUS_STOPPED
        

        def __init__(self,master):
                global DAQ1,str_motor_list
                
                self.master = master
                str_motor_list = SFG_axes.init_motors(1)
                
                
                
                self.MainArray = SpectrumArray(startfreq = 2800,endfreq = 3600,stepsize = 5)
                DAQ1 = DAQObject()
                
                self.periodicCall()

                return None
        
        
        def StartSpectrum(self):
                global StartFreq,EndFreq,StepSize,No_of_Scans,motor_status,NumShots,ScanNo,PauseFlag, Spec_name, updateflag
                self.Current_Window = wSFGWIN
                logging.info("Started Spectrum"+str(StartFreq)+str(EndFreq)+str(StepSize)+str(No_of_Scans))
                
                
               
                
                
                if self.status == SFGMAIN_STATUS_RUNNING:
                        
                        CallError(SPECTRUM_IN_PROGRESS)
                        return -1
                else:      
                        self.status = SFGMAIN_STATUS_RUNNING

                
                self.Command_GUI((DISABLE_ALL,))
                Spec_name = GetSpectrumName()
                
                self.Command_GUI((UPDATE_FILENAME,Spec_name))
                PauseFlag = threading.Event()
                PauseFlag.set()
                updateflag = threading.Event()
                updateflag.clear()
               
                
                ScanNo=0
                self.Command_GUI((PARAM_UPDATE,))      
                updateflag.wait()
               
                CurrentFreq = StartFreq
                
                sfgwin.MainArray.reset(StartFreq,EndFreq,StepSize)
                
                SFG_axes.SetMotorMotionParam()  
                while self.status == SFGMAIN_STATUS_RUNNING:
                        
                        PauseFlag.wait()
                        start_time = time.time()
                        
                        temp = CalculateTargetFreq(CurrentFreq,StartFreq,EndFreq,StepSize,ScanNo,No_of_Scans)
                        
                        target = temp[0]
                        if ScanNo !=  temp[1]:
                                        SaveSpectrum(sfgwin.MainArray.Array,Spec_name)
                                        ScanNo = temp[1]
                        
                        
                        CurrentFreq = target
                        self.Command_GUI((UPDATE_FREQ,CurrentFreq))
                        self.Command_GUI((UPDATE_SCANNO,ScanNo))
                        
                        
                        if target == 0:
                                self.status = SFGMAIN_STATUS_STOPPED
                                break
                        self.Command_GUI((UPDATE_STATUS,"Scanning to current frequency..."))                   
                        SFG_axes.GotoWavenumber(target)
                        self.Command_GUI((UPDATE_STATUS,"Measuring..."))
                        s = DAQ1.CollectNShots(NumShots)
                        sfgwin.MainArray.insertpoint(ScanNo,CurrentFreq,s)
                        self.Command_GUI((UPDATE_STATUS,"Updating plots..."))
                        
                        self.Command_GUI((UPDATE_PLOTS,))
                        
                        duration = time.time()-start_time
                        if isEven(ScanNo):

                            time_remaining = time.gmtime(((CurrentFreq-StartFreq)/StepSize+(No_of_Scans - ScanNo)*(EndFreq-StartFreq)/StepSize)*duration)
                        else:
                            time_remaining = time.gmtime(((EndFreq-CurrentFreq)/StepSize+(No_of_Scans - ScanNo)*(EndFreq-StartFreq)/StepSize)*duration)
                        time_remaining_str = str(time_remaining.tm_hour)+":"+str(time_remaining.tm_min)+":"+str(time_remaining.tm_sec)
                        self.Command_GUI((UPDATE_TIME_REMAINING,time_remaining_str))
                
                self.Command_GUI((UPDATE_STATUS,"Scanning to home..."))
                SFG_axes.GotoWavenumber(2800)
                
                
                self.Command_GUI((UPDATE_STATUS,"Saving motor positions.  Please wait..."))
                SFG_axes.SaveMotorPositions()
                logging.info("Saved motor positions")
                
                self.Command_GUI((UPDATE_STATUS, "Motor positions saved."))
                self.Command_GUI((UPDATE_STATUS, "Saving file..."))
                self.Command_GUI((SAVE_SPECTRUM,Spec_name))
                self.Command_GUI((ENABLE_ALL,))
                
                       
                self.Command_GUI((UPDATE_STATUS, "Ready."))
                
                return 0

                
        def Optimize_Loop(self):
                
                global optwin,DAQ1

                
                
                self.status = SFGMAIN_STATUS_RUNNING
                self.Current_Window = wOPTWIN
                darray = numpy.ndarray(shape = [self.boxcar_width,4])
              
                
                
                logging.debug("starting optimize thread")
                
                
                
                while self.status == SFGMAIN_STATUS_RUNNING :
                        
                        
                        s = numpy.array([DAQ1.CollectNShots(1)])
                        if darray.shape[0] > 99:
                                darray = darray[1:]
                        
                        darray = numpy.append(darray,s,axis = 0)
                        
                        data=  numpy.mean(darray[-self.boxcar_width:],axis = 0)
                              
                        optwin.OptArray.ContDatainsertpoint(data)
                        self.Command_GUI((UPDATE_PLOTS,))
                                
                       
             
                return 0

        def Motor_Calibration(self, motor):
                
                global optwin,DAQ1
                
                self.status = SFGMAIN_STATUS_RUNNING
                self.Current_Window = wOPTWIN

                logging.info("Calibrating " + motor.AxisName)
 
                SFG_axes.GotoWavenumber(2800)
                
                logging.debug("starting motor calibration thread")
                
                frequency_list = numpy.arange(2800,3650,50)
                data_list = numpy.array([])
                
                
                left = 80
                right  = 100
                
               
                
                for target in frequency_list:
                        logging.debug('optimizing at ' + str(target))
                        self.Command_GUI((UPDATE_STATUS,"Calibrating "+motor.AxisName+". Frequenc: "+str(target)))
                        SFG_axes.GotoWavenumber(int(target))
                       
                        center = motor.GetPosition()
                        
                        position_list = numpy.arange(center-left,center+right,20)
                        data = numpy.array([])
                        for position_target in position_list:
                                logging.debug('traveling to ', +position_target)
                                motor.GotoPosition(position_target)
                                motor.WaitUntilStopped()
                                avgIR = DAQ1.CollectNShots(100)[1]
                                
                                data = numpy.append(data,avgIR)
                                if self.status == SFGMAIN_STATUS_STOPPED:
                                        return 0

                

                        fit_coeffs = numpy.polyfit(position_list,data,deg=3)
                        x = numpy.arange(center-left,center+right,1)
                        y = fit_coeffs[0]*x**3+ fit_coeffs[1]*x**2 + fit_coeffs[2]*x + fit_coeffs[3]

                        
                        optimum_x = x[numpy.where(y == numpy.max(y))]
                        
                        data_list = numpy.append(data_list, optimum_x[0])
                        
                       
                        
                        self.Command_GUI((DISPLAY_CALIB,(x,y,position_list,data,'fig1')))
                        
                        
                final_fit_coeffs = numpy.polyfit(frequency_list,data_list,deg=3)
                logging.info("found calibration coefficients, " + str(final_fit_coeffs))
                a = numpy.arange(2800,3605,5)
                b = final_fit_coeffs[0]*a**3+ final_fit_coeffs[1]*a**2 + final_fit_coeffs[2]*a + final_fit_coeffs[3]
                self.Command_GUI((DISPLAY_CALIB,(a,b,frequency_list,data_list,'fig2')))
                
                        
                SFG_axes.GotoWavenumber(2800)
                self.Command_GUI((UPDATE_STATUS,"Ready."))
                self.status = SFGMAIN_STATUS_STOPPED

               

                return 0
        def Motor_Optimization(self):
                import scipy
                global optwin,DAQ1
                
                self.status = SFGMAIN_STATUS_RUNNING
                self.Current_Window = wOPTWIN

                logging.info("Optimizing motors")
 
                
                data_list = numpy.array([])
                logging.debug("starting motor optimization thread")

                for motor in SFG_axes.motor_list[1:4]:
                       
                       
                        center = motor.GetPosition()
                        
                        position_list = numpy.arange(center-100,center+150,50)
                        y = numpy.array([])
                        for position_target in position_list:
                                self.Command_GUI((UPDATE_STATUS,"Optimizing "+motor.AxisName+". Position: "+str(round(position_target))))
                                logging.debug(motor.AxisName +' traveling to '+str(position_target))
                                
                                motor.GotoPosition(position_target)
                                motor.WaitUntilStopped()
                                
                                avgIR = DAQ1.CollectNShots(200)[1]
                                
                                
                                y = numpy.append(y,avgIR)
                                if self.status == SFGMAIN_STATUS_STOPPED:
                                        return 0
                        
                        fit_coeffs = numpy.polyfit(position_list,y,deg=3)
                        #x = position_list
                        x_fit = numpy.linspace(center-100,center+100,50)
                        
                        def y_fit(x):return (fit_coeffs[0]*x**3+ fit_coeffs[1]*x**2 + fit_coeffs[2]*x + fit_coeffs[3])
                        
                            
                     
                        optimum_x = x_fit[numpy.where(y_fit(x_fit) == numpy.max(y_fit(x_fit)))]
                       
                        if optimum_x.size == 1:
                                motor.GotoPosition(int(optimum_x))
                         
                                data_list = numpy.append(data_list,optimum_x)
                        
                
                        
                        self.Command_GUI((DISPLAY_CALIB,(position_list,y,x_fit,y_fit(x_fit))))
                        
                        
                self.Command_GUI((UPDATE_STATUS,"Ready"))
                logging.info("found optimized positions, " + str(data_list))
                
                

               

                return 0
                                        
                                        
                                        
        def Frequency_Location(self):
                from scipy import optimize
                global optwin,DAQ1
                
                self.status = SFGMAIN_STATUS_RUNNING
                self.Current_Window = wOPTWIN
 
               
                
                
                
               
                
                left = 80
                right  = 100
                
                motor4 = SFG_axes.motor_list[3]
                motor1 = SFG_axes.motor_list[0]



                self.Motor_Optimization()
                motor1_pos = numpy.array([motor1.GetPosition()])
                motor4_pos = numpy.array([motor4.GetPosition()])

                motors_start_pos = [SFG_axes.motor_list[0].GetPosition(),SFG_axes.motor_list[1].GetPosition(),SFG_axes.motor_list[2].GetPosition(),SFG_axes.motor_list[3].GetPosition()]
                motor1_start_pos = motors_start_pos[0]
                motor1_target_list = numpy.arange(motor1_start_pos+50,motor1_start_pos+250,50)
                #print motors_start_pos
                for motor1_target in motor1_target_list:
                       
                        self.Command_GUI((UPDATE_STATUS,"Finding Frequency"))
                        motor1.GotoPosition(motor1_target)
                        
                        self.Motor_Optimization()
                        if self.status == SFGMAIN_STATUS_STOPPED:
                                return 0
                        
                        motor1_pos = numpy.append(motor1_pos,motor1.GetPosition())
                        motor4_pos = numpy.append(motor4_pos,motor4.GetPosition())
                        #print motor1_pos
                        #print motor4_pos
                

                self.Command_GUI((DISPLAY_CALIB,(motor1_pos,motor4_pos,[],[])))
                m1_fit = numpy.polyfit(motor1_pos,motor4_pos,deg=2)
                #print m1_fit
                dm4_dm1_emp = (2*m1_fit[0]*motor1_start_pos + m1_fit[1])
                print dm4_dm1_emp 
                 
                def f(x): return ((3*motor4.Calib[0]*x**2 + 2*motor4.Calib[1]*x+ motor4.Calib[2])/(3*motor1.Calib[0]*x**2 + 2*motor1.Calib[1]*x + motor1.Calib[2])
                                  - dm4_dm1_emp)**2
                l = optimize.fmin(f,2800)
                
                #print l
                
                for motor in SFG_axes.motor_list:
                        motor.GotoPosition(motors_start_pos[int(motor.iAxis.value)])
                
                        
                
                self.Command_GUI((DISPLAY_CALIB,(motor1_pos,motor4_pos,[],[])))
                        
               
                self.Command_GUI((UPDATE_STATUS,"Motors currently at ~"+str(l)))
                self.status = SFGMAIN_STATUS_STOPPED
                self.threadopt= threading.Thread(target=sfgmain.Optimize_Loop)
                self.MMPthread= threading.Thread(target=sfgmain.MonitorMotorPos)
                self.threadopt.start( )
                self.MMPthread.start( )
               

                return 0

             
                
        def MonitorMotorPos(self):
                
                
                logging.debug("started monitor motor positions thread")
                while self.status == SFGMAIN_STATUS_RUNNING:
                        
                        self.Command_GUI((UPDATE_MOTOR_POS,))
                        
                        time.sleep(0.05)
                logging.debug("ended MMP thread")
                return 0

        
        def Command_GUI(self,msg):
                global optwin
                if self.Current_Window == wSFGWIN:
                        sfgwin.queue._put(msg)
                elif self.Current_Window == wOPTWIN:
                        optwin.queue._put(msg)
                
                return 0
        
        

        def periodicCall(self):
                global sfgwin,optwin,errorhandler
                if end_program == False:
                        if self.Current_Window == wSFGWIN:
                                x = 500
                                C = sfgwin
                        elif self.Current_Window == wOPTWIN:
                                x = 20
                                C = optwin
                
                        errorhandler.Queue_Callback()
                        C.Queue_Callback()
                        self.master.after(x,self.periodicCall)
                else:
                        self.master.destroy()
                
                
                        
                return 0

        





class DAQObject(object):
        device_name = "Dev1"
        channel_name = "ai0:1"
        
        def __init__(self):
            return None

        def Reset(self):
                CHK(mx.DAQmxResetDevice(self.device_name))
                return 0 

    
    
        def CollectNShots(self,n):
                
                
#                TH0 = c_ulong()
#                timeout = 10 # in sec.  Time to wait for DAQ to trigger before calling error.
#                sample_rate = 10000.0 # in Hz.  set to max rate of expected trigger 
#                channel_str = self.device_name + "/" + self.channel_name
#               
#
#                max_num_samples = n
#                data = numpy.zeros((2*n,),dtype = numpy.float64)
#
#                CHK(mx.DAQmxCreateTask("",byref(TH0)))
#                logging.debug("Created DAQ Task")
#                CHK(mx.DAQmxCreateAIVoltageChan(TH0,"Dev1/ai0:1","",c_long(-1),c_double(-10),c_double(10),10348,None))
#                
#                logging.debug("Created AI Voltage Channel")
#                
#                CHK(mx.DAQmxCfgSampClkTiming(TH0,"PFI0",c_double(10000.0),10280,10178,c_ulonglong(2*n)))
#                logging.debug("Configed sample timing")
#               
#                CHK(mx.DAQmxStartTask(TH0))
#                
#                read = c_long()
#                
#                if  CHK(mx.DAQmxReadAnalogF64(TH0,max_num_samples,c_double(-1),0,data.ctypes.data,2*max_num_samples,byref(read),None))==-1:                           
#                        CallError(DAQ_ERROR_TIMEOUT)
#                        
#                        mx.DAQmxStopTask(TH0)
#                        mx.DAQmxClearTask(TH0)
#                        return [0,0,0,0]
#                logging.debug("Read")        
#                        
#                
#                SFGdata = data[0:n]
#                IRdata = data[n:2*n]
#                avgSFG = numpy.mean(SFGdata)
#                stdSFG = numpy.std(SFGdata)
#                avgIR = numpy.mean(IRdata)
#                Norm = numpy.mean(SFGdata/IRdata)
#                
#                if numpy.max(SFGdata)>9.9:
#                        CallError(DAQ_ERROR_MAXOUT)
#                        
#                        
#                        
#
#                iRetVal = [avgSFG,avgIR,stdSFG,Norm]
#                        
#                mx.DAQmxStopTask(TH0)
#                mx.DAQmxClearTask(TH0)
#                
#                
#                logging.debug("Data collected successfully.")
                time.sleep(0.1)
                iRetVal = [0,1,2,3]
                return iRetVal


        def CollectHistogram(self,m):
                SFGdata = numpy.ndarray((m,))
                IRdata = numpy.ndarray((m,))
                
                if m<100:
                        
                        return -1
                
                for x in range(11):
                        if x==10:
                        
                                n = m%10
                                if n == 0:
                                        break
                        else:
                                n = m/10
                        self.task = c_ulong()

                        max_num_samples = n
                        data = numpy.zeros((2*max_num_samples,),dtype = numpy.float64)

                        CHK(mx.DAQmxCreateTask("",byref(self.task)))
                        
                        CHK(mx.DAQmxCreateAIVoltageChan(self.task,"Dev1/ai0:1","",c_long(-1),c_double(-10),c_double(10),10348,None))
                        
                        
                        CHK(mx.DAQmxCfgSampClkTiming(self.task,"PFI0",c_double(10000.0),10280,10178,c_ulonglong(2*n)))
                        
                       
                        CHK(mx.DAQmxStartTask(self.task))
                        
                        read = c_long()
                        CHK(mx.DAQmxReadAnalogF64(self.task,max_num_samples,c_double(-1),0,data.ctypes.data,2*max_num_samples,byref(read),None))
                        
                                                     
                        mx.DAQmxStopTask(self.task)
                        
                        

                        mx.DAQmxClearTask(self.task)
                        half = int(data.size/2)
                        SFGdata[:] = data[0:half]
                        IRdata[:] = data[half:]

                try:
                        with open('C:\\Python27\\histogram.csv',"wb") as f:
                                
                               
                                for row in SFGdata:
                                        
                                        
                                        f.write(str(row)+'\n')
                               
                            
                            
                            
                                f.close()

                                
                        
                except IOError:
                        pass
                optwin.queue.put((DISPLAY_HISTOGRAM,(SFGdata,IRdata)))
                return 1
       # def Shutdown(self):
                
                #CHK(mx.DAQmxStopTask(self.task))
                #CHK(mx.DAQmxClearTask(self.task))
                
                #return 0
                

                
           
def CHK(err):
       
        if err<0:
                CallError(0)
                buf_size =100
                buf = create_string_buffer('\000' * buf_size)
                mx.DAQmxGetErrorString(err,byref(buf),buf_size)
                
                logging.warning("NIDAQmx Error number " + str(err) + str(buf.value))
                return -1
        return 0       
        
    
class DAQOptionsWindow(object):
        def __init__(self):
                global installed_modules, DAQ1
                
                self.top =Toplevel()
                self.top.title(string = "DAQ Options")
                
                self.frame  =Frame(master = self.top)
                self.frame.grid(row = 1, column = 0)
                self.info_frame = Frame(master = self.top)
                self.info_frame.grid(row = 0, column = 0)
                
                Label(master = self.info_frame,text = "Device: ").grid(row = 0, column =0)
                self.Device_Label = Label(master = self.info_frame,text = DAQ1.device_name).grid(row = 0, column =1)

                Label(master = self.info_frame,text = "Channel: ").grid(row = 1, column =0)
                self.Device_Label = Label(master = self.info_frame,text = DAQ1.channel_name).grid(row = 1, column =1)
                

                self.Reset_Button = Button(self.frame, text = "Reset Device", command = DAQ1.Reset)
                self.Reset_Button.grid(row = 0, column = 1 )
                return None
     
        
class SFG_MainWindow(object):
        
        
        

        def __init__(self,master):
           
                
                self.master = master
                self.queue = NonredundantQueue()
                self.frame=Frame(master = root,width=200, height=300)
                self.frame.grid(row=1,column=0, padx = 20,pady =5, columnspan = 10)
                

               
                

                

                self.StartButton = Button(self.frame,
                    text = "Start",
                    command=self.StartSpectrum,width=5,height=1)
                self.StartButton.grid(row=1,column=0,sticky=W)
                self.StopButton = Button(self.frame,
                    text = "Stop",
                    command=self.StopSpectrum,
                    width=5,
                    height=1)
                self.StopButton.grid(row=3,column=0,sticky=W)

                self.PauseButton = Button(self.frame,
                    text = "Pause",
                    command=self.Pause,width=5,height=1)
                self.PauseButton.grid(row=5,column=0,sticky=W)

                self.StartFreq_Label = Label(self.frame,width=20,height=1, text = "Start Freq")
                
                self.StartFreq_Label.grid(row=1,column=1)

                self.StopFreq_Label = Label(self.frame,width=20, height = 1, text = "Stop Freq")
                self.StopFreq_Label.grid(row=2,column=1)

                self.NumShots_Label = Label(self.frame,width=20, height = 1, text = "Shots per point")
                self.NumShots_Label.grid(row=3,column=1)

                self.StepSize_Label = Label(self.frame,width=20, height = 1, text = "Step Size")
                
                self.StepSize_Label.grid(row=4,column=1)

                self.NoOfScans_Label = Label(self.frame,width=20, height = 1, text = "No of Scans")
                self.NoOfScans_Label.grid(row=5,column=1)
                
                self.StartFreq_Entry = Entry(self.frame,width=5)
                self.StartFreq_Entry.insert(END,"2800")
                self.StartFreq_Entry.grid(row=1,column=2)

                self.EndFreq_Entry = Entry(self.frame,width=5)
                self.EndFreq_Entry.insert(END,"3600")
                self.EndFreq_Entry.grid(row=2,column=2)

                self.NumShots_Entry = Entry(self.frame,width=5)
                self.NumShots_Entry.insert(END,"10")
                self.NumShots_Entry.grid(row=3,column=2)

                self.StepSize_Entry = Entry(self.frame,width=5)
                self.StepSize_Entry.insert(END,"5")
                self.StepSize_Entry.grid(row=4,column=2)

                self.NoOfScans_Entry = Entry(self.frame,width=5)
                self.NoOfScans_Entry.insert(END,"2")
                self.NoOfScans_Entry.grid(row=5,column=2)

                self.CurrentFreq_Label = Label(self.frame,width=20,height=1, text = "Current Freq")
                
                self.CurrentFreq_Label.grid(row=1,column=3)

                self.ScanNo_Label = Label(self.frame,width=20, height = 1, text = "Current Scan")
                self.ScanNo_Label.grid(row=2,column = 3)

                self.timeremaining_Label = Label(self.frame,width=20, height = 1, text = "Time remaining:")
                self.timeremaining_Label.grid(row=3,column=3)

                self.filename_Label = Label(self.frame,width=20, height = 1, text = "File saved as:")
                self.filename_Label.grid(row=4,column=3)

                
                
                

                self.currentfreq_text = Text(self.frame,width = 5, height = 1)
                self.currentfreq_text.insert(END,StartFreq)
                self.currentfreq_text.grid(row = 1, column =4,sticky = W)

                self.scanno_text = Text(self.frame,width = 5, height = 1)
                self.scanno_text.insert(END,StartFreq)
                self.scanno_text.grid(row = 2, column =4,sticky = W)

                self.timeremaining_text = Text(self.frame, width = 20, height = 1)
                self.timeremaining_text.insert(END,"")
                self.timeremaining_text.grid(row = 3, column =4, sticky = W)

                self.filename_text = Text(self.frame,width = 20, height = 1)
                self.filename_text.insert(END,"")
                self.filename_text.grid(row = 4, column =4,sticky = W)

                self.statusbar = Label(self.frame, bd=1, relief=SUNKEN, anchor=W)
                
                self.statusbar.config(text = "Ready")
                self.statusbar.grid(row=7,column = 0,columnspan = 10)

               
               
               

                

                self.menubar = Menu(root)
                

                self.filemenu = Menu(self.menubar, tearoff=0)
                self.filemenu.add_command(label="Open", command = self.display)
                self.filemenu.add_command(label="Save", command = lambda: SaveSpectrum(sfgwin.MainArray.Array,Spec_name))
                self.filemenu.add_separator()
                self.filemenu.add_command(label="Exit", command = quitproc)

                self.menubar.add_cascade(label="File", menu=self.filemenu)
                
                self.toolsmenu = Menu(self.menubar, tearoff=0)
                self.toolsmenu.add_command(label="Optimize",command = self.Optimize)
                
                self.toolsmenu.add_command(label="Update Scan Parameters",command = self.ScanParameterUpdate)
                self.toolsmenu.add_command(label="Edit Notebook",command = self.NotebookEdit)
                self.toolsmenu.add_command(label="View Log",command = lambda: SFG_Notebook.SFG_LogWindow())
                
                self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)
                
                self.optionsmenu = Menu(self.menubar, tearoff=0)
                self.optionsmenu.add_command(label="Motor Options", command = self.MotorOptions)
                
                self.optionsmenu.add_command(label="DAQ Options", command = self.DAQOptions)
                self.logdebugvar = IntVar()
                self.logdebugvar.set(0)
                self.optionsmenu.add_checkbutton(label = 'Debug mode', variable = self.logdebugvar, command = self.SetLogLevel)
                self.menubar.add_cascade(label="Options", menu=self.optionsmenu)

                
                
                
                root.config(menu= self.menubar)
                
                self.MainArray = SpectrumArray(startfreq = 2800,endfreq = 3600,stepsize = 5)
                self.SFGPlot= MultichannelPlot(root,row = 0,column =0)
                self.IRPlot= MultichannelPlot(root,row = 0, column = 5)
                
                self.SFGPlot.AddChannel(self.MainArray,'SFG', color = 'b')
                self.SFGPlot.AddChannel(self.MainArray,'AvgSFG', color = 'r')
                self.IRPlot.AddChannel(self.MainArray,'AvgIR','r')
               
                return None
        
        def display(self):
                logging.debug(str(threading.enumerate()))
                #SFG_DisplayWindow()
                return 0
        def Queue_Callback(self):
                
                global daily_data_folder
                
                ##"""Handle all messages currently in the queue, if any."""
                while self.queue.qsize():
                        try:
                                msg = self.queue._get()
                                
                                
                                if msg[0] ==UPDATE_STATUS:
                                        self.statusbar.config(text = msg[1])

                                elif msg[0] == PAUSE_SPECTRUM:
                                        PauseFlag.clear()
                                        tkMessageBox.showinfo("Spectrum Paused", "Press to resume collection.")
                                        PauseFlag.set()
                                elif msg[0] == UPDATE_PLOTS:
                                        self.SFGPlot.Update()
                                        self.IRPlot.Update()
                                elif msg[0] == PARAM_UPDATE:
                                        self.ScanParameterUpdate()
                                elif msg[0] == SAVE_SPECTRUM:
                                        if tkMessageBox.askyesno("Save?", "Do you wish to save this spectrum?"):
                                                SaveSpectrum(sfgwin.MainArray.Array,Spec_name)
                                                self.WriteToNotebook(msg[1])
                                        else:
                                                os.chdir(daily_data_folder)
                                                os.remove(Spec_name)
                                elif msg[0] == STOP_SPECTRUM:
                                        self.StopSpectrum()
                                
                                elif msg[0] == UPDATE_FREQ:
                                        self.currentfreq_text.delete(1.0,END)
                                        self.currentfreq_text.insert(END,msg[1])    
                                elif msg[0]== UPDATE_SCANNO:
                                        
                                        self.scanno_text.delete(1.0,END)
                                        self.scanno_text.insert(END,msg[1])
                                elif msg[0]== UPDATE_TIME_REMAINING:
                                        self.timeremaining_text.delete(1.0,END)
                                        self.timeremaining_text.insert(END,msg[1])
                                elif msg[0] == UPDATE_FILENAME:
                                        self.filename_text.delete(1.0,END)
                                        self.filename_text.insert(END,Spec_name)
                                elif msg[0] == WARNING:
                                        tkMessageBox.showwarning("Warning",msg[1])
                                elif msg[0] == KILL_QUEUE:
                                        pass
                                        return 0
                                elif msg[0] == NOTEBOOK:
                                        self.WriteToNotebook()
                                        return 0
                                elif msg[0] == DISABLE_ALL:
                                        self.StartButton.config(state = DISABLED)
                                        self.NumShots_Entry.config(state = DISABLED)
                                        self.StepSize_Entry.config(state = DISABLED)
                                        self.StartFreq_Entry.config(state = DISABLED)
                                        self.EndFreq_Entry.config(state = DISABLED)
                                elif msg[0] == ENABLE_ALL:
                                        self.StartButton.config(state = NORMAL)
                                        self.NumShots_Entry.config(state = NORMAL)
                                        self.StepSize_Entry.config(state = NORMAL)
                                        self.StartFreq_Entry.config(state = NORMAL)
                                        self.EndFreq_Entry.config(state = NORMAL)
                                elif msg[0] == DISPLAY_ERROR_MESSAGE:
                                        ErrorCheck(msg[1])
                                        return 0
                                elif msg[0] == 0:
                                        break
                                
                                        

                                    
                        except Queue.Empty:
                                pass

                
                return 0       
                
                
                return None
        def StartSpectrum(self):
                x = threading.Thread(target=sfgmain.StartSpectrum)
                x.daemon= True
                x.start()
                return 0 
        def DAQOptions(self):
                if sfgmain.status == SFGMAIN_STATUS_RUNNING:
                        tkMessageBox.showwarning("Warning","Spectrum in progress.  Stop spectrum first.")
                else:
                        DAQOptionsWindow()
                return 0
        def MotorOptions(self):
                
                if sfgmain.status == SFGMAIN_STATUS_RUNNING:
                        tkMessageBox.showwarning("Warning","Spectrum in progress.  Stop spectrum first.")
                else:
                        SFG_axes.SFGMotorOptionsWindow()
                return 0
                
        def Optimize(self):
                global optwin, sfgmain
                
                if sfgmain.status == SFGMAIN_STATUS_RUNNING:
                        tkMessageBox.showwarning("Warning","Spectrum in progress.  Stop or pause spectrum before optimizing motors.")
                else:
                        optwin.top.deiconify()
                        
                        root.withdraw()
                       
                        

                        self.threadopt= threading.Thread(target=sfgmain.Optimize_Loop)
                        self.MMPthread= threading.Thread(target=sfgmain.MonitorMotorPos)
                        self.threadopt.start( )
                        self.MMPthread.start( )
                        

                return 0
            
       
        
        def Pause(self):
            
                PauseFlag.clear()
                tkMessageBox.showinfo("Spectrum Paused", "Press to resume collection.")
                PauseFlag.set()
                sfgmain.status == SFGMAIN_STATUS_PAUSED
                
                return 0
            
        def StopSpectrum(self):
                global DAQ1
                if sfgmain.status == SFGMAIN_STATUS_STOPPED:
                        pass
                elif tkMessageBox.askokcancel("Quit", "Do you really wish to cancel spectrum?"):
                        logging.info("Spectrum Aborted")
                        sfgmain.status = SFGMAIN_STATUS_STOPPED
                        return 1
                        
             

                return 0
        

        

        def ScanParameterUpdate(self):
                global CurrentFreq,StartFreq,EndFreq,StepSize,ScanNo,No_of_Scans,NumShots,updateflag

                
                
                if int(self.NumShots_Entry.get())>1000:
                        tkMessageBox.showwarning("Warning","Number of Shots is too high.")
                else:
                        NumShots=int(self.NumShots_Entry.get())


                if int(self.StartFreq_Entry.get())<2000:
                        tkMessageBox.showwarning("Warning", "Start Frequency is suspect.")
                else:
                        StartFreq = int(self.StartFreq_Entry.get())


                if int(self.EndFreq_Entry.get())>4000:
                        tkMessageBox.showwarning("Warning", "End Frequency is suspect.")
                else:
                        EndFreq = int(self.EndFreq_Entry.get())

                if int(self.StepSize_Entry.get())<2:
                        tkMessageBox.showwarning("Warning", "Step size is not valid.")
                else:
                        StepSize = int(self.StepSize_Entry.get())

                if int(self.NoOfScans_Entry.get())<1:
                        tkMessageBox.showwarning("Warning", "Step size is not valid.")
                else:
                        No_of_Scans = int(self.NoOfScans_Entry.get())
                updateflag.set()
                
                return 0
        def WriteToNotebook(self, file_name):
                
                
               
                comment = tkSimpleDialog.askstring("Notebook entry", "Enter notes")
                if comment == None:
                        comment = ""
                SFG_Notebook.AppendNotebook(file_name,comment)
                       
                return 0

        def NotebookEdit(self):
                
                notewin = SFG_Notebook.SFG_NotebookWindow()
                
                return 0
        def SetLogLevel(self):
                if self.logdebugvar.get() == 1:
                        
                        logging.info("Changed to debug logging mode.")
                        logging.getLogger().setLevel(logging.DEBUG)
                else:
                        logging.info("Changed to normal logging mode.")
                        logging.getLogger().setLevel(logging.INFO)
                return 0
        def ReinitializeMotors(self):
                
                if sfgmain.status == SFGMAIN_STATUS_RUNNING:
                        tkSimpleDialog.showwarning("Error","Spectrum in progress.  End spectrum before reinitializing motors.")
                else:
                
        
                        SFG_axes.SaveMotorPositions()
                        logging.info("Saved motor positions")
                        SFG_axes.Close_Motors()
                        comment = tkSimpleDialog.askinteger("Reinitialize motors", "Enter number of motors.")
                        if comment != None:
                                SFG_axes.init_motors(num_of_motors = comment)

                return 0
                        
                        
                        

                

class OptimizeWindow(object):
        global str_motor_list
        
    
    
        def __init__(self):
                
                global optwin,DAQ1,str_motor_list 
                
                self.queue = NonredundantQueue()
                
                
                
                self.top = Toplevel()
                self.top.title(string = "optimize")
                
                self.frame=Frame(self.top)
                self.frame.grid(row = 1, column = 0)
                
                
                self.int_motorpos = IntVar()
                self.int_motorpos.set(Get_Current_Axis_Position())
                
                
                self.MotorPosLabel = Label(self.frame,width =15, height = 2, fg = "blue",textvariable = self.int_motorpos)
                self.MotorPosLabel.grid(row=2,column=2,sticky = W)

               
                self.GotoFrequencyEntry =Entry(self.frame,width=5)
                self.GotoFrequencyEntry.insert(END,"")
                self.GotoFrequencyEntry.bind("<Return>",self.Goto)
                self.GotoFrequencyEntry.grid(row=1,column=1,sticky = W)

               

                self.GotoFrequencyButton = Button(self.frame,
                                text = "Goto",
                                command = lambda:self.Goto(0),
                                width=6,
                                height=1)
  
                self.GotoFrequencyButton.grid(row=2,column=1,sticky=W)

                
                self.VelocityBar = Scale(self.frame,from_ = 1000, to = 0)
                self.VelocityBar.set(10000)
                self.VelocityBar.grid(row  =2 ,column = 5, rowspan = 2,sticky = W)

                self.VelocityLabel = Label(self.frame,width =10, height = 2, fg = "blue",text = "Motor Speed")
                self.VelocityLabel.grid(row=1,column=5,sticky = W)
                self.var_range = IntVar()
                self.var_range.set(0)
                self.rangebox = Checkbutton(self.frame, text = "10x", variable=self.var_range)
                self.rangebox.grid(row = 2, column =6)
                
                    
               
                

                self.ForwardButton = Button(self.frame,
                                text = "Forward",
                                width=6,
                                height=1)
                
                self.ForwardButton.bind("<Button-1>",self.GoForward)
                self.ForwardButton.bind("<ButtonRelease-1>",Stop_Current_Axis)
                self.ForwardButton.grid(row=1,column=3,sticky=W)
                self.ReverseButton = Button(self.frame,
                                text = "Reverse",
                                width=6,
                                height=1)
                
                self.ReverseButton.bind("<Button-1>",self.GoReverse)
                self.ReverseButton.bind("<ButtonRelease-1>",Stop_Current_Axis)
                self.ReverseButton.grid(row=2,column=3,sticky=W)

                

               

                self.SetFrequencyEntry =Entry(self.frame,width=5)
                self.SetFrequencyEntry.insert(END,"")
                self.SetFrequencyEntry.grid(row=2,column=4,sticky = W)

                

  
                self.MPRButton = Button(self.frame,
                        text = "Reset Motor Positions",
                        command=self.ResetMotorPositions,
                        width=15,
                        height=2,
                        wraplength  = 100)
                self.MPRButton.grid(row=1,column=4,sticky=W)

             

                self.var_curr_axis = StringVar()
                self.var_curr_axis.set(SFG_axes.Get_Current_Axis_Name())
                
               
                self.MotorMenu = OptionMenu(self.frame,self.var_curr_axis, *str_motor_list, command = self.UpdateCurrentAxis)
                self.MotorMenu.grid(row = 1,column =2,sticky = W)

                self.statusbar = Label(self.frame, bd=1, relief=SUNKEN, anchor=W)
                
                self.statusbar.config(text = "Ready")
                self.statusbar.grid(row=7,column = 0,columnspan = 10)

                
                self.menubar = Menu(self.top)
                

                self.toolsmenu = Menu(self.menubar, tearoff=0)
                self.toolsmenu.add_command(label="Stats", command = self.CollectHistogram)
                self.toolsmenu.add_command(label="Calibration", command = self.CalibMotor)
                self.toolsmenu.add_command(label="Optimization", command = self.OptimizeMotors)
                self.toolsmenu.add_command(label="Find Frequency", command = self.LocateFrequency)
                self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)
                self.top.config(menu= self.menubar)

                self.BoxcarVar = IntVar()
                self.BoxcarVar.set(1)

                self.BoxcarBar = Scale(self.frame,from_ = 100, to = 1, variable = self.BoxcarVar)
                self.BoxcarBar.bind("<ButtonRelease-1>", self.SetAveraging)
                self.BoxcarBar.grid(row  =2 ,column = 8, rowspan = 2,sticky = W)
                
                self.BoxcarLabel = Label(self.frame,width =15, height = 2, fg = "blue",text = "Boxcar Averaging")
                self.BoxcarLabel.grid(row=1,column=8,sticky = W)
                
                

                
               
                
                self.OptPlot= MultichannelPlot(self.top,0,0)
                self.OptArray = SpectrumArray(startfreq = 0,endfreq = 100,stepsize = 1)
                self.OptPlot.AddChannel(self.OptArray,'SFG','k')
                self.OptPlot.AddChannel(self.OptArray,'IR','r')
                
                
                self.top.protocol("WM_DELETE_WINDOW", optquitproc)

                
                
                return None
        
     

                
        def Queue_Callback(self):
                
                
                
                ##"""Handle all messages currently in the queue, if any."""
                while self.queue.qsize():
                        try:
                                msg = self.queue._get()
                                
                                
                                
                                if msg[0] == UPDATE_PLOTS:
                                        self.OptPlot.Update()
                                elif msg[0] ==UPDATE_STATUS:
                                        self.statusbar.config(text = msg[1])
                                        
                                elif msg[0] == UPDATE_MOTOR_POS:
                                        motor_name= self.var_curr_axis.get() 
                                        self.int_motorpos.set(Get_Current_Axis_Position())
                                elif msg[0] == KILL_QUEUE:
                                        return 0
                                elif msg[0] == DISPLAY_HISTOGRAM:
                                        self.DisplayHistogram(msg[1])
                                elif msg[0] == DISPLAY_CALIB:
                                        self.DisplayCalibPlot(msg[1])
                                elif msg[0] == DISPLAY_ERROR_MESSAGE:
                                        ErrorCheck(msg[1])
                                        return 0


                                    
                        except Queue.Empty:
                                
                                pass

                
                return 0
        def SetAveraging(self,extra):
                global sfgmain
                sfgmain.boxcar_width = self.BoxcarVar.get()
                return 0
        def CalibMotor(self):
                sfgmain.status = SFGMAIN_STATUS_STOPPED
                time.sleep(1)
                
                starting_frequency = tkSimpleDialog.askinteger("Enter start frequency", "")
                ending_frequency = tkSimpleDialog.askinteger("Enter ending frequency","")

                if starting_frequency%50!=0 or ending_frequency%50!=0:
                        tkMessageBox.showwarning("Warning", "Frequencies must be divisible by 50")
                        
                self.hist_window = Toplevel()
                self.hist_window.title("Autocalibration")
                self.button = Button(master = self.hist_window, width = 5, text = 'quit', command  = self.endcalib).pack(side = LEFT)
                self.fig = Figure()
                self.ax1 = self.fig.add_subplot(111)
              
                self.hist_canvas = FigureCanvasTkAgg(self.fig,master = self.hist_window)
                self.hist_canvas.show()
                self.hist_canvas.get_tk_widget().pack()
                
               
                DataThread = threading.Thread(target = sfgmain.Motor_Calibration, args = (SFG_axes.CurrentAxis,))
                DataThread.daemon = True       
                DataThread.start()
                
                return 0
        def OptimizeMotors(self):
                sfgmain.status = SFGMAIN_STATUS_STOPPED
                time.sleep(1)
                        
                self.hist_window = Toplevel()
                self.hist_window.title("Optimization")
                self.button = Button(master = self.hist_window, width = 5, text = 'quit', command  = self.endcalib).pack(side = LEFT)
                self.fig = Figure()
                self.fig.add_subplot(111)
                
                self.hist_canvas = FigureCanvasTkAgg(self.fig,master = self.hist_window)
                self.hist_canvas.show()
                self.hist_canvas.get_tk_widget().pack()
                
               
                DataThread = threading.Thread(target = sfgmain.Motor_Optimization)
                DataThread.daemon = True       
                DataThread.start()
                return 0
        def LocateFrequency(self):
                sfgmain.status = SFGMAIN_STATUS_STOPPED
                time.sleep(1)
                        
                self.hist_window = Toplevel()
                self.hist_window.title("Optimization")
                self.button = Button(master = self.hist_window, width = 5, text = 'quit', command  = self.endcalib).pack(side = LEFT)
                self.fig = Figure()
                self.fig.add_subplot(111)
                #self.fig.add_subplot(222)
                #self.fig.add_subplot(223)
                ##self.fig.add_subplot(224)
                self.hist_canvas = FigureCanvasTkAgg(self.fig,master = self.hist_window)
                self.hist_canvas.show()
                self.hist_canvas.get_tk_widget().pack()
                
               
                DataThread = threading.Thread(target = sfgmain.Frequency_Location)
                DataThread.daemon = True       
                DataThread.start()
                return 0
        def endcalib(self):
                sfgmain.status = SFGMAIN_STATUS_STOPPED
                return 0
        def CollectHistogram(self):
                sfgmain.status = SFGMAIN_STATUS_STOPPED
                
                x = tkSimpleDialog.askinteger("Statistics", "Enter number of shots")
                DataThread = threading.Thread(target = DAQ1.CollectHistogram, args = (x,))
                DataThread.daemon = True       
                DataThread.start()
                
                
                return 0
                
                
        def DisplayHistogram(self,stats_data):
                hist_window = Toplevel()
                hist_window.title("Histogram")
                
                fig = Figure()
                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)
                SFG = ax1.hist(stats_data[0],50)
                IR = ax2.hist(stats_data[1],50)
                 
                SFG_hist = stats_data[0]#numpy.histogram(stats_data[0],50)
                SFG_avg = numpy.mean(stats_data[0])
                SFG_stdev = numpy.std(stats_data[0])
                       
                ax1.text(0, ax1.ylim()[1], "Avg:"+str(SFG_avg), size=15)
                ax1.text(0, ax1.ylim()[1]*0.9, "Stdev:"+str(SFG_stdev), size=15)
                
                
                hist_canvas = FigureCanvasTkAgg(fig,master = hist_window)
                hist_canvas.get_tk_widget().pack()
                hist_canvas.draw()
                toolbar = NavigationToolbar2TkAgg(hist_canvas, hist_window)
                toolbar.update()
                hist_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
                self.SaveHistogram(SFG_hist)
                self.StartThread()
                
                
                
                return 0

        def DisplayCalibPlot(self,data):
                self.fig.axes[0].cla()
                self.fig.axes[0].plot(data[0],data[1],'s')
                self.fig.axes[0].plot(data[2],data[3],'-')
                
                
                self.hist_canvas.draw()
                return 0 
                
        def SaveHistogram(self, histogram_data):
        
                # Saves data from a histogram object into a csv file.  
                import csv
                
                from datetime import date
                
                date_str = date.today().strftime("%y%m%d")
                target_dir = "C:\\sfg\\data\\" + date_str
                if os.path.exists(target_dir) is False:
                        logging.warning("Save directory does not exist")
                        CallError(DATA_DIRECTORY_NOT_FOUND)
                        return DATA_DIRECTORY_NOT_FOUND
                else:
                        os.chdir(target_dir)
                 
                                
                file_name = "histogram.csv"
                with open(file_name,"wb") as f:
                        CSV_FILE = csv.writer(f,dialect = 'excel')
                        
                                        
                        
                        #for i in histogram_data[0]:
                                
                                #flat = str(i) #= histogram_data[0][i]#[histogram_data[0][i],histogram_data[1][i]]
                                #CSV_FILE.writerow(flat)
                       
                    
                    
                    
                        f.close()

                                
                        

                       
            
                return 0
                             
        def UpdateCurrentAxis(self,motor_name):
                               
                Set_Current_Axis(motor_name)
                self.int_motorpos.set(Get_Current_Axis_Position())
                self.VelocityBar.from_ = 1000
                
                logging.debug("Current axis: "+ motor_name)
                return 0
                                      
        def StartThread(self):
                
                
                DataThread = threading.Thread(target = sfgmain.Optimize_Loop)
                DataThread.daemon = True       
                DataThread.start()
                return 0
                
       
        
        def GoForward(self,extra):
                
              
                velocity = self.VelocityBar.get()*(10**int(self.var_range.get()))
                
                Move_Current_Axis(1,velocity)
                 
                return None
        def GoReverse(self,extra):
                
               
               
                velocity = self.VelocityBar.get()*(10**int(self.var_range.get()))
                
                Move_Current_Axis(-1,velocity)
                 
                return 0
     
        
        
        def Goto(self,extra):
                
                target = int(self.GotoFrequencyEntry.get())
                if target>4000 or target<2600:
                        tkMessageBox.showwarning("Warning","Target frequency is out of range.")
                else:
                        SFG_axes.SetMotorMotionParam()
                        GotoWavenumber(target)
                        
                
                        
                return 0
        def ResetMotorPositions(self):
                
                
                if tkMessageBox.askokcancel("Reset Motor Positions", "Do you really wish reset the motor positions?"):
                        
                        try:
                                tFreq = int(self.SetFrequencyEntry.get())
                                if SetWavenumber(tFreq)==0:
                                        logging.info("motor positions reset")
                                
                        except IOError:
                                CallError(MOTOR_POSITION_RESET_ERROR)
                                return -1
                        
                return 0       
        
                        
            

        
        
def optquitproc():
    
    global optwin
    sfgmain.status = SFGMAIN_STATUS_STOPPED
    
    optwin.top.withdraw()
    root.deiconify()
    sfgmain.status = SFGMAIN_STATUS_STOPPED
    
    
    
    return None
        

                
                


      
                
                

       
        
def GetSpectrumName():

        #returns a string with filename for next spectrum in the data folder
        global daily_data_folder
        
        from datetime import date
        
        date_str = date.today().strftime("%y%m%d")
        
        target_dir = 'C:\\sfg\\data'
        
        if os.path.exists(target_dir) is False:
                logging.warning("Save directory does not exist")
                return DATA_DIRECTORY_NOT_FOUND
        else:
                os.chdir(target_dir)
        folder_list = os.listdir(target_dir)
        daily_data_folder = 'C:\\sfg\\data\\'+date_str
        if os.path.exists(date_str) is False:
                logging.info("created the day's folder"+ date_str)
                os.mkdir(daily_data_folder)
        
        os.chdir(daily_data_folder)
        file_list = os.listdir('.')
        
        if len(file_list)==0:
                next_file = date_str+"01"+'.csv'
        else:
                file_no = 1
                next_file_try = str(int(date_str)*100+file_no)+'.csv'
                while next_file_try in file_list:
                        file_no+=1
                        next_file_try = str(int(date_str)*100+file_no)+'.csv'
                next_file = next_file_try

        return next_file

    





def CalculateTargetFreq(curr,start,end,step,scanno,noscans):
        clearplot = 0
       
        if scanno == 0: #very first data point
            scanno+=1
            return [start,scanno,clearplot]

        elif isEven(scanno)==0:
            if curr == end:
                scanno+=1
                clearplot =1
                if scanno>noscans:
                    sfgmain.status=SFGMAIN_STATUS_STOPPED
                    return [0,0]
                else:
                    return [curr,scanno,clearplot]
            else:
                return  [(curr+step),scanno,clearplot]

        elif isEven(scanno)==1:
            if curr == start:
                scanno+=1
                clearplot = 1
                if scanno>noscans:
                    sfgmain.status=SFGMAIN_STATUS_STOPPED
                    return [0,0]
                else:
                    return [curr,scanno,clearplot]
            else:
                return  [(curr-step),scanno,clearplot]


        else:
                CallError(TARGET_FREQ_CALC_ERROR)
                return TARGET_FREQ_CALC_ERROR





def isEven(number):
    if number%2==0:
       return 1
    else:
        return 0


def quitproc():
        global end_program,sfgmain
        
        if sfgmain.status == SFGMAIN_STATUS_RUNNING:
            
                if sfgwin.StopSpectrum()==0:
                        return 0
               
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        
                
                SFG_axes.SaveMotorPositions()
                logging.info("Saved motor positions")
                
                SFG_axes.Close_Motors()
                SFG_Run_Status.Update_Status(False)
                logging.shutdown()
                end_program = True
                #on 'end_program' being set to True, SFGControl's PeriodicCall function kills root thread. 
                
                
        return 0






if SFG_Run_Status.Check_Status() == True:
        tkMessageBox.showwarning("Error","An instance of SFGMe is already running.")
        
        
else:
        
        SFG_Run_Status.Update_Status(True)
        
        SFG_Notebook.initialize_logging()
        logging.info("program start")
        
        root = Tk()
        root.title(string  = "SFGme")
        
        sfgwin = SFG_MainWindow(root)
        
        
        
        
        errorhandler = ErrorHandler(root,ErrorQueue)
        
        sfgmain = SFG_Control(root)
        root.protocol("WM_DELETE_WINDOW", quitproc)
        optwin = OptimizeWindow()
        optwin.top.withdraw()
        
     

        root.mainloop()


