#!/usr/bin/env python3

import requests
import json

apikey = ""
with open("apikey.txt", "r") as f:
    apikey = next(f).strip()

payload = {"access_key": apikey, "symbols": "USD,SEK"}

data = []

for year in range(2011, 2017 + 1):
    for month in range(1, 12 + 1):
        url = f"http://data.fixer.io/api/{year}-{month:02}-15"
        r = requests.get(url, params=payload)
        j = r.json()
        data.append(j)

with open("currency-data.json", "w") as f:
    json.dump(data, f, indent=4)
