import os, json, requests, csv, re, random, threading
import pandas as pd
from datetime import datetime

locations = []

with open("wind_farms_data.csv", 'r', newline='', encoding='UTF-8') as f:
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            if int(row[3]) >= 0:
                locations.append((float(row[4]), float(row[5]),row[0]))
        line_count += 1

locations = list(dict.fromkeys(locations))

base_url = r"https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=WS50M&community=SB&longitude={longitude}&latitude={latitude}&start=20160901&end=20220901&format=json"

wind_power_speed = pd.read_csv("wind_power_5y_processed.csv",parse_dates=['datetime'])
print(wind_power_speed)

import numpy as np
slices = 8
locations_slices = np.array_split(locations, slices)

def get_wind_speed_for_locations(locations,index,wind_power_speed):
    for latitude, longitude,name in locations:
        #locations.remove((latitude, longitude,name))
        print(latitude, longitude,name)

        api_request_url = base_url.format(longitude=longitude, latitude=latitude)
        response = requests.get(url=api_request_url, verify=True)

        content = json.loads(response.content.decode('utf-8'))['properties']['parameter']['WS50M']
        data[name] = list(content.values())
        print(len(data[name]))

    values = pd.DataFrame.from_dict(data)
    values["datetime"] = pd.to_datetime(list(content.keys()),format="%Y%m%d%H")
    wind_power_speed = wind_power_speed.join(values.set_index('datetime'),on='datetime')
    print(wind_power_speed.head(15))
    wind_power_speed.to_csv("result" + str(index) + ".csv",index=False)

for i in range(slices):
    data = {}
    get_wind_speed_for_locations(locations_slices[i],i,wind_power_speed)