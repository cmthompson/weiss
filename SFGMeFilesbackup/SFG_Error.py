# contains error codes for SFGME program
from Tkinter import *
import tkMessageBox
import Queue

CALIB_LOAD_ERROR = -101
POSITION_LOAD_ERROR = -102
POSITION_SAVE_ERROR  = -103
MOTOR_TIMEOUT = -104
PARAM_FILE_NOT_FOUND = -105
POSITION_FILE_NOT_FOUND = -106
MOTORS_IN_MOTION = -107
CALIB_SAVE_ERROR = -108
FREQ_OUT_OF_RANGE = -109
MOTOR_INIT_FAILED = -110

NOTEBOOK_LOAD_ERROR = -200
NOTEBOOK_SAVE_ERROR = -201
NOTEBOOK_APPEND_ERROR = -202
LOG_LOAD_ERROR = -203

DAQ_ERROR_TIMEOUT = -300
DAQ_ERROR_MAXOUT = -301

UPDATE_RUN_STATUS_ERROR = -400
RUN_STATUS_FILE_NOT_FOUND = -401
DUPLICATE_SFGME_INSTANCE = -402


SPECTRUM_SAVE_ERROR = -1000
TARGET_FREQ_CALC_ERROR = -1001
DATA_DIRECTORY_NOT_FOUND = -1002
CONTROL_FILE_DIRECTORY_NOT_FOUND = -1003
SPECTRUM_IN_PROGRESS = -1004



class NonredundantQueue(Queue.Queue):

        def _init(self,maxsize):
                Queue.Queue._init(self, maxsize) 
                return None
        
        def _put(self, item):
                if item not in self.queue:
                        
                        Queue.Queue._put(self, item)
               
                        
            
                return 0

        def _get(self):
                try:
                        x = Queue.Queue._get(self)
                except IndexError:
                        return 0
            
            
                return x





def CallError(error):
        ErrorQueue.put(error)
        return 0

class ErrorHandler(object):
        def __init__(self,master,queue):
                self.master = master
                self.queue = queue
                return None
        def Queue_Callback(self):
                while self.queue.qsize():
                        try:
                                error = self.queue._get()
                               
                                if error == 0:
                                        pass
                                elif error == CALIB_LOAD_ERROR:
                                        tkMessageBox.showwarning("Error", "Error while loading calibration parameters.")
                                elif error == POSITION_LOAD_ERROR:
                                        tkMessageBox.showwarning("Error", "Error while loading motor positions.")
                                elif error == POSITION_SAVE_ERROR:
                                        tkMessageBox.showwarning("Error", "Error while saving motor positions.")        
                                elif error == MOTOR_TIMEOUT:
                                        tkMessageBox.showwarning("Error", "Motors took longer than ten seconds to reach target.")
                                elif error ==PARAM_FILE_NOT_FOUND:
                                        tkMessageBox.showwarning("Error", "Motor calibration file not found.'mcalib.csv' should be in 'C:\sfg\control_files'.")
                                elif error ==POSITION_FILE_NOT_FOUND:
                                        tkMessageBox.showwarning("Error", "Motor position file not found.  'mpositions.csv' should be in 'C:\sfg\control_files'.")
                                elif error == MOTORS_IN_MOTION:
                                        tkMessageBox.showwarning("Error", "Motors are still in motion. Requested operation cancelled.")

                                elif error == CALIB_SAVE_ERROR:
                                        tkMessageBox.showwarning("Error", "Error while saving calibration parameters.")

                                elif error == NOTEBOOK_LOAD_ERROR:
                                        tkMessageBox.showwarning("Error",  "Could not load notebook file.  File is already open or cannot be found.")
                                elif error == NOTEBOOK_SAVE_ERROR:
                                        tkMessageBox.showwarning("Error",  "Could not save notebook file.  File is already open or cannot be found.")
                                elif error == NOTEBOOK_APPEND_ERROR:
                                        tkMessageBox.showwarning("Error", "Could not append to notebook file.  File is already open or cannot be found.")
                                elif error == NOTEBOOK_LOAD_ERROR:
                                        tkMessageBox.showwarning("Error",  "Could not load log file.  File is already open or cannot be found.")
                                elif error == DAQ_ERROR_TIMEOUT:
                                        tkMessageBox.showwarning("Error",  "DAQ timed out.  Check triggering and that collection time does not excced 10 seconds.")
                                elif error == DAQ_ERROR_MAXOUT:
                                        tkMessageBox.showwarning("Error",  "DAQ maxed out.  Check that signal into Ch0 of DAQ does not exceed 10 volts.")
                                elif error == SPECTRUM_SAVE_ERROR:
                                        tkMessageBox.showwarning("Error",  "Error saving spectrum.  Target file may already be open.")
                                elif error == SPECTRUM_IN_PROGRESS:
                                        tkMessageBox.showwarning("Error",  "Spectrum in progress.")
                                elif error == TARGET_FREQ_CALC_ERROR:
                                        tkMessageBox.showwarning("Error",  "Error in calculating target frequency.")
                                elif error == DATA_DIRECTORY_NOT_FOUND:
                                        tkMessageBox.showwarning("Error",  "Data directory, 'C:/sfg/data', could not be found.")
                                elif error == UPDATE_RUN_STATUS_ERROR:
                                        tkMessageBox.showwarning("Error",  "Error updating the SFG run status in 'SFG_Me_RunStatus.txt'.")
                                elif error == RUN_STATUS_FILE_NOT_FOUND:
                                        tkMessageBox.showwarning("Error",  "Could not find SFG_Me_RunStatus.txt")
                                elif error == CONTROL_FILE_DIRECTORY_NOT_FOUND:
                                        tkMessageBox.showwarning("Error",  "Could not find control file directory, 'C:/SFG/control_files'.")
                              
                                       
                                elif error == FREQ_OUT_OF_RANGE :
                                        tkMessageBox.showwarning("Error","Target frequency is out of range.")

                                elif error == LOG_LOAD_ERROR :
                                        tkMessageBox.showwarning("Error","Error loading log file 'C:/sfg/control_files/SFGlog.log'")


                                        
                                else:
                                        tkMessageBox.showwarning("Error", "Uncatalogued Error number " + str(error))
                                
                        


                                    
                        except Queue.Empty:
                                
                                pass
                return 0


ErrorQueue = NonredundantQueue()

        



