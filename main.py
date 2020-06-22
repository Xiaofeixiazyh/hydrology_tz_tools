# -*- coding: utf-8 -*-
"""
Created on 2020-6-22 
@author: Yuhang Zhang
"""

# required packages
import numpy as np
import pandas as import pd 
from datetime import datetime, timedelta


def read_raw_data(data_dir):
    """
    function: read the raw data and make data set
    input:
        data_dir : raw data path, eg: '54514.txt'
    output:
        data : data, numpy array, dims = (stationID, intTime, rainfall)
                                  type = (int, int, float)
    """
    raw_data = pd.read_csv(data_dir, sep='\s+', header=None, low_memory=False)
    raw_data.columns = ['stationID', 'intTime', 'rainfall']
    raw_data.loc[raw_data['rainfall']=="//", 'rainfall'] = '0'
    data = raw_data.values
    
    # transfer the data type from str to float
    data[:,2] = data[:,2].astype(float)
    
    # scale factor
    data[:,2] = data[:,2]/10

    return data


def write2file(rainfall_event, out_dir):
    """
    function: wirte one rain event to file and return the summary informations
    input: 
        rainfall_event: one rainfall event
        out_dir: out file path, eg: result
    output:
        attribute about one rainfall event
        filename: the path of the rainfall event saved
        dates_start: when the rain start
        dates_end: when the rain end
        duration: duration of the rain event
        total rainfall: total rainfall of the rain event  
    """
    
    dates = rainfall_event[:,1]
    rainfall = rainfall_event[:,2]
    rainfall[np.where(rainfall==-1)[0]] = 0
    
    t1 = datetime.strptime(str(dates[0]), '%Y%m%d%H%M%S')
    t2 = datetime.strptime(str(dates[-1]), '%Y%m%d%H%M%S')
    duration = 24*60*(t2-t1).days + (t2-t1).seconds//60
    
    dates_start = t1.strftime('%Y-%m-%d %H:%M')
    dates_end = t2.strftime('%Y-%m-%d %H:%M')
    total_rainfall = np.sum(rainfall)
    
    
    
    event_name = str(dates[0])
    filename = out_dir + '/'  + event_name + '.txt'
    
    with open(filename, 'w') as f:
        f.write('Start: %s;    End: %s\n'%(dates_start, dates_end))
        f.write('Total rainfall: %.1f mm;    Duration: %d minutes\n'%(total_rainfall, duration))
        f.write('\n')
        for l in range(rainfall_event.shape[0]):
            date_i = datetime.strptime(str(dates[l]), '%Y%m%d%H%M%S').strftime('%Y-%m-%d    %H:%M')
            f.write('%s    %.1f\n' %(date_i, rainfall[l]))
        f.close()
    
    return filename, dates_start, dates_end, duration, total_rainfall


def clip_rain(data, dry_num, threshold, out_dir):
    """
    function: clip the rain events form time series
    input: 
        data, retun value from the read_raw_data function
        dry_num: type(int),  minimum rainfall interval
        threshold: minimum total rainfall to define one rainfall event
        outdir: file path to save 
    """
    
    length = len(data)
    pr = data[:,2]
    t = 0
    
    starts = []
    ends = []
    durations = []
    total_rainfalls =  []
    filenames = []
    
    
    while t < length:
        sum1 = 0
        if pr[t] == 0:
            t = t + 1
        else:
            t0 = t
            t1 = t0 + dry_num
            sum1 = np.sum(pr[t0:t1])
            if sum1 >= threshold:
                t2 = t0 + 1
                while t2 < length:
                    sum2 = 0
                    if pr[t2] != 0:
                        t2 = t2 + 1
                    else:
                        sum2 = np.sum(pr[t2:t2+dry_num])
                        if sum2 >= threshold:
                            t2 = t2 + 1
                        elif np.sum(pr[t0:t2]) >= threshold:
                            one_event = data[t0:t2, :]
                            filename, dates_start, dates_end, duration, total_rainfall = write2file(one_event, out_dir)
                            filenames.append(filename)
                            starts.append(dates_start)
                            ends.append(dates_end)
                            durations.append(duration)
                            total_rainfalls.append(total_rainfall)
                            t = t2
                            break
                        else:
                            t = t2
                            break
            else:
                t = t + 1
                
    summary = np.array([filenames, starts, ends, durations, total_rainfalls]).T
    df = pd.DataFrame(summary, columns=['filename', 'start','end', 'duration (min)', 'total_rainfall (mm)'])
    df.to_csv(out_dir + '/' + 'summary.csv', index=False)



# main function 
if __name__ == '__main__':

    threshold = 2
    dry_time = 24  # hour
    dry_num = int(dry_time*60/5)

    data_dir = '54514.txt'  # input your data_dir
    out_dir = r'C:\Users\zyh\Desktop\test'      # inpurt your out_dir, need to create first

    data = read_raw_data(data_dir)
    clip_rain(data, dry_num, threshold, out_dir)












