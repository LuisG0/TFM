import os, json, requests, csv, re, random, threading
import pandas as pd
from datetime import datetime

wind_power_speed = pd.read_csv("wind_power_5y_processed.csv")
print(wind_power_speed.info())
