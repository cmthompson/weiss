# SFG_axes.py is an API for motor control in the SFG program

from Tkinter import *
from ctypes import *
import time
from SFG_Error import *
import time
import logging
import XPS_Q8_drivers
import numpy





MCModePosition = c_ushort(2)
MCModeVelocity = c_ushort(4)
MCForward = c_ushort(1)
MCReverse = c_ushort(2)





class axis:
        
        iAxis =0
        AxisName = ""
        Calib = [0,0,0,-1]
        
        
            
        def __init__(self,axis):
                self.SetAxis(axis)
                print socketId
                
                 # Kill the group
                [errorCode, returnString] = myxps.GroupKill(socketId, self.group)
                if (errorCode != 0):
                    displayErrorAndClose (socketId, errorCode, 'GroupKill')
                    
                # Initialize the group
                
                [errorCode, returnString] = myxps.GroupInitialize(socketId,self.group)
                if (errorCode != 0):
                    displayErrorAndClose (socketId, errorCode, 'GroupInitialize')
                    return None
                print 'search home'
                [errorCode, returnString] = myxps.GroupHomeSearch(socketId,self.group)
                if (errorCode != 0):
                    displayErrorAndClose (socketId, errorCode, 'GroupHomeSearch')
                    return -1
                
                
               
             
                return None
        
        def SetAxis(self,axis):
                
                self.AxisName = "motor"+str(axis)
                self.group = 'SP'+str(axis)
                self.iAxis = self.group + '.Pos' +str(axis)
                self.Velocity = 20
                self.AxisNumber = axis                
                
                
                return 0
        def SetMotionParam(self):
                pass
                       
                       
                return 0
        def GetStatus(self):
                print self.group
                [errorCode, currentStatus] = myxps.GroupStatusGet(socketId, self.group)
                if (errorCode != 0):
                    displayErrorAndClose (socketId, errorCode,'GroupStatusGet')
                    return -1
               
                return currentStatus
        
        
        def SetPosition(self,target):
                
                pass
                
                return 0
        

        def GetPosition(self):
                [errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, self.iAxis, 1)
                if (errorCode != 0):
                    displayErrorAndClose (socketId, errorCode,'GroupPositionCurrentGet')
                    return -1
                else:
                    print 'Positioner ' + self.AxisName + ' is in position ' + str(currentPosition)
          
                  
                return currentPosition

        def GetVelocity(self):

                pass
                  
                return 0   

        def GotoPosition(self,x):
                logging.debug('Moving motor ' + str(self.AxisName)+ ' to '+str(x))
                [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId,self.group, [float(x)])
                if (errorCode != 0):
                    displayErrorAndClose(socketId, errorCode,'GroupMoveAbsolute')
                              
                return 0

        def SetFrequency(self,x):

                target = self.Calib[0] + self.Calib[1]*x + self.Calib[2]*(x**2)+ self.Calib[3]*(x**3)
                self.SetPosition(target)
                logging.debug('Setting position of motor ' + str(self.AxisName)+ ' to '+str(target))
                 
                return target 

        def GotoFrequency(self,x):
                
                if x <2700 or x>4000:
                        CallError(FREQ_OUT_OF_RANGE)
                        return FREQ_OUT_OF_RANGE
                target = self.Calib[0] + self.Calib[1]*x + self.Calib[2]*(x**2)+ self.Calib[3]*(x**3)
                self.GotoPosition(target)
                logging.debug('motor ' + str(self.AxisName)+ ' moving to '+str(target))
                return 0
            
        def Move(self,selected_direction,selected_velocity):
                pass
#                [errorCode, returnString] = myxps.GroupJogModeEnable(socketId,self.group)
#                if (errorCode != 0):
#                    displayErrorAndClose(socketId, errorCode, 'GroupJobModeEnable')
#                    return -1 
#                [errorCode, returnString] = myxps.GroupJogParametersSet(socketId,self.group,selected_direction*selected_velocity,20)
#                if (errorCode != 0):
#                    displayErrorAndClose(socketId, errorCode, 'GroupJobModeParameterSet')
#                    return -1  

                         
                return 0

        def Stop(self):
                pass

