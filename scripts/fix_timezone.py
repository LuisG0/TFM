import os, json, requests, csv, re, random, threading
import pandas as pd
from datetime import datetime

wind_power_speed = pd.read_csv("wind_power_5y.csv",sep=";",usecols=["value","datetime"])
print(wind_power_speed.info())

wind_power_speed["datetime"] = wind_power_speed["datetime"].str.split("+").str[0]
print(wind_power_speed.info())
print(wind_power_speed.head())
wind_power_speed = wind_power_speed.groupby("datetime").mean()
print(wind_power_speed.info())
print(wind_power_speed.head())

wind_power_speed.to_csv("wind_power_5y_processed.csv")