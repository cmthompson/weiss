# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 10:17:36 2014

@author: chris
"""

import os
import os.path
import re
def rename():
    os.chdir('/home/chris/Orca/Methylbenzenethiol')
    s = loadtxt('MBTvibs.csv',
            unpack = True,
            usecols = (0,1),
            delimiter = ',')
    for f in os.listdir('.'):
        if 'methylbenzenethiol.out.v' in f:
            vibnum = f.split('.')[2].replace('v','')
            try:
                int_vibnum = int(vibnum)
            except:
                continue
            if int_vibnum<11:
                continue
            else:
                freq = s[1][s[0]==int_vibnum]
                
                #print int_vibnum, int(freq[0])
                try:
                    os.rename(f, (f[0:-4]+'_'+str(int(freq[0]))+'.xyz'))
                except: 
                    print 'error',f, int_vibnum, freq
    return 0