# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:37:31 2015

@author: chris
"""

def z():#xyz_to_mop(filename):
    filename = '/home/chris/Orca/slabopt/scphos_opt2.out.xyz'
    f = open(filename,'rb')
    a = str()
    a = open(filename+'.mop', 'wb')
    a.write('command\ncomment\ncomment\n')
    for i in f.readlines()[2:]:
        
        i = i.split(' ')
        while '' in i: 
            i.remove('')
        i[-1] = i[-1][:-1]
        if i[0] == 'S' or i[0]=='Cd':
            obj ='  0  '
        else:
            obj = '  1  '
        
        newline = i[0]+'     '+i[1]+obj+i[2]+obj+i[3]+obj+'\n'
        a.write(newline)
        
        
       # 
        print newline
    return 0
