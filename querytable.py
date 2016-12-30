import sqlite3
from datetime import *
from dateutil.relativedelta import *

def calcdurhr(begin,end):
    begin=datetime.strptime(begin,"%a %b %d %Y at %H:%M")
    end=datetime.strptime(end,"%a %b %d %Y at %H:%M")
    t=relativedelta(end,begin)
    return t.days*24+t.hours+t.minutes/60.0


def dumptable(tablename,conn):
    conn.row_factory=sqlite3.Row
    r=conn.cursor()
    r.execute('select * from {tn}'.format(tn=tablename))
    entries=r.fetchmany(100)
    avgdurhr=0
    count=0
    print "|  begin                     | elapsed (hr) |rating"
    #       |  Wed Dec 21 2016 at 17:39  |  Wed Dec 21 2016 at 20:39  |  3.0  |  no
    for e in entries:
        elapsed=calcdurhr(e['time'],e['duration'])
        lenstr=9-len(str(elapsed))
        print "| ", e['time'], " | ", " "*lenstr, "%0s" %elapsed, " | ", e['rating']
        avgdurhr+=elapsed
        count+=1
    print "average hours were " + str(avgdurhr/count)