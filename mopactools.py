# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:43:38 2015

@author: chris
"""

import sys
filename= sys.argv[2]

def out_xyz():
    f  =open(filename, 'rb')
    r = f.readlines()
    f.close()
    for i in r:
        if '----' in i:
            start =  r.index(i)
    
   
    for i in r[start:]:
        if 'CARTESIAN COORDINATES' in i:
            start = start+r[start:].index(i)+2
    a=str()    
    for z in r[start:]:
        print i
        i = z.split(' ')
        while '' in i: 
            i.remove('')
      
        if i[0].isdigit():
            
            i[4]=i[4][:-2]
            a+=i[1]+'    '+i[2]+'    '+i[3]+'    '+i[4]+'   '+'\n'
            numatoms=int(i[0])
        else:
            break
 

    #a  = r[start:end]
    
    f=open(filename+'.xyz','wb')    
    print numatoms
    
    f.writelines([str(numatoms), '\ncomment\n'])
    #for i  in a:
        #f.writelines(i[10:])
    f.write(a)
    f.close()
    return 0
    
    
        
def mop_to_avo():
    r = open(filename+'.xyz','wb')
    f.readline()
    f.readline()
    f.readline()
    number_of_atoms = 0
    for t in f.readlines():
        number_of_atoms+=1
    number_of_atoms-=2
    r.write(str(number_of_atoms)+'\n\n')
    f.seek(0)
    f.readline()
    f.readline()
    f.readline()
    for t in f.readlines():
        t=t.split(' ')
       
        s= t[0]+' '+t[1]+' '+t[3]+' '+t[5]
        
        r.write(s+'\n')
       
    f.close()
    r.close()
    return number_of_atoms


        
    
def xyz_mop():
    print 'convert xyz file to a mop templat file: '+filename
    f = open(filename,'rb')
    a = str()
    a = open(filename+'.mop', 'wb')
    a.write('EF PRECISE\ncomment\ncomment\n')
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
func_arg = {"-xyz_mop": xyz_mop, "-out_xyz": out_xyz}

if __name__ == "__main__":
    func_arg[sys.argv[1]]()
