# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 01:32:20 2021

@author: SAYED
"""

import random

f = open("Map_Genarator.txt","w+")

for i in range(500):
    
    for j in range(500):
        if j == 499:
            f.write("%d\n" % random.randint(0, 5))
        else:
            f.write("%d " % random.randint(0, 5))


f.close() 