#                [errorCode, returnString] = myxps.GroupJogParametersSet(socketId,self.group,0,20)
#                if (errorCode != 0):
#                    displayErrorAndClose(socketId, errorCode, 'GroupJobModeParameterSet')
#                    return -1 
#                [errorCode, returnString] = myxps.GroupJogModeDisable(socketId,self.group)
#                if (errorCode != 0):
#                    displayErrorAndClose(socketId, errorCode, 'GroupJobModeDisable')
#                    return -1 
   
                return 0
                
        def Abort(self):
                pass
#                [errorCode, returnString] = myxps.GroupMoveAbort(socketId,self.group)
#                if (errorCode != 0):
#                    displayErrorAndClose(socketId, errorCode, 'GroupMoveAbort')
#                    return -1 
                return 0  
        
class CalibEntryWindow:
        LineList = []
        Kill = 1
        ParamList = []

        def __init__(self,master,file_name):
                
                self.file_name = file_name
                self.master = master
                
                self.P1 = Toplevel()
                self.frame=Frame(master = self.P1)
                self.frame.grid(row=0, padx = 5,pady =5)

                self.motor_Label = Label(self.frame,width=20, height = 1, text = "motor #")
                self.motor_Label.grid(row=0,column=0)

                self.a1_Label = Label(self.frame,width=20, height = 1, text = "a1")
                self.a1_Label.grid(row=0,column=1)

                self.a2_Label = Label(self.frame,width=20, height = 1, text = "a2")
                self.a2_Label.grid(row=0,column=2)

                self.a3_Label = Label(self.frame,width=20, height = 1, text = "a3")
                self.a3_Label.grid(row=0,column=3)

                self.a4_Label = Label(self.frame,width=20, height = 1, text = "a4")
                self.a4_Label.grid(row=0,column=4)

                for a in motor_list:
                        self.LineList.append(CalibEntryLine(self.P1,a.AxisNumber,a))
                

                
                
                #self.LoadButton = Button(self.P1,
                  #  text = "Load from file",
                  #  command = self.Load,
                
                   # height=1)
                #self.LoadButton.grid(row=1,column=1,sticky=W)

                self.SaveButton = Button(self.P1,
                    text = "Save",
                    command = self.Save,
                
                    height=1)
                self.SaveButton.grid(row=0,column=1,sticky=W)

                self.Load()
               
                
                return None
        
       
        
        
        def Load(self):
                
                        
                for line in self.LineList:
                        
                   
                        line.a1_var.set(str(line.motor.Calib[0]))
                        
                        line.a2_var.set(str(line.motor.Calib[1]))
                        
                        line.a3_var.set(str(line.motor.Calib[2]))
                        
                        line.a4_var.set(str(line.motor.Calib[3]))
                               
                        
                return 0
        def Save(self):
                
                      
                import csv, os
                for a in motor_list:
                        a.Calib = [float(self.LineList[a.AxisNumber-1].a1_Entry.get()),float(self.LineList[a.AxisNumber-1].a2_Entry.get()),float(self.LineList[a.AxisNumber-1].a3_Entry.get()),float(self.LineList[a.AxisNumber-1].a4_Entry.get())]
                        
                try:                
                        with open(self.file_name,"wb") as f:
                                CSV_FILE = csv.writer(f,dialect = 'excel')

                                header_list= ["motor","a1","a2","a3","a4"]
                                
                                
                                CSV_FILE.writerow(header_list)
                                for line in self.LineList:
                                        
                                        param_row=[str(a.AxisNumber),str(0),str(0),str(0),str(0)]
                                        for a in motor_list:
                                                if a.AxisNumber == line.motor_num:
                                
                                                        param_row = [str(a.AxisNumber),str(a.Calib[0]), str(a.Calib[1]), str(a.Calib[2]), str(a.Calib[3])]
                 
                                                       
                                               
                                                        
                                        CSV_FILE.writerow(param_row)

                                f.close()
                except IOError:
                        CallError(CALIB_SAVE_ERROR)
                        return CALIB_SAVE_ERROR

               
                return 0

