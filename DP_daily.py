import os
import fnmatch
from obspy import UTCDateTime
from obspy.core import read, Stream
import pickle
import rayleigh_utils as utils
import numpy as np

def process(db, sta_key):
    sta = db[sta_key]  # sta is the meta_data

    UTC_sta = UTCDateTime("2015-01-01T00:00:00")
    UTC_end = UTCDateTime("2017-12-31T00:00:00")


    cur_time = UTC_sta

    ws = 8000
    dn = 0.25

    output = open(sta.station + "/days", "w+")
    list_ratios = []
    list_days = []
    while cur_time < UTC_end:
        julday = cur_time.julday
        year = cur_time.year

        trZ, trP = get_data(str(sta_key) + '/rayleigh/', year, julday)

        if len(trZ) < 1 or len(trP) < 1:
            cur_time += 3600 * 24
            continue

        ratio = utils.rayleigh_DP_ratio(trZ[0], trP[0], ws)

        output.write(str(year)+"."+str(julday) + '\n')
        list_ratios.append(ratio)

        print "daily working on" + str(julday)

        cur_time += 3600 * 24

    np.savetxt(sta.station+"/ratio",list_ratios)

def get_data(filedir, year, julday):
    """
    Function to read all available receiver functions that meet SNR threshold
    :param filedir: String()
    :param julday: Integer
    :param year: Integer
    :return: Stream() objects
    """
    # Define empty streams
    trNZ = Stream()
    trNP = Stream()
    trZ = Stream()
    trP = Stream()

    filename = str(year) + "." + str(julday)

    # Loop through directory and load files
    for file in os.listdir(filedir):
        if fnmatch.fnmatch(file, filename + '.BHZ'):
            tr = read(filedir + file)
            trZ.append(tr[0])
        elif fnmatch.fnmatch(file, filename + '.P'):
            tr = read(filedir + file)
            trP.append(tr[0])

    return trZ, trP


# Loads station db and builds attribute dict of station stats
def load_db(fname):
    db = pickle.load(open(fname, 'rb'))
    for k, v in db.items():  # k is station's name v is attributes of the station
        db[k] = meta_data(v)
    return db


# Attribute dict class
class meta_data(dict):
    def __init__(self, stats):
        self.__dict__ = self
        self.network = stats[0]
        self.station = stats[1]
        self.stla = stats[2]
        self.stlo = stats[3]
        self.stel = stats[4]
        self.azim = stats[5]
        self.cha = stats[6]
        self.dstart = stats[7]
        self.dend = stats[8]


def run(key='AXCC1'):
    dbfile = 'stations.pkl'
    stationdb = load_db(dbfile)
    sta_key = key
    print "working on " + sta_key
    return process(stationdb, sta_key)


if __name__ == "__main__":
    keys = ['AXCC1','AXEC2','AXBA1']
    run()
