from email.utils import parsedate
import os, json, requests, csv, re, random, threading
import pandas as pd
from datetime import datetime

results = pd.read_csv("../data/result0.csv",parse_dates=["datetime"])
print(results.info())

for i in range(1,120):
    if i == 119:
        resultsAux = pd.read_csv("../data/result"+ str(i) + ".csv",usecols=range(2,11))
    else:
        resultsAux = pd.read_csv("../data/result"+ str(i) + ".csv",usecols=range(2,12))
    results = pd.concat([results, resultsAux], axis=1)

print(results.info())  
results.to_csv("../data/result.csv",index=False)