class CalibEntryLine:

        def __init__(self,master,motor_num, motor):
                self.master = master
                self.motor = motor
                self.motor_num = motor_num
                self.frame=Frame(master = self.master, width = 1000)
                self.frame.grid(column = 0, columnspan = 9, sticky = W)
                
                self.motor_Entry = Label(self.frame,width=20, height = 1, text = self.motor.AxisName)
                self.motor_Entry.grid(row=0,column=0)

                self.a1_var = StringVar()
                self.a1_var.set(str(motor.Calib[0]))
                self.a1_Entry = Entry(self.frame,width=20, textvariable = self.a1_var)
                self.a1_Entry.grid(row=0,column=2)

                self.a2_var = StringVar()
                self.a2_var.set("0")    
                self.a2_Entry = Entry(self.frame,width=20,textvariable = self.a2_var)
                self.a2_Entry.grid(row=0,column=4)

                self.a3_var = StringVar()
                self.a3_var.set("0")
                self.a3_Entry = Entry(self.frame,width=20,textvariable = self.a3_var)
                self.a3_Entry.grid(row=0,column=6)

                self.a4_var = StringVar()
                self.a4_var.set("0")
                self.a4_Entry = Entry(self.frame,width=20,textvariable = self.a4_var)
                self.a4_Entry.grid(row=0,column=8)

                
                return None
#########################
motor_list = []

def displayErrorAndClose (socketId, errorCode, APIName):
    global myxps
    if (errorCode != -2) and (errorCode != -108):
        [errorCode2, errorString] = myxps.ErrorStringGet(socketId,
        errorCode)
        if (errorCode2 != 0):
            print APIName + ': ERROR ' + str(errorCode)
        else:
            print APIName + ': ' + errorString
    else:
        if (errorCode == -2):
            print APIName + ': TCP timeout'
        if (errorCode == -108):
            print APIName + ': The TCP/IP connection was closed by an administrator'
    myxps.TCP_CloseSocket(socketId)
    return 0


def EnableAllMotors(): return 0
                          
                



def Stop_All_Motors():
                for a in motor_list:
                    a.Abort()
                    
                return 0

            
def init_motors(num_of_motors):
        global socketId, myxps, motor_list,hCtlr,CurrentAxis
        serv_address =  '192.168.0.254'
        print 'using server address' + serv_address
        
        
        motor_list = []
        str_motor_list =[]
        
       
                 # opens motor controller handle
               # Instantiate the class
        myxps = XPS_Q8_drivers.XPS()
        # Connect to the XPS
        socketId = myxps.TCP_ConnectToServer(serv_address, 5001, 20)
        # Check connection passed
        if (socketId == -1):
            print 'Connection to XPS failed, check IP & Port'
            return str_motor_list

        
           
        for i in range(num_of_motors):
                motor_list.append(axis(i+1))

                         
                   
      
        for a  in motor_list:
                str_motor_list.append(a.AxisName)
        
 
            
       
                
        
        
        
        #Load_Motor_Positions("mpositions.csv") 
        #Load_Calibration_Parameters("mcalib.csv", motor_list)           #Load motor calibration curves from mcalib.csv
        
        motor_list[0].Calib = [1,0.001,0,0]            #These listed incase the file gets lost
        #motor_list[1].Calib = [-23461, 6.7026, 9.0507e-4, -1.2646e-7]
        #motor_list[2].Calib = [-6563.6, 20.773, -5.2874e-3, 3.0866e-7]
        #motor_list[3].Calib = [-12307, -4.4513, 6.52e-4, 1.27e-7]    
        #motor_list[4].Calib = [182900,-63.1514,0,0]
    
        CurrentAxis = motor_list[0]
        
        return str_motor_list

