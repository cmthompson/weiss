# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 21:41:19 2014

@author: Chris
"""
#from urllib2 import urlopen
#import re
#
#
#
#name = "https://www.facebook.com/"
#response = urlopen(name)
#html= str(response.read())
#print html[0:1000]

from twill.commands import *
from twill.namespaces import get_twill_glocals
 
go('https://nrc58.nas.edu/nrcwebrap/rap/login/login.asp')
local_dict = get_twill_glocals()
print local_dict

fv("1", "txtUserEmail", "chris.thompson@berkeley.edu")
fv("1", "pwdPassword", "forwardho")
showforms()
submit('0')
