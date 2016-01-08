# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:05:49 2015

@author: chris
"""

from numpy import *

            


class File(object):
    num_frames = 1
    accum_time = 1
    def __init__(self, fname):
        self._fid = open(fname, 'rb')
        self._load_size()
        self._load_date_time()
        self.get_info()
       
        
    def _load_size(self):
        
        self._xdim = self.read_at(42, 1, uint16)[0]
        self._ydim = self.read_at(656, 1,  uint16)[0]
        self._numframes = int(self.read_at(1446, 1, int32))
        
    def _load_date_time(self):
        
        try:
            rawdate = self.read_at(20, 9,  int8)
            rawtime = self.read_at(172, 6,  int8)
            
            strdate = ''
            
            for ch in rawdate:
                strdate += chr(ch)
            
            for ch in rawtime:
                strdate += chr(ch)
            
            self._date_time = time.strftime("%b %d %Y %H:%M:%S",time.strptime(strdate,"%d%b%Y%H%M%S"))
        except:
            self._date_time = 'no date info'
        
    def get_size(self):
        return (self._xdim, self._ydim)
   
        

    def read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return  fromfile(self._fid, ntype, size)

    def load_img(self):
        img = self.read_at(4100,self._xdim * self._ydim* self._numframes,  float32)
        img = img.reshape((self._numframes,self._ydim, self._xdim))
        
        return img
   
    def get_info(self):
        
       # print 'datatype', self.read_at(108, 1, uint16)
        infostring = str()
       
        infostring+=  str(self._date_time)+'\n'
        infostring+=  'frames:'+ str(int(self.read_at(1446, 1, int32)))+'\n'
        
         
       # infostring+=  'readout time'+ str(self.read_at(672,1, int32))+'\n'
        infostring+=  'accumulations:'+ str(self.read_at(668,1, int32))+'\n'+ str(int(self.read_at(10,1, float32)))+ 'seconds'+'\n'
        infostring+=  'excitation wavelength:'+ str(self.read_at(3311,1, float64))+ 'nm'+'\n'
        infostring+= 'gain setting:'+ str(int(self.read_at(198,1, uint16)))+'\n'
        infostring+= 'detector temp' + str(self.read_at(36, 1, float32))+ 'degree C \n'
        
        self.info = infostring 
        return self.info
    def get_accum_time(self):
        
        return float(self.read_at(10,1, float32))
        
        
    def close(self):
        self._fid.close()