def RestoreInitialPositions():
        initial_motor_pos

        if tkMessageBox.askokcancel("Reset?", "Do you wish to reset motor positions?"):
        
                for a in motor_list:
                        a.SetPosition(initial_motor_pos[motor_list.index(a)])
        return 0


def GotoWavenumber(tFreq):
        start = time.time()
        time_elapsed = 0
        logging.debug("Moving motors to " + str(tFreq))
        
        for a in (motor_list):
                print a
                
                a.GotoFrequency(tFreq)
          
#        for a in reversed(motor_list):  #reversed because motor5 (monochromator) takes the longest)
#                
#                while a.GetStatus != 12:
#                        
#                        time.sleep(0.3)
#                        time_elapsed+=0.3
#                        
#                        
#                       
#                        if time_elapsed>10:  # if motors have not reached position after 10 seconds...
#                                Stop_All_Motors()
#                                logging.info("motors timed out")
#                                CallError(MOTOR_TIMEOUT)
#                                return MOTOR_TIMEOUT
        
        logging.debug("Motors reached target")
        #Stop_All_Motors()
        
                          
        return 0
        
def SetMotorMotionParam():
        for a in (motor_list):
                a.SetMotionParam()
        return 0


def SetWavenumber(tFreq):
        global motor_list
#        for a in motor_list:
#            
#                if mcapi32.MCIsStopped(hCtlr,a.iAxis,c_double(0.1))<=0:
#                        return -4
        
        for a in motor_list:
                
                a.SetFrequency(tFreq)
               
        return 0

def Set_Current_Axis(str_motor_name):
        global CurrentAxis
        for a in motor_list:
                if a.AxisName == str_motor_name:
                        CurrentAxis = a
                        
        
        return 0
        

def Move_Current_Axis(selected_direction,selected_velocity):
        CurrentAxis.Move(selected_direction,selected_velocity)
        return 0
        
def Stop_Current_Axis(extra):
        CurrentAxis.Stop()
        return 0

def Get_Current_Axis_Position():
        return int(CurrentAxis.GetPosition())
        
def Get_Current_Axis_Max_Velocity():
        return CurrentAxis.Velocity
        
def Get_Current_Axis_Name():
        return CurrentAxis.AxisName


def Load_Calibration_Parameters(file_name,motor_list):
        import os, csv

       
        try:
                        pos = numpy.loadtxt("C:\\sfg\\control_files\\mcalib.csv",delimiter = ',',skiprows = 1)
                        for row in pos:
                                for a in motor_list:
                                                                
                                        if a.AxisNumber == int(row[0]):                    
                                                a.Calib = list(row[1:])
                                                
        except IOError:
                CallError(POSITION_LOAD_ERROR)
        except ValueError:
                CallError(POSITION_LOAD_ERROR)
                return CALIB_LOAD_ERROR

               
                
        
        return 0

def Load_Motor_Positions(file_name,oldway = False):
        import os, csv
        global motor_list
        target_dir = 'C:\\sfg\\control_files'
        os.chdir(target_dir)
        if oldway:
                try:
                        
                        with open(file_name,"rb") as f:

                                CSV_READER = csv.reader(f,dialect = 'excel')
                                for row in CSV_READER: 
                                        if row[0] == "motor":
                                                pass
                                        else:
                                                i = int(row[0])
                                                for a in motor_list:
                                                        
                                                        if a.AxisNumber == i:
                                                                
                                                                a.SetPosition(float(row[1]))
                                                                
                                    
                                f.close()
                except IOError:
                        CallError(POSITION_LOAD_ERROR)
                except ValueError:
                        CallError(POSITION_LOAD_ERROR)
        else:
                try:
                        pos = numpy.loadtxt("C:\\sfg\\control_files\\mpositions.csv",delimiter = ',',skiprows = 1)
                        for row in pos:
                                for a in motor_list:
                                                                
                                        if a.AxisNumber == int(row[0]):                    
                                                a.SetPosition(row[1])
                                                
                except IOError:
                        CallError(POSITION_LOAD_ERROR)
                except ValueError:
                        CallError(POSITION_LOAD_ERROR)
        pos_list = str()
        for a in motor_list:
                pos_list+=(","+str(a.GetPosition()))
                
                
        logging.info("Loaded Motor Positions" + pos_list)
        return 0

