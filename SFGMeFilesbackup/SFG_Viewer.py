from Tkinter import *
import tkFileDialog
import numpy
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
import SFG_Display


root = Tk()
SFG_Display.SFG_DisplayWindow(master = root)

root.mainloop()
       
                        
    



