# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:13:36 2018

@author: xiaofeixiazyh
"""

# 针对水文数据
# 数据的记录方式为每天的8点到第二天8点，因此，将其转换为每日0点到23点

data = []
with open(r'test.txt') as f:
    lines = f.readlines()
    for line in lines:
        data.append(float(line))


trans = []        

length = int(len(data)/24)
times = 0
for i in range(length):
    print(i)
    for j in range(i*24+3, i*24+24):
        trans.append(data[j])
    for j in range(i*24,i*24+3):
        trans.append(data[j])
    
    i+=1


with open(r"result.txt",'w') as w:
    for i in range(len(trans)):
        w.write(str(trans[i]))
        w.write('\n')
        