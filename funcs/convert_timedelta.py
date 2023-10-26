def converttimedelta(td):
    sec = td.seconds
    hours = sec//3600
    mins = (sec - hours*3600)//60
    str(mins)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(mins)) == 1:
        mins = "0" + str(mins)
    return f'{hours}:{mins}'
