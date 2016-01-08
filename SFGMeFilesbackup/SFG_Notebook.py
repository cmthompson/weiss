import os
from datetime import date
import Tkinter
from SFG_Error import *
import logging

class SFG_NotebookWindow:
        
        
        

        def __init__(self,target_dir = None , target_file = None):
                if target_file == None:
                    if target_dir == None:
                        
                        self.target_dir = "C:\\sfg\\data\\" + date.today().strftime("%y%m%d")
                        self.nb_filename = self.target_dir[-6:]+'_notes.txt' 
                    else:
                        self.target_dir = target_dir
                        self.nb_filename = self.target_dir+'/notes.txt' 
                        
                else:
                    self.nb_filename = target_file
                    self.target_dir = os.path.dirname(target_file)

                if os.path.exists(self.target_dir) is False:
                        os.mkdir(self.target_dir)
                
                self.top = Tkinter.Toplevel()
                self.top.title(self.target_dir)
                self.frame= Tkinter.Frame(master = self.top,width=200, height=300)
                self.frame.pack(expand =True)
                self.menubar = Tkinter.Menu(self.top)
                self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
                self.filemenu.add_command(label="Save", command = self.SaveNotebook)
                self.menubar.add_cascade(label="File", menu=self.filemenu)
                
                self.top.config(menu= self.menubar)
          

                self.scroll = Tkinter.Scrollbar(self.frame)
                self.scroll.pack(side  = Tkinter.RIGHT, fill = Tkinter.BOTH)
                self.t = Tkinter.Text(self.frame,yscrollcommand=self.scroll.set)
                self.t.pack(expand = True,side = Tkinter.LEFT)
                
                self.scroll.config(command=self.t.yview)

                self.LoadNotebook()
                
                return None

        def LoadNotebook(self):

                os.chdir(self.target_dir)
         
                try:
                        if os.path.exists(self.nb_filename):
                                with open(self.nb_filename,"rb") as f:
                                        
                                        
                                        for line in f:
                                          
                                            self.t.insert(Tkinter.END,line)
                                        f.close()
                        else:
                                with open(self.nb_filename,"wb") as f:
                                        f.close()
                                pass
                               
                except IOError:
                        CallError(NOTEBOOK_LOAD_ERROR)
                        return NOTEBOOK_LOAD_ERROR
                return 0

        def SaveNotebook(self):
                os.chdir(self.target_dir)
          
                try:
                        
                        with open(self.nb_filename,"wb") as f:
                                a = self.t.get(0.0,Tkinter.END)
                                for line in a:
                                        
                                        f.write(line)
                                    
                                
                                
                                f.close()
                        
                except IOError:
                        CallError(NOTEBOOK_SAVE_ERROR)
                        return NOTEBOOK_SAVE_ERROR
                
                return 0
def AppendNotebook(file_name,comment):
        from time import gmtime,strftime
        
        target_dir = "C:\\sfg\\data\\" + date.today().strftime("%y%m%d")
        if os.path.exists(target_dir) is False:
                os.mkdir(target_dir)
                
        os.chdir(target_dir)                
         

                
        nb_filename = '.\\'+date.today().strftime("%y%m%d")+'_notes.txt'
                


        
 
        try:
                if os.path.exists(nb_filename):
                        with open(nb_filename,"ab") as f:
                                
                                f.write('\n'+file_name+'\n'+comment)
                                f.close()
                else:
                        with open(nb_filename,"wb") as f:
                        
                                f.write('\n'+strftime("%H:%M:%S ", gmtime())+ file_name+': '+comment+'\n')
                                f.close()
        except IOError:
                CallError(NOTEBOOK_APPEND_ERROR)
                return NOTEBOOK_APPEND_ERROR
        return 0

class SFG_LogWindow:
        
        
        

        def __init__(self):
                               
                 
               
                

               
                self.target_dir = "C:\\sfg\\control_files"
                if os.path.exists(self.target_dir) is False:
                        os.mkdir(self.target_dir)
                
                        
         

                
                self.nb_filename = 'SFGlog.log'
                
                

                self.top = Tkinter.Toplevel()
                self.frame= Tkinter.Frame(master = self.top,width=200, height=300)
                self.frame.pack()
                
                
                self.menubar = Tkinter.Menu(self.top)
                
                self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
                
                self.menubar.add_cascade(label="File", menu=self.filemenu)
                
                self.top.config(menu= self.menubar)
                
               
                
                self.scroll = Tkinter.Scrollbar(self.frame)
                self.scroll.pack(side  = Tkinter.RIGHT, fill = Tkinter.BOTH)
                self.t = Tkinter.Text(self.frame,yscrollcommand=self.scroll.set)
                self.t.pack(side = Tkinter.LEFT)
                
                self.scroll.config(command=self.t.yview)
                self.LoadLog()
                
                return None

        def LoadLog(self):

                os.chdir(self.target_dir)
           
                try:
                        
                        with open(self.nb_filename,"rb") as f:
                                
                                
                                for line in f:
                                        
                                        self.t.insert(Tkinter.END,line)
                                f.close()

                                                                               
                except IOError:
                        CallError(LOG_LOAD_ERROR)
                        return LOG_LOAD_ERROR
                
                return 0
        
def initialize_logging():
        import datetime
        os.chdir("C:\\sfg\\control_files")
        if os.path.exists('SFGlog.log'):
                try:
                        log_date_str = datetime.date.today().strftime("%y/%m/%d")
                        with open('SFGlog.log',"rb") as f:
                                
                                
                                log_first_line = f.readline()
                                f.close()
                        #if log_first_line[0:8] != log_date_str:
                                #os.remove('SFGlog.log')
                                                            
                except IOError:
                        CallError(LOG_LOAD_ERROR)
                        return LOG_LOAD_ERROR
                
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%y/%m/%d %I:%M:%S %p', filename='SFGlog.log',level=logging.INFO)
        return 0



