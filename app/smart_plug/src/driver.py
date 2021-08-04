from open_weather_client import get_hourly_weather
from scheduler import compute_schedule
from tp_link_sp_controller import send_schedule_cmd, clean_schedule
from time_util import mins_to_mins

from datetime import datetime
import pytz
import functools

import logging


ip = "192.168.3.248"


"""##### TODO #####
Add arg parser:
    dry run 
    ip 
    clean schedule only 


    start hour 
    group size

"""

def reschedule_today(commands):
    if commands:
        clean_schedule(ip)

    for mins, on_off in commands:
        send_schedule_cmd(mins_to_mins(mins), on_off, ip)


# temps = [
#     40, 40, 40, #10PM, 11PM, 12PM
#     39, 39, 39, #1AM. 2AM, 3AM
#     38, 38, 38, #4AM, 5AM, 6AM
#     38, 39, 40, #7AM, 8AM, 9AM
#     41, 43, 45  #10AM, 11AM, 12PM
#     ]

# start at 22:00 local time
start_hour = 1
length = 8
#shift = -1
group_size = 2
hourly_threashold = 20
adjustment_rate = 0.70

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

api_temps = get_hourly_weather(start_hour, length)
logging.info("start_hour: {}, length: {}, group_size: {}, hourly_threashold: {}, adjustment_rate: {}". \
    format(start_hour, length, group_size, hourly_threashold, adjustment_rate))
logging.info("api_temps: {}".format(api_temps)) # will not print anything

#print("api_temps: {}".format(api_temps))
commands = compute_schedule(api_temps, group_size, hourly_threashold, adjustment_rate)
reschedule_today(commands)


# total = 0
# for s,e,p in schedules:
#     total += p
# if schedules:
#     print ("total hours range {}-{}, total power on hours: {}".format(schedules[0][0]/60, schedules[-1][1]/60%24, round(total/60, 1)))
#     print ("current datetime: {}".format(datetime.now(pytz.timezone('America/New_York')).strftime("%m/%d/%y %H:%M:%S")))
