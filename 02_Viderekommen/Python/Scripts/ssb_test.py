#### Dette er et testscript for å spørre etter og behandle data fra SSBs API.
#### Marker kode og trykk "Shift + Enter" for å kjøre den valgte koden.

######## Laste nødvendige (standard-)pakker

import requests  # For å kjøre spørringer mot alle mulige APIer ++
import pandas as pd  # For å håndtere data i tabellform. Standard i "Data science"
from pyjstat import pyjstat  # Anbefalt av SSB for å håndtere JSON-stat2 formatet

######## Hente data fra SSB API

# Endepunkt for SSB API
url = "https://data.ssb.no/api/v0/no/table/11607/"

# Spørring fra SSB API (hentet fra "API-spørring for denne tabellen" etter søk i Statistikkbanken)
query = {
  "query": [
    {
      "code": "Region",
      "selection": {
        "filter": "agg_single:Komm2020",
        "values": [
          "3806",
          "3807",
          "3808",
          "3812",
          "3813",
          "3814",
          "3815",
          "3816",
          "3817",
          "3818",
          "3819",
          "3820",
          "3821",
          "3822",
          "3823",
          "3824",
          "3825"
        ]
      }
    },
    {
      "code": "Alder",
      "selection": {
        "filter": "item",
        "values": [
          "15-74"
        ]
      }
    },
    {
      "code": "Kjonn",
      "selection": {
        "filter": "item",
        "values": [
          "0",
          "2",
          "1"
        ]
      }
    },
    {
      "code": "Landbakgrunn",
      "selection": {
        "filter": "item",
        "values": [
          "tot",
          "abc",
          "zzz",
          "ddd",
          "eee"
        ]
      }
    },
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "Sysselsatte2"
        ]
      }
    },
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "2022",
          "2023"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

######## Spørring vha. "requests"-modulen (Promt til ChatGPT: "Gi meg Python-kode for å hente data fra SSBs API ved hjelp av følgende kode: [limte inn alt over denne linjen]")

# Send POST-forespørselen
response = requests.post(url, json=query)

# Sjekk om forespørselen var vellykket
if response.status_code == 200:
    print("Forespørsel vellykket!")

    # Last JSON-stat2-data direkte til Dataset-objektet
    dataset = pyjstat.Dataset(response.json())

    # Konverter dataset til pandas DataFrame
    df = dataset.write("dataframe")

    # Skriv ut DataFrame for å verifisere data
    print(df.head())
else:
    print(f"Feil ved henting av data. Statuskode: {response.status_code}")
    print(response.text)


######## Leke seg med datasett (kalles en "dataframe" i pandas)

## Skriv # etterfulgt av en enkel beskrivelse av hva du ønsker å gjøre med datasettet.
## Trykk "Enter", vent på forslag fra Github Copilot, og trykk "Tab" for å godta forslaget.

# Vis grunnleggende info om datasettet
df.info()

# Vis de første 5 radene i datasettet
df.head()



## TIPS: Dobbeltklikke på en enkeltvariabel (f. eks. "df") og trykk "Shift + Enter" for å se innholdet i variabelen.
# Sammenlikne f. eks. "print(df)" med å dobbeltklikke på "df" og trykke "Shift + Enter"

######## Til slutt: Skrive endelig dataframe (df) til .csv-fil med ditt navn
df.to_csv("ssb_data_ditt_navn.csv", index=False)
