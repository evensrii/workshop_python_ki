import requests
import pandas as pd
from pyjstat import pyjstat

# Endepunkt for SSB tabell 07459
url = "https://data.ssb.no/api/v0/no/table/07459/"

# Spørring mot SSB API
query = {
  "query": [
    {
      "code": "Region",
      "selection": {
        "filter": "agg:KommSummer",
        "values": [
          "K-3212",
          "K-3214",
          "K-3216",
          "K-3218"
        ]
      }
    },
    {
      "code": "Alder",
      "selection": {
        "filter": "vs:AlleAldre00B",
        "values": []
      }
    },
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "2024",
          "2025"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

# Send POST-forespørsel
response = requests.post(url, json=query)

if response.status_code == 200:
    print("Forespørsel vellykket!")
    dataset = pyjstat.Dataset(response.json())
    df = dataset.write('dataframe')
    print(df.head())
    df.to_csv("ssb_07459_data.csv", index=False)
else:
    print(f"Feil ved henting av data. Statuskode: {response.status_code}")
    print(response.text)
