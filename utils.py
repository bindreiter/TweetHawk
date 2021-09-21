import datetime
from time import time

def timeElapsedString(timeDelta):
    if timeDelta == None:
        return "Never"

    print(str(datetime.datetime.now()))
    
    timeNow =  datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    timeDelta = timeNow - datetime.datetime.strptime(str(timeDelta), '%Y-%m-%d %H:%M:%S')
    print(timeDelta.days)
    if int(timeDelta.days > 0):
        if int(timeDelta.days) == 1:
            return '1 day ago'
        else:
            return '%s days ago' % int(timeDelta.days)
    elif int(timeDelta.seconds / 3600) > 0:
        if int(timeDelta.seconds / 3600) == 1:
            return '1 hour ago'
        else:
            return '%s hours ago' % int(timeDelta.seconds / 3600)
    elif int(timeDelta.seconds / 60) < 2:
        return '1 minute ago'
    else:
        return '%s minutes ago' % int(timeDelta.seconds / 60) 