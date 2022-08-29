import os, json, requests, csv, re, random, threading
import pandas as pd
from datetime import datetime

def parse_date(date):
    parts = re.split('[T\-]+', date[0:date.find(':')])
    parsed = parts[0] + parts[1] + parts[2] + parts[3]
    return parsed

custom_date_parser = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f")


def update_data():
    random.shuffle(locations)

    cont = 0

    wind_power_speed = pd.read_csv("wind_power_speed.csv",names=["date","power"],parse_dates=['date'])
    wind_power_speed["date"] = wind_power_speed["date"].apply(parse_date)


    for latitude, longitude,name in locations[:60]:
        locations.remove((latitude, longitude))

        api_request_url = base_url.format(longitude=longitude, latitude=latitude)
        data = {}
        response = requests.get(url=api_request_url, verify=True, timeout=30.00)

        try:
            content = json.loads(response.content.decode('utf-8'))['properties']['parameter']['WS50M']
            attrs = []
            vals = []

            for attr, val in content.items():
                attrs.append(attr)
                vals.append(val)

        except:
            cont += 1
            continue

        

        file_data = []

        with open('wind_power_speed.csv', 'r') as input:
            csv_reader = csv.reader(input)

            for row in csv_reader:
                file_data.append(row)

        with open('wind_power_speed.csv', 'w', newline='') as out:
            csv_writer = csv.writer(out)

            for row in file_data:
                try:
                    csv_writer.writerow(row + [data[parse_date(row[0])]])
                except KeyError as e:
                    print(e)
                    pass

        print(cont)

    print('a esperar')
    #threading.Timer(3660, update_data).start()


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

update_data()
# random.shuffle(locations)
#
# cont = 0
#
# for latitude, longitude in locations[:60]:
#     api_request_url = base_url.format(longitude=longitude, latitude=latitude)
#     data = {}
#     response = requests.get(url=api_request_url, verify=True, timeout=30.00)
#
#     try:
#         content = json.loads(response.content.decode('utf-8'))['properties']['parameter']['WS50M']
#
#         print(content)
#
#         for attr, val in content.items():
#             data[attr] = val
#
#     except:
#         print('a')
#         cont += 1
#         continue
#
#     file_data = []
#
#     with open('wind_power_speed.csv', 'r') as input:
#         csv_reader = csv.reader(input)
#
#         for row in csv_reader:
#             file_data.append(row)
#
#     with open('wind_power_speed.csv', 'w', newline='') as out:
#         csv_writer = csv.writer(out)
#
#         for row in file_data:
#             try:
#                 csv_writer.writerow(row + [data[parse_date(row[0])]])
#             except KeyError as e:
#                 print(e)
#                 pass
#
#     print(cont)




# with open('wind_power_speed.csv', 'w', newline='') as out, open("wind_power.csv", 'r') as input:
#     csv_reader = csv.reader(input)
#     csv_writer = csv.writer(out)
#     for row in csv_reader:
#         csv_writer.writerow([row[0], row[1]] + data[parse_date(row[0])])
#
# print(data)