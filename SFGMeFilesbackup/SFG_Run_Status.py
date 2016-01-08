import os
from SFG_Error import *

def Check_Status():  # Checks if other SFG_Me instances are running
                
        
                    
        
        
        
        target_dir = "C:\\sfg\\control_files"
        #if os.path.exists(target_dir) is False:
                
                #return CONTROL_FILE_DIRECTORY_NOT_FOUND
        #else:
                #os.chdir(target_dir)

        
        try:
                os.chdir(target_dir)
                with open("SFG_Me_RunStatus.txt","rb") as f:
                        status_string = f.readline()
                        
                        if status_string == "running":
                                f.close()
                                return True
                        elif status_string == "not running":
                                f.close()
                                return False
        except IOError:
                CallError(RUN_STATUS_FILE_NOT_FOUND)
                return RUN_STATUS_FILE_NOT_FOUND
        except WindowsError:
                CallError(CONTROL_FILE_DIRECTORY_NOT_FOUND)
                return CONTROL_FILE_DIRECTORY_NOT_FOUND

        return 0

def Update_Status(bool_status):
        
        target_dir = "C:\\sfg\\control_files"
       

       
        try:
                os.chdir(target_dir)
                with open("SFG_Me_RunStatus.txt","wb") as f:
                        if bool_status == False:
                                f.write("not running")
                        else:
                                f.write("running")
                        f.close()
        except IOError:
                CallError(UPDATE_RUN_STATUS_ERROR)
                return UPDATE_RUN_STATUS_ERROR
        except WindowsError:
                CallError(CONTROL_FILE_DIRECTORY_NOT_FOUND)
                return CONTROL_FILE_DIRECTORY_NOT_FOUND
        return 0


