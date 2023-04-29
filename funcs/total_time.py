import datetime

def totaltime(start, end, c):
    ttl = {}
    ttl['time'] = end - start
    ttl['dinner'] = datetime.timedelta(hours=0)
    if ttl["time"] >= datetime.timedelta(hours=4):
        ttl['dinner'] = datetime.timedelta(minutes=30)
    if ttl["time"] >= datetime.timedelta(hours=6):
        ttl['dinner'] = datetime.timedelta(hours=1)
    ttl['total'] = (ttl['time'] - ttl['dinner']) * c
    ttl['totalfloat'] = float(ttl['total'].seconds/3600)
    if ttl['total'].days > 0:
        ttl['totalfloat'] += ttl['total'].days*24
    ttl['c'] = c
    return ttl
