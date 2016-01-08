# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:38:20 2014

@author: Chris

Creating a figure for the Robey Proposal
"""
x = linspace(-100,200,1000)
cla()

#plot(3*exp(-(x-0)**2/4), 'b')
#fill_between(x,1*exp(-(x-40)**2/(40*0.1)),color = 'r' )  #20 ps
#fill_between(x,3*exp(-(x-0)**2/(40*10)),color = 'b' )

fill_between(x,100/((50-x)**2+100),color = 'b' )

#fill_between(x,3*exp(-(x-60)**2/(40*0.1)),color = 'g' ) # 40 fs
ylim(0,4)
yticks([0])
xticks([0])