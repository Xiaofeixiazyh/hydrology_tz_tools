# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:34:06 2018

@author: xiaofeixiazyh
"""

# 计算任何时段的降雨量
# 输入文件的降雨量时段为t0
# 输出文件的降雨量时段为t 
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math


#def eachFile(filepath):
#    '''
#    读取路径下所有的文件并打印出文件名
#    '''
#    pathDir = os.listdir(filepath)
#    for allDir in pathDir:
#        if len(allDir) == 18 and allDir[15:18] == 'txt':
#            child = filepath + "\\" + allDir
#            print(child)
#eachFile(r'D:\13tz_\tz_rainfall_5min')        
        
def read_data(filename):
    data = []  # 存储新的数据
    with open(filename,'r') as f:
        while True:
            lines = f.readline() #整行读取数据
            if not lines:
                break
                pass
            zd, time, value = [i for i in lines.split()] #将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            # zd 代表站点编号； time 代表时间； value 代表降雨量  #注意：刚读进来的数据是以字符串的形式存储
#            print(type(value))
            data.append(float(value)/10)    #将单位换算为1mm 的标准单位
#            data = np.array(data)
    return data 

def conv2t(data,t0, t):
    '''
    从时间间隔为t0分钟转为时间间隔为t分钟的数据
    data : 输入数据
    t0： 输入数据的时间间隔
    t ： 输出数据的时间间隔
    '''
    dt = int(t/t0)   # dt 结果为float类型  !!!!  要转换为int类型
    length = int(len(data)/dt) # 控制循环的次数 

    data_trans = []
    j = 0
    for i in range(length):
        data_trans.append(sum(data[j:j+dt]))
        j += dt
    return data_trans


def print_time(filename,length, dt):
    '''
    格式化输出时间格式
    输入为： 文件名，时间序列长度，时间间隔
	输入的文件中文件格式为 年 月 日 时 分 
    输出为：格式化的时间序列
    '''
    year = [0] *length
    month = [0] *length
    day = [0] *length
    hour = [0] *length
    minute = [0] *length
    with open(filename, 'r') as f:
        year[0],month[0],day[0],hour[0],minute[0] = f.readline().strip().split()
        year[0] = int(year[0])
        month[0] = int(month[0])
        day[0] = int(day[0])
        hour[0] = int(hour[0])
        minute[0] = int(minute[0])  #读入起始日期
# =============================================================================
# 循环准备输出时间格式   
# =============================================================================
    for i in range(1, length):
        leap_year = 0 
        # 一般情况下分钟数加dt， 其他不变
        if dt <= 60:   # 时间间隔小于1小时  要按分钟加
            minute[i] = minute[i-1] + dt
            hour[i] = hour[i-1]
            day[i] = day[i-1]
            month[i] = month[i-1]
            year[i] = year[i-1]
        elif dt<= 1440: # 时间间隔大于1小时 小于24小时即小于1天时，按照时进行叠加
            dt_trans1 = int(dt/60)
            hour[i] = hour[i-1] + dt_trans1
            day[i] = day[i-1]
            month[i] = month[i-1]
            year[i] = year[i-1]
        else:  # 时间间隔大于1天，按天进行叠加
            dt_trans2 = int(dt/60/24)
            day[i] = day[i-1] + dt_trans2
            month[i] = month[i-1]
            year[i] = year[i-1]
            
        # 判断是否为闰年，用来确定2月的天数
        if((year[i]%4==0) and (year[i]%100!=0) or (year[i]%400==0)):
            leap_year = 1
        # 超过60分钟为下一个小时
        if minute[i]>=60:
            minute[i] = 0
            hour[i] += 1
        # 超过24小时记为第二天 
        if(hour[i] >= 24):
            hour[i] -= 24
            day[i] += 1
        # 判断月,超过月最大天数的记为下一个月，大于1年的记为下一年    
        if month[i] in (1,3,5,7,8,10):
            if day[i]>=32:
                day[i] -= 31 
                month[i] += 1
        elif month[i] in(4,6,9,11):
            if day[i]>=31:
                day[i] -= 30 
                month[i] += 1
        elif month[i] ==2:
            if(leap_year==1 and day[i]>=30):
                day[i] = day[i]- 29
                month[i] += 1
            elif(leap_year==0 and day[i]>=29):
                day[i] = day[i] -28
                month[i] += 1
        elif month[i] ==12:   # 月份为12时应该特殊对待，年份应该加1
            day[i] -= 32
            month[i] =1
            year[i] +=1
            
        elif month[i] >= 13 :
            day[i] = 1
            month[i] = 1
            year [i] += 1
 
    return year,month,day,hour,minute
    


#filename = r'C:\Users\xiaofeixiazyh\Desktop\test.txt'
#year,month,day,hour,minute = print_time(filename,None)
#print(year,month,hour,day,hour,minute)
    
    

def write_data(data,filename):
    '''
    写入文件
    '''
    with open(filename, 'w') as f:
        for i in data:
            f.write(str(i))
            f.write('\n')
# =============================================================================
# 输出数据部分
# =============================================================================
delta_t = 60 * 24*3
filename = r'C:\Users\xiaofeixiazyh\Desktop\2013-2017.txt'
prec = read_data(filename)
data_trans = conv2t(prec, 5, delta_t)  
filename2 = r'C:\Users\xiaofeixiazyh\Desktop\2013-2017_2.txt'
write_data(data_trans, filename2)  


# =============================================================================
#  输出时间格式
# =============================================================================
#filename3 = r'C:\Users\xiaofeixiazyh\Desktop\test.txt'
#length = len(data_trans)
#year,month,day,hour,minute = print_time(filename,length,10)
#print(year[0],month[0],day[0],hour[0],minute[0])
#year,month,day,hour,minute = print_time(filename3,length,delta_t)
#s = []
#with open(r'C:\Users\xiaofeixiazyh\Desktop\time.txt','w') as w:
#    for i in range(length):
#        s = '\t'.join((str(year[i]),str(month[i]),str(day[i]),str(hour[i]),str(minute[i])))
#        w.write(s)
#        w.write('\n')




    