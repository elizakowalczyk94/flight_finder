import pandas
import requests
import os
from dotenv import load_dotenv

load_dotenv("venv/.env")

KIWI_LINK = os.getenv("KIWI_LINK")
KIWI_KEY = os.getenv("KIWI_KEY")
CSV_FILE = "cities_to_follow.csv"


class DataManager:

    def __init__(self):
        self.kiwi_iata_endpoint = KIWI_LINK + "/locations/query"
        self.kiwi_key = {"apikey": KIWI_KEY}

        self.write_iata_to_csv()
        self.city_file = pandas.read_csv(CSV_FILE, delimiter=",")

    def get_iata(self, city_name):
        kiwi_json = requests.get(url=self.kiwi_iata_endpoint,
                                 params={"term": city_name},
                                 headers=self.kiwi_key).json()
        city_iata = kiwi_json["locations"][0]["code"]
        return city_iata

    def write_iata_to_csv(self):
        df_without_iata = pandas.read_csv(CSV_FILE, delimiter=",")
        dict_iata = {"city": [c.title() for c in df_without_iata.city.tolist()],
                     "max_price": df_without_iata.max_price.tolist(),
                     "iata": [self.get_iata(c.title()) for c in df_without_iata.city]}
        df_with_iata = pandas.DataFrame(dict_iata)
        df_with_iata.to_csv(CSV_FILE, index=False)
