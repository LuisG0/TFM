import os, json, requests, csv, re, random, threading
import pandas as pd
from datetime import datetime

wind_power_speed = pd.read_csv("../data/result.csv")
print(wind_power_speed.info())
wind_power_speed = wind_power_speed.dropna()
print(wind_power_speed.info())
wind_power_speed.to_csv("../data/hourly_data.csv",index=False)