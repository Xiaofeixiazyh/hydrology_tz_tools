# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:11:46 2018

@author: xiaofeixiazyh
"""

# 

dict = {}
with open(r'C:\Users\xiaofeixiazyh\Desktop\合并重复关键词.txt' ,'r') as f:
    for line in f:
        line = line.strip()
        a = line.split('\t')
#        print(a)
        dict.setdefault(a[0],[])
#        print(dict)
        length = len(a)
        for i in range(1, length):
            dict[a[0]].append(a[i])
#    print(dict)
with open(r'C:\Users\xiaofeixiazyh\Desktop\合并重复关键词_hou.txt' ,'w') as w:
    for k,v in dict.items():
        w.write(str(k) + ' ')
        length = len(v)
        for i in range(length):
            w.write(v[i] + ' ')
        w.write('\n')
        
        
        