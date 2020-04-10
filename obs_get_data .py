# coding=utf-8
'''
修改时间即可，start_time、end_time 按照格式修改
此脚本下载数据后会进行预处理
因此在原来的步骤中的预处理过程可以跳过
'''

# Import modules and functions
import numpy as np
import obspy.core
import os.path
import pickle
from obspy import UTCDateTime
from obspy.core import read, Stream, Trace
from obspy.clients.fdsn import Client


# Main function
def process():
    station = 'AXCC1'
    network = 'OO'
    # Define path to see if it exists
    obspath = station + "/"
    if not os.path.isdir(obspath):
        print 'Path to ' + obspath + ' doesn`t exist - creating it'
        os.makedirs(obspath)

    # Establish client
    client = Client()

    # Specify date for transfer function calculation
    start_time = UTCDateTime('2018-01-02')
    end_time = UTCDateTime('2018-05-01')
    

    # Define start and end times for noise requests
    tstart = start_time
    tend = start_time + 3600. * 24.

    
    while tstart < end_time:

        # Get waveforms from client
        try:
            sth = client.get_waveforms(network, station, '*', \
                                       'BHZ', tstart, tend, attach_response=True)
        except Exception as e:
            print "Failed on" + str(jd) + "due to" + str(e)
            tstart = tend
            tend = tstart + 3600.* 24.
            continue
        try:
            stp = client.get_waveforms(network, station, '*', \
                                       'HDH', tstart, tend, attach_response=True)
        except Exception as e:
            print "Failed on" + str(jd) + "due to" + str(e)
            tstart = tend
            tend = tstart + 3600. * 24.
            continue

        sth.remove_response(output='DISP')
        stp.remove_response()

        # Detrend, filter
        sth.detrend('demean')
        sth.detrend('linear')
        sth.filter('lowpass', freq=0.5 * 4.0, corners=2, zerophase=True)
        sth.decimate(10)

        stp.detrend('demean')
        stp.detrend('linear')
        stp.filter('lowpass', freq=0.5 * 4.0, corners=2, zerophase=True)
        stp.decimate(10)
        stp.decimate(5)

        # Extract traces
        trZ = sth.select(component='Z')[0]
        trP = stp.select(channel='HDH')[0]

        # Define file names
        jd = str(tstart.julday).zfill(3)
        yr = str(start_time.year).zfill(4)
        fileZ = obspath + network + '.' + station + '..' + 'BHZ.M.' + yr + '.' + jd + '.SAC'
        fileP = obspath + network + '.' + station + '..' + 'HDH.M.' + yr + '.' + jd + '.SAC'
        # Save traces
        trZ.write(fileZ, format='sac')
        trP.write(fileP, format='sac')

        print jd

        tstart = tend
        tend = tstart + 3600. * 24.




###############################
# Choose one station to process
process()

###################
