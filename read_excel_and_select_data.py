# -*- coding: utf-8 -*-
"""
Created on Fri May 25 10:29:29 2018

@author: xiaofeixiazyh
"""
'''
this code for select station and station_id
'''

import pandas as pd
#import numpy as np

#--------------------手动输入部分------------------------#
int_filename = r'C:\Users\xiaofeixiazyh\Desktop\孙晓琳-2017年整理-暴雨内涝资料整理20180523.xlsx'  # 输入文件的路径		eg：filename = r'C:\Users\xiaofeixiazyh\Desktop\孙晓琳-2017年整理-暴雨内涝资料整理20180523.xlsx'
out_filename = r'C:\Users\xiaofeixiazyh\Desktop\result.xlsx'
sheet_name = '6.21-6.24'  # 输入要操作的sheet表的名称 eg： sheetname = '6.18'
skiprows =  2       # 输入要跳过的行数 eg： skiprows = 2
usecols = 'G:K '      # 输入要读取的列  eg： ‘G:K’
station_id = 'FXPP0882'
station_name= '来广营'

#--------------------程序处理部分-------------------------#
df = pd.read_excel(int_filename, sheet_name=sheet_name, skiprows=skiprows, usecols=usecols)
data = df[df['编码']== station_id]  # 在这里修改所需站点编号 eg：data = df[df['编码']== 'FXPP0878']
starttime=data.iloc[0,3]
endtime = data.iloc[-1,3]
time_range = pd.date_range(starttime, endtime, freq='5Min')

station = []
code = []
prec = [0]*len(time_range)
for i in range(len(time_range)):
	station.append(station_name)  # 输入站点中文名称 eg：station_name.append('奥体匹克公园')
	code.append(station_id)  		  # 输入站点编码 eg：code.append('FXPP0878')

index = range(1,len(time_range)+1)

d = {
		'名称':station,
        '时间':time_range, 
        '雨量':prec,
        '编码':code,
        '序号':index
}

columns = ['序号', '名称', '编码', '时间', '雨量']
Newdata = pd.DataFrame(d,columns=columns)

data_merge = Newdata.append(data)
data_selected = data_merge.drop_duplicates(['时间'], keep='last', inplace=False)

#---------------------------文件保存--------------------#
data_selected.to_excel(out_filename)
# 在此输入保存文件的路径 eg：data_selected.to_excel(r'C:\Users\xiaofeixiazyh\Desktop\result.xlsx')
