import datetime

def convert_time(date, time):
    try:
        r_time = time.replace(':', '.').replace(' ', '.')
        n_time = r_time.split('.')
        res = datetime.datetime(date.year, date.month, date.day, int(n_time[0]), int(n_time[1]), 0, 0)
        return res
    except:
        return False