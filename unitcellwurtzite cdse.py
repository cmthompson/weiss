# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 07:39:02 2015

@author: chris
"""
from itertools import combinations_with_replacement,product

#Cd       0.6670000000      0.3330000000      0.0000000000                 
#Cd       0.6670000000      0.3330000000      1.0000000000                 
#Cd       0.3330000000      0.6670000000      0.5000000000                 
#Se       0.3330000000      0.6670000000      0.8750000000                 
#Se       0.6670000000      0.3330000000      0.3750000000     
a = 4.3*array([1,0,0])
b = 4.3*array([cos(radians(60)), sin(radians(120)), 0])
c = 7.02*array([0,0,1])


Cd1 = array([0.667,0.333, 0])
Cd2 = array([0.333,0.667,0.5])
Se1 = array([ 0.3330000000  ,0.6670000000 ,0.8750000000])               
Se2 = array([0.6670000000,0.3330000000, 0.3750000000])
def cart_coords(cell=(0,0,0)):
    
    cellorigin = a*cell[0] + b*cell[1]+c*cell[2]
    print 'cell', cell
    cd1 = a*Cd1[0] + b*Cd1[1]+c*Cd1[2] + cellorigin
    cd2 = a*Cd2[0] + b*Cd2[1]+c*Cd2[2] + cellorigin
    se1 = a*Se1[0] + b*Se1[1]+c*Se1[2] + cellorigin
    se2 = a*Se2[0] + b*Se2[1]+c*Se2[2] + cellorigin
    
    ret =  list([list(cd1), list(cd2), list(se1), list(se2)])
  
    return ret

def write_supercell():  ### If you want 100 slab, make the a lenght smallest
    f = open('/home/chris/Desktop/supercell.xyz', 'w')
    r =product(range(3),range(10), range(10))
    x = list()
    
    for item in r:
       print item
       
       x.append(cart_coords(cell=item))
   
   
    f.write(str(len(x)*4)+'\n\n')
    for unit in x:
        f.write('Cd '+str(unit[0][0])+' '+str(unit[0][1])+' '+str(unit[0][2])+'\n')
        f.write('Cd '+str(unit[1][0])+' '+str(unit[1][1])+' '+str(unit[1][2])+'\n')
        f.write('Se '+str(unit[2][0])+' '+str(unit[2][1])+' '+str(unit[2][2])+'\n')
        f.write('Se '+str(unit[3][0])+' '+str(unit[3][1])+ ' '+str(unit[3][2])+'\n')
    f.close()
    
    return 0

def write_supercell_frag(size = (2,3,3),type='mopac'):  ### If you want 100 slab, make the a lenght smallest
    
    r =product(range(size[0]),range(size[1]), range(size[2]))
    x = list()
    
    if type=='orca':   
        f = open('/home/chris/Desktop/slabopt/supercellfrag.xyz', 'wb')
        f.write(str(r.__sizeof__())+'\n\n')
        for item in r:
           
           unit = cart_coords(cell=item)
           if item[0]==size[0]-1:  ## surface layer
               group = '2'
           else:
               group = '1'
           
           f.write('Cd('+group+') '+str(unit[0][0])+' '+str(unit[0][1])+' '+str(unit[0][2])+'\n')
           f.write('Cd('+group+') '+str(unit[1][0])+' '+str(unit[1][1])+' '+str(unit[1][2])+'\n')
           f.write('Se('+group+') '+str(unit[2][0])+' '+str(unit[2][1])+' '+str(unit[2][2])+'\n')
           f.write('Se('+group+') '+str(unit[3][0])+' '+str(unit[3][1])+ ' '+str(unit[3][2])+'\n')
    elif type=='mopac':
        f = open('/home/chris/Desktop/slabopt/supercellfrag.mop', 'wb')
        f.write('PM3\n\n\n')
        for item in r:
     
            unit = cart_coords(cell=item)
            if item[0]==size[0]-1:  ## surface layer
                group = ' 1 '  #need the spaces on either side
            else:
                group = ' 1 '  ##need the spaces
           
            f.write('Cd '+str(unit[0][0])+group+str(unit[0][1])+group+str(unit[0][2])+group+'\n')
            f.write('Cd '+str(unit[1][0])+group+str(unit[1][1])+group+str(unit[1][2])+group+'\n')
            f.write('Se '+str(unit[2][0])+group+str(unit[2][1])+group+str(unit[2][2])+group+'\n')
            f.write('Se '+str(unit[3][0])+group+str(unit[3][1])+group+str(unit[3][2])+group+'\n')   

    f.close()
    
    return 0

def mop_to_avo(filename):
    f=open(filename, 'rb')
    r = open(filename+'.xyz','wb')
    f.readline()
    f.readline()
    f.readline()
    number_of_atoms = 0
    for t in f.readlines():
        number_of_atoms+=1
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
    
 
    