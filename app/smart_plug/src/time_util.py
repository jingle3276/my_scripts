
from datetime import datetime
import pytz

new_york_tz = pytz.timezone('America/New_York')



def mins_to_hour(mins):
    return mins%1440/60


def hour_to_mins(the_hour):
    return the_hour*60

def mins_to_mins(mins):
    return mins%1440

def dt_to_local_date(dt):
    return datetime.datetime.fromtimestamp(dt)


def local_time_in_timestamp(the_hour):
    local_now = datetime.now(new_york_tz)
    local_time = local_now.replace(hour=the_hour, minute=00, second=00, microsecond=00)
    return local_time.timestamp()


# convert unix timestamp dt in utc to tp link min integer
# 
def dt_to_mins(timestamp):
    local_datetime = datetime.fromtimestamp(timestamp, new_york_tz)
    the_hour = local_datetime.timetz().hour
    return hour_to_mins(the_hour)
