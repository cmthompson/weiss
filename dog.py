# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 18:06:45 2015

@author: chris
"""

class Dog(object):
    
    tricks = []
    tricks2 = 1
    
    def __init__(self):
        return None
    
    def addtrick(self,t):
        self.tricks.append(t)
        self.tricks2 = t
        return None
        
        
    
    