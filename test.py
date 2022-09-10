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

base_url = r"https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=WS50M&community=SB&longitude={longitude}&latitude={latitude}&start=20210602&end=20220529&format=json"

wind_power_speed = pd.read_csv("wind_power_speed.csv",names=["date","power"],parse_dates=['date'])
print(wind_power_speed)

for latitude, longitude,name in locations[:60]:
        locations.remove((latitude, longitude,name))
        print(latitude, longitude,name)

        api_request_url = base_url.format(longitude=longitude, latitude=latitude)
        data = {}
        response = requests.get(url=api_request_url, verify=True, timeout=30.00)


        content = json.loads(response.content.decode('utf-8'))['properties']['parameter']['WS50M']
        df = pd.json_normalize(content).T
        df = df.reset_index(level=0)
        df.columns = ["date",name]
        df["date"] = pd.to_datetime(df['date'],format="%Y%m%d%H")
        print(df)
        wind_power_speed = wind_power_speed.join(df.set_index('date'),on='date')
        print(wind_power_speed.head(30))
        break