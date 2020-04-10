import pickle
from obspy.core import UTCDateTime

# Dictionary with all station information
# Keys are station names, and each item contains 
# a list of network names, station names, station lat,
# station lon, deployment depth, azimuth of channel 1, 
# and channel type (either BH or HH)
stations = \
        {'AXCC1': ['OO', 'AXCC1', 45.954681, -130.008896, 1528, 0, 'BH', UTCDateTime('2015-03-01'), UTCDateTime('2015-06-01')],
         'AXBA1':['OO', 'AXBA1', 45.820180, -129.736700, 2607.2, 0, 'BH', UTCDateTime('2015-03-01'), UTCDateTime('2015-06-01')],
        'AXEC2':['OO', 'AXEC2', 45.939670, -129.973800, 1519.0, 0, 'BH', UTCDateTime('2015-03-01'), UTCDateTime('2015-06-01')]
         }

pickle.dump(stations, open('stations.pkl', 'wb'))

