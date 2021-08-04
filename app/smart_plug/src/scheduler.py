from time_util import mins_to_hour

def hourly_power_level(temp, max=52, min=23):
    return (max-temp)/(max-min)


def optimize_power_mins_on_time(mins, power_mins):
    hour = mins_to_hour(mins)
    result = power_mins

    if hour >= 18 and hour < 24: # when the house radiator is on
        # 11PM before
        result = result * 0.6

    elif hour >= 0 and hour <= 3: 
        result = result * 0.9

    elif hour > 3 and  hour < 6:
        result = result * 0.8

    elif hour >= 6 and hour < 9:
        result = result * 0.6
    
    elif hour >= 8 and hour <= 12:
        result = result * 0.5

    else:
        result = result

    return result



def group_hourly_power_mins(group_size, hourly_power_mins):
    assert len(hourly_power_mins)%group_size == 0, "group size{} cannot be divided by the total hourly_power_mins size: {}".format(group_size, len(hourly_power_level))

    count = 0
    grouped_power_mins = []
    start_mins = 0
    agg = 0
    for item in hourly_power_mins:
        mins = item["mins"]
        optimize_grouped_power_mins = item["optimized_power_on_mins"]
        if count == 0:
            start_mins = item["mins"]
            agg += optimize_grouped_power_mins
            count += 1
        elif count == (group_size-1):
            grouped_power_mins.append((start_mins, mins+60, agg+optimize_grouped_power_mins))
            agg = 0
            count = 0
        else:
            agg += optimize_grouped_power_mins
            count += 1
    return grouped_power_mins


def display_message(grouped_schedule, group_size):
    if grouped_schedule:
        total_hour = 0
        start_hour = mins_to_hour(grouped_schedule[0][0])
        end_hour = mins_to_hour(grouped_schedule[-1][1])

        for s, e, p_mins in grouped_schedule:
            if p_mins >= group_size*60: 
                total_hour += group_size
            else:
                total_hour += p_mins/60
        print("group_size: {}, group schedule: {}".format(group_size, grouped_schedule))
        print("total hour: {}, hour range: {}-{}".format(total_hour, start_hour, end_hour))

# combine adjacent groups (fully powered group)
# drop power_mins that are below threshhold
# construct command: (mins, 0 or 1(on/off))
def optimize_grouped_schedule_and_make_command(grouped_schedule, drop_threshold, group_size):
    command = []
    length = len(grouped_schedule)

    grouped_schedule = [g for g in grouped_schedule if g[2]>drop_threshold]

    display_message(grouped_schedule, group_size)

    prev_continuous = False
    for i, (start, end, power_mins) in enumerate(grouped_schedule):
        if (start + power_mins) < end:
            if prev_continuous:
                command.append((start+power_mins, 0))
            else:
                command.append((start, 1))
                command.append((start+power_mins, 0))
            agg_powers = 0
            prev_continuous = False
        else: # continuous block
            if prev_continuous: 
                if i == (length - 1): # the last block
                    command.append((end, 0))
            else:
                command.append((start, 1))
                if i == (length - 1):
                    command.append((end, 0))
            prev_continuous = True
    return command


def get_compute_temp(temp, feel_like):
    return (temp*2+feel_like)/3


def compute_hourly_schedule(temps, adjustment_rate):
    hourly_temps = []
    for item in temps:
        temp_avg = get_compute_temp(item["temp"], item["feel_like"])
        mins = item["mins"]
        rate = hourly_power_level(temp_avg)
        power_on_mins = rate * 60

        item["power_on_mins"] = power_on_mins
        item["optimized_power_on_mins"] = int(optimize_power_mins_on_time(mins, power_on_mins)*adjustment_rate)
        hourly_temps.append(item)
    return hourly_temps


def compute_schedule(temps, group_size, hourly_threshold=30, adjustment_rate=1.0):
    hourly_schedule = compute_hourly_schedule(temps, adjustment_rate)
    grouped_schedule = group_hourly_power_mins(group_size, hourly_schedule)
    command = optimize_grouped_schedule_and_make_command(grouped_schedule, hourly_threshold, group_size)
    return command

# def slice_schedule(start_hour, end_hour, schedules):
#     start_mins = start_hour * 60
#     end_mins = end_hour * 60
#     out = []
#     for s,e, mins in schedules:
#         if e > start_mins and s < end_mins:
#             out.append((s, e, mins))
#     return out

