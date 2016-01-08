# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 19:20:14 2015

@author: chris
"""

from Tkinter import *

root = Tk()


def callback(event):
    frame.focus_set()
    print "clicked at", event.x, event.y
def unclick(event):
    print 'unclicked'

frame = Frame(root, width=100, height=100)

frame.bind("<Button-1>", callback)
frame.bind("<ButtonRelease-1>", unclick)
frame.pack()

root.mainloop()