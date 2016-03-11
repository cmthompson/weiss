# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 08:50:50 2014

@author: chris
"""

import sys
sys.path.append('/home/chris/PyScripts')



import ramanTools.RamanTools, ramanTools.RamanSpectrum
from Tkinter import *
import os
ioff()
os.chdir('/home/chris/Documents/DataWeiss')

root = Tk()
root.withdraw()
ramanTools.RamanTools.DisplayWindow(root,ax=None)
root.mainloop()

