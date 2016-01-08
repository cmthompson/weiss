# -*- coding: utf-8 -*-
"""
Created on Thu Jan 09 12:46:00 2014

@author: Chris
"""

import csv

def step1():
    
    ret_val = list()
    with open("C:\\Users\\Chris\\Google Drive\\SFGLog.log","rb") as f:
                    
        CSV_READER = csv.reader(f,dialect = 'excel')

        i = 0
        for row in CSV_READER:
                i+=1
                if len(row)<1:
                    pass
                elif "2800" in row[0] and "14/01/03" in row[0]:
                    
                    ret_val.append(row[0])
                else:
                    pass
        print i 
        f.close()
        
    return ret_val


def step2(o):
    ret_val = list()
    
    for i in range(len(o)-1):
        time_delay = 0
        [h1,m1,s1] = o[i].split(' ')[1].split(':')
        [h2,m2,s2] = o[i+1].split(' ')[1].split(':')
        

        m1 = int(m1)
        s1 = int(s1)
        m2 = int(m2)
        s2 = int(s2)
        if m2 >= m1:
            time_delay += (m2-m1)*60 
        else:
            time_delay += (m2-m1+60)*60
        if s2 >= s1:
            time_delay += (s2-s1)
        else:
            time_delay += (m2-m1+60)
        if time_delay!=0:
            ret_val.append((time_delay,(str(h1)+":"+str(m1)+":"+str(s1))))
    
    return ret_val
    
def step1b():
    
    ret_val = list()
    with open("C:\\Users\\Chris\\Google Drive\\SFGLog.log","rb") as f:
                    
        CSV_READER = csv.reader(f,dialect = 'excel')

        i = 0
        for row in CSV_READER:
                i+=1
                if len(row)<1:
                    pass
                elif "Saved motor positions" in row[0] and "14/01/03" in row[0]:
                    
                    ret_val.append(row[0])
                else:
                    pass
        print i 
        f.close()
        
    return ret_val    
                                