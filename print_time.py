# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:17:18 2018

@author: xiaofeixiazyh
"""

# 输出时间 规定时间的时间格式




def print_time(filename,length, dt):
    '''
    格式化输出时间格式
    输入为： 文件名，时间序列长度，时间间隔
    输出为：格式化的时间序列
    '''
    year = [0] *length
    month = [0] *length
    day = [0] *length
    hour = [0] *length
    
# =============================================================================
#     开始时间的读取
# =============================================================================
    with open(filename, 'r') as f:
        year[0],month[0],day[0],hour[0] = f.readline().strip().split()
        year[0] = int(year[0])
        month[0] = int(month[0])
        day[0] = int(day[0])
        hour[0] = int(hour[0])

# =============================================================================
# 循环准备输出时间格式   
# =============================================================================
    for i in range(1, length):
        leap_year = 0
        hour[i] = hour[i-1] +  dt
        day[i] = day[i-1]
        month[i] = month[i-1]
        year[i] = year[i-1]
        
        # 判断是否为闰年，用来确定2月的天数
        if((year[i]%4==0) and (year[i]%100!=0) or (year[i]%400==0)):
            leap_year = 1
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
        elif month[i] == 12:
            if day[i]>=32:
                day[i] -=31
                month[i] = 1
                year[i] += 1
        elif month[i] >= 13 :
            day[i] = 1
            month[i] = 1
            year [i] += 1
 
    return year,month,day,hour

filename = r'time_start.txt'
length = 333120
dt =1
year,month,day,hour = print_time(filename, length,dt)
s= []

with open(r'time_out.txt','w') as w:
    for i in range(length):
        s = ' '.join((str(year[i]),str(month[i]),str(day[i]),str(hour[i])))
        w.write(s)
        w.write('\n')