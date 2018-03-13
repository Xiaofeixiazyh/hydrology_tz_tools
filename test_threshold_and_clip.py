# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 16:34:29 2018

@author: xiaofeixiazyh
"""

# 按指定要求筛选并且将数据切片，然后分别统计量

def read_data(filename):  #读取文件，文件格式为三列
    '''
    读取数据，数据的格式为三列，第一列序号，第二列时间，第三列为数值。
    输入为文件路径，输出为要处理的数据的一个 列表
    '''
    data = []  # 存储新的数据
    with open(filename,'r') as f:
        while True:
            lines = f.readline() #整行读取数据
            if not lines:
                break
                pass
            idx, time, value = [i for i in lines.split()] #将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            # idx 代表序号； time 代表时间； value 代表排污量速率  #注意：刚读进来的数据是以字符串的形式存储
#            print(type(value))
            data.append(float(value))  # 值为浮点型！！！ 从文件中读取的数据为str
#            data = np.array(data)
    return data # list

def test_times(data,threshold):
    '''
    统计大于阈值的个数
    输入为一个列表，输出为大于阈值统计的次数
    '''
    times = 0
    length = len(data)
    i = 0
    while i < length:
        if data[i] > threshold :   
            j = i+1
            for k in range(j,length):
                if data[k] <= threshold:   # 注意可能存在死循环
                    break
            i = k
            times += 1
        else:
            i += 1
    return times

	
def cilp_times(data, threshold,times):  # 将筛选出的数据进行切片
    '''
	输入： 列表数据；阈值； 切片出的个数
    '''
    lis = [[] for i in range(times)]
    lis_idx = 0
    length = len(data)
    i = 0
    while i < length:
        if data[i] > threshold :
            lis[lis_idx].append(data[i]) 
            j = i+1
            for k in range(j,length):
                if data[k] > threshold:
                    lis[lis_idx].append(data[k]) 
                if data[k] <= threshold:
                    break
            i = k
            lis_idx += 1
        else:
            i += 1
    return lis

	
	

import numpy as np 
def sum_everytime(lis):  # 对切片出的数据进行分析，计算，速率转化为量
    sum_ = []
    
    for i in range(len(lis)):
        data = np.array(lis[i])
        sum_.append(np.sum(data-threshold)*10*60)   #时间间隔为十分钟，原单位为m3/s，因此数据*10*60
    return sum_


        
    
def write_data(data,filename): #将切片的数据写入新的文件中
    '''
    写入文件
    '''
    with open(filename, 'w') as f:
        for i in range(len(data)):
            for j in data[i]:
                f.write(str(j))
                f.write('\n')
            f.write('--------------------\n')


            
#lis = [[1,2,3],[2,3,4],[1,1,1]]
#sum_ = sum_(lis)
#print(sum_)

#filename1 = r'C:\Users\xiaofeixiazyh\Desktop\yl.txt'
#filename2 = r'C:\Users\xiaofeixiazyh\Desktop\yl_2.txt'

filename1 = r'C:\Users\xiaofeixiazyh\Desktop\plan2\plan2.2013\weir_wuyi.txt'
filename2 = r'C:\Users\xiaofeixiazyh\Desktop\plan2\plan2.2013\weir_wuyi_chulihou.txt'

threshold = 0.00
data = read_data(filename1)
times = test_times(data, threshold)
print("所求的次数为：{}".format(times))
lis = cilp_times(data, threshold, times)
sum_ = sum_everytime(lis)

with open(r"result.txt",'w') as w:  # 将切片数据分析后的结果写入文件
    for i in range(len(sum_)):
        w.write(str(sum_[i]))
        w.write('\n')
        
        
        
        
#sum_ = sum_(lis)
#print("total value is {}".format(sum_))
#write_data(lis,filename2)  