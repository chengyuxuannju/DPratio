import pickle
from obspy.core import Stream, AttribDict
from obspy import UTCDateTime, read


def process(db, key):
    sta = db[key]

    sta_time = UTCDateTime("2016-01-01T00:00:00")
    end_time = UTCDateTime("2016-12-31T00:00:00")

    year = sta_time.year

    d_path = sta.station + "/raw/" + sta.network + "." + str(key) + ".." + "BHZ.M." + str(year) + "."
    p_path = sta.station + "/raw/" + sta.network + "." + str(key) + ".." + "HDH.M." + str(year) + "."

    ts = sta_time
    te = ts + 3600 * 24
    path = sta.station + "/rayleigh/"

    while ts < end_time:

        julday = ts.julday

        if julday < 100:
            jul_str = "0" + str(julday)
        else:
            jul_str = str(julday)

        try:
            sac_d = read(pathname_or_url=d_path + jul_str + "*red", format="SAC")
            sac_p = read(pathname_or_url=p_path + jul_str + "*red", format="SAC")
        except Exception:
            ts += 3600 * 24
            te = ts + 3600 * 24
            print "Failed" + jul_str
            continue

        filename_prefix = path + str(year) + "." + str(julday)
        print "working on " + filename_prefix

        disp = sac_d.slice(ts, te)
        pres = sac_p.slice(ts, te)
        print 'Done slice'

        if len(disp.traces) == 0 or len(pres.traces) == 0:
            ts += 3600 * 24
            te = ts + 3600 * 24
            continue

        # Get the longest segment, p and d are the same length
        try:
            disp, pres = find_longest_equal(disp, pres)
            print "Done fl"
        except AttributeError:
            print "Caught"
            ts += 3600 * 24
            te = ts + 3600 * 24
            continue

        fileZ = filename_prefix + ".BHZ"
        fileP = filename_prefix + ".P"

        trZ = disp.traces[0]
        trP = pres.traces[0]

        trZ.write(fileZ, format='sac')
        trP.write(fileP, format='sac')

        ts += 3600 * 24
        te = ts + 3600 * 24


def find_longest_equal(d, p):
    """
    Find the longest time and return the new Stream
    :param d,p: a Stream object has several time slice
    :return d_slice,p_slice: Stream object (For remove response)
    :exception pressure date not coherent with displacement
                data length too short
    """
    d = d.traces
    index = 0
    tempT = d[0]

    for i in range(len(d)):
        if len(d[i]) > len(tempT):
            index = i
            tempT = d[i]

    d_slice = d[index]

    #  the admittance of each day is based on 9 to 30 2000 s long time series
    # 9*2000 = 18000
    if d_slice.meta.endtime - d_slice.meta.starttime < 18000:
        print d_slice.meta.endtime - d_slice.meta.starttime
        print "SHORT"
        raise AttributeError

    p_slice = p.slice(d_slice.meta.starttime, d_slice.meta.endtime)
    # Must be a single trace
    if len(p_slice.traces) != 1:
        print "MUCH"
        raise AttributeError

    p_slice = p_slice.traces[0]

    sta = max(p_slice.meta.starttime, d_slice.meta.starttime)
    end = min(p_slice.meta.endtime, d_slice.meta.endtime)

    if end - sta < 18000:
        print "SHORT"
        raise AttributeError

    return Stream().append(d_slice).slice(sta, end), Stream().append(p_slice).slice(sta, end)


def update_stats(tr, stla, stlo, stel, ws, ss):
    tr.stats.sac = AttribDict()
    tr.stats.sac.stla = stla
    tr.stats.sac.stlo = stlo
    tr.stats.sac.stel = stel
    tr.stats.sac.user8 = ws
    tr.stats.sac.user9 = ss

    return tr


def load_db(fname):
    db = pickle.load(open(fname, 'rb'))
    for k, v in db.items():
        db[k] = meta_data(v)
    return db


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


if __name__ == '__main__':

    sta_keys = ['AXCC1']

    dbfile = 'stations.pkl'

    stationdb = load_db(dbfile)

    for key in sta_keys:
        process(stationdb, key)
