import requests
from time_util import local_time_in_timestamp, dt_to_mins, hour_to_mins

Open_Weather_Map_API_URL = "http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=imperial&exclude=minutely,daily,alerts&appid={}"
Open_Weather_Map_API_KEY = "0343d0eb4489e660fe2f8992c7dda4a1"
lat=40.752792
lon=-73.880127

def get_today_weather_from_api():
    url = Open_Weather_Map_API_URL.format(lat, lon, Open_Weather_Map_API_KEY)
    #print("url: {}".format(url))
    response = requests.get(url)
    return response.json()


#def get_hourly_weather(start_timestamp=local_time_in_timestamp(22), length=12):
def get_hourly_weather(start_hour, length=12):
    start_timestamp = local_time_in_timestamp(start_hour)
    start_mins = hour_to_mins(start_hour)
    obj = get_today_weather_from_api()
    hourly = obj["hourly"]

    out = []
    count = 0
    for hour_obj in hourly:
        if count == length:
            return out

        #mins = dt_to_mins(hour_obj["dt"])
        if hour_obj["dt"] >= start_timestamp:
            #avg = (hour_obj["temp"] + hour_obj["feels_like"]) / 2
            #out.append((hour_obj["dt"], avg))
            obj = {
                "mins": start_mins + count*60,
                "temp": hour_obj["temp"],
                "feel_like": hour_obj["feels_like"]
            }
            out.append(obj)
            count += 1
