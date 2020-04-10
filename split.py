# coding=utf-8
"""
将下载的原始数据按天分割
放到download文件夹下运行，在raw文件夹下产生文件
"""
from obspy import read
import os


def process():
    path = "./"
    files = os.listdir(path)
    copy = list(files)
    for f in copy:
        if not f.endswith("SAC"):
            files.remove(f)

    files = sorted(files)

    for f in files:
        print f
        work_on_SAC(f)


def work_on_SAC(file):
    f = read(file, 'SAC')
    t = f[0]

    net = str(t.stats.network)
    sta = str(t.stats.station)
    cha = str(t.stats.channel)

    pts = len(t)
    sample_rate = 200
    if cha == "BHZ":
        sample_rate = 40
    daypts = 3600. * 24 * sample_rate
    days = pts // daypts

    hash = "." + str(file.split(".")[-2])[:-3]
    f_pre = "../raw/"

    if days < 1:
        fname = f_pre + ".".join(file.split(".")[:-2]) + hash + ".SAC"
        t.write(fname, 'SAC')
        print fname
        return

    tstart = t.stats.starttime
    tend = tstart + 3600. * 24

    for i in range(int(days)):
        yr = str(tstart.year).zfill(4)
        jd = str(tstart.julday).zfill(3)
        fname = f_pre + net + "." + sta + ".." + cha + ".M." + yr + "." + jd + hash + ".SAC"
        cur_t = t.slice(tstart, tend)
        # cur_t = t.trim()
        cur_t.stats.sac['b'] = 0
        cur_t.stats.sac['e'] = 3600. * 24
        cur_t.stats.sac['nzjday'] = int(jd)
        cur_t.write(fname, 'SAC')
        print fname
        tstart = tend
        tend = tstart + 3600. * 24

    # last one
    yr = str(tstart.year).zfill(4)
    jd = str(tstart.julday).zfill(3)
    fname = f_pre + net + "." + sta + ".." + cha + ".M." + yr + "." + jd + hash + ".SAC"
    cur_t = t.slice(tstart)
    cur_t.stats.sac['b'] = 0
    cur_t.stats.sac['e'] = (cur_t.stats.endtime - tstart)
    cur_t.stats.sac['nzjday'] = int(jd)
    cur_t.write(fname, 'SAC')
    print fname


if __name__ == "__main__":
    process()
