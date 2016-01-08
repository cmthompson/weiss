# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:30:52 2014

@author: Chris
"""
import os

from K1 import *


#'L-H with O2 Frumkin'
#'Simple Langmuir-Hinshelwood'
#'Jelemensky'



ioff() 
root = Tk()
 
mwin = Window(master = root)
root.protocol("WM_DELETE_WINDOW", quitproc)
sfgmain = ThreadControl(root, mwin, model = 'L-H with ethoxy switch' )
mwin.control_thread = sfgmain
 
root.mainloop()

ion()
    