def SaveMotorPositions(oldway=False):      
        import csv, os
        global motor_list
        Stop_All_Motors()
        target_dir = 'C:\\sfg\\control_files'
        os.chdir(target_dir)
        file_name = "mpositions.csv"
        if oldway:
                try:
                        with open(file_name,"wb") as f:
                                CSV_FILE = csv.writer(f,dialect = 'excel')
                                header_list= ["motor","position"]
                                CSV_FILE.writerow(header_list)   
                                for a in motor_list:
                                        
                                        CSV_FILE.writerow([int(a.iAxis[-1]),a.GetPosition()])

                                f.close()
                except IOError:
                        CallError(POSITION_SAVE_ERROR)
                        return POSITION_SAVE_ERROR
        else:   ###using the new way.
                
                mpos_array = numpy.ndarray((len(motor_list),2))
                for a in motor_list:
                        
                        mpos_array[int(a.iAxis[-1])-1] = numpy.array([[int(a.iAxis[-1]),a.GetPosition()]])
                        
                        numpy.savetxt("C:\\sfg\\control_files\\mpositions.csv",mpos_array,delimiter = ',',header = 'motor,position')
                    
       
        return 0


def Close_Motors():
        global socketId
        myxps.TCP_CloseSocket(socketId)
        return 0
        
def TestCode():
    global myxps, socketId
    # Instantiate the class
    myxps = XPS_Q8_drivers.XPS()
    # Connect to the XPS
    socketId = myxps.TCP_ConnectToServer('192.168.0.254', 5001, 20)
    # Check connection passed
    if (socketId == -1):
        print 'Connection to XPS failed, check IP & Port'
        sys.exit ()
    # Add here your personal codes, below for example:
    # Define the positioner
    group = 'SP1'
    positioner = 'SP1.Pos1'
    # Kill the group
    [errorCode, returnString] = myxps.GroupKill(socketId, group)
    if (errorCode != 0):
        displayErrorAndClose (socketId, errorCode, 'GroupKill')
        sys.exit ()
    # Initialize the group
    print 'initializing group'
    [errorCode, returnString] = myxps.GroupInitialize(socketId,group)
    if (errorCode != 0):
        displayErrorAndClose (socketId, errorCode, 'GroupInitialize')
        return -1
    # Home search
    print 'search home'
    [errorCode, returnString] = myxps.GroupHomeSearch(socketId,group)
    if (errorCode != 0):
        displayErrorAndClose (socketId, errorCode, 'GroupHomeSearch')
        return -1
    # Make some moves
    
    for index in range(3):
    # Forward
        [errorCode, returnString] = myxps.GroupMoveRelative(socketId,positioner, [20.0])
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode,'GroupMoveAbsolute')
            return -1
        # Get current position
        [errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode,'GroupPositionCurrentGet')
            return -1 ()
        else:
            print 'Positioner ' + positioner + ' is in position ' + str(currentPosition)
    # Backward
    for index in range(10):
        [errorCode, returnString] = myxps.GroupMoveRelative(socketId,positioner, [-20.0])
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode,'GroupMoveAbsolute')
            return -1
        # Get current position
        [errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode,'GroupPositionCurrentGet')
            return -1
        else:
            print 'Positioner ' + positioner + ' is in position ' + str(currentPosition)
    # Close connection
    myxps.TCP_CloseSocket(socketId)
    #----------- End of the demo program ----------#
    return 0

def testout():
    init_motors(1)
    r = motor_list[0]
    
    
    print 'trying velocity mode'
    r.Move(1,10)
    time.sleep(10)
    r.Stop()
    Close_Motors()
    return 0
    
                

