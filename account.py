# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 15:30:38 2016

@author: chris
"""

from numpy import random
class Account(object):
    
    def __init__(self,initialvalue,growthrate,
                 salary=0,periodicwithdrawls = list(),growthnoise = 0):
        self.initialvalue = initialvalue
        self.salary=salary
        self.growthrate = pandas.Series(
                            (ones((100,))+random.randn(100)*growthnoise)*growthrate,
                             arange(0,100))
        print 'average growth rate', mean(self.growthrate)
    
        
        
        self.wd = pandas.DataFrame(zeros((100,)), arange(100))
        for i in periodicwithdrawls:
            print i
            self.wd = pandas.concat([self.wd,pandas.DataFrame(array(i[1]),array(i[0]))])
            
     
        
        self.account = pandas.Series(ones((100,))*self.initialvalue, arange(0,100))
        self.calculate()
        self.plot()
        print 'final amount at 100 y.o.', self.account.iget(70)
        return None
    
    def recalc_growthrate(self):
        self.growthrate = pandas.Series(
                            (ones((100,))+random.randn(100)*growthnoise)*growthrate,
                             arange(0,100))
        return 0
    
    
    def calculate(self):
        for i in self.account.index[1:]:
            
            self.account[i]=self.account[i-1]*(1+self.growthrate[i])
            self.account[i]+=self.salary
            
            for wd in self.wd:
                print type(wd)
                if True:#wd[i]:
                    
                    self.account[i]-=wd[i]
            
        return None
        
    def plot(self,*args,**kwargs):
        return self.account.plot(*args, **kwargs)