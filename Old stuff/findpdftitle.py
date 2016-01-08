# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 11:50:12 2014

@author: chris
"""

# pyPdf available at http://pybrary.net/pyPdf/
from pyPdf import PdfFileWriter, PdfFileReader
import os

def run():
    os.chdir('/home/chris/Documents/Literature')
    for fileName in os.listdir('.'):
        
        try:
            input1 = PdfFileReader(file(fileName, "rb"))
       
            # print the title of document1.pdf
            print '##1', fileName, '##2', input1.getDocumentInfo().title
        except:
            pass
            
    return 0