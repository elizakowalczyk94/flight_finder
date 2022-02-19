import pandas
import requests
import os
from dotenv import load_dotenv

load_dotenv("venv/.env")

KIWI_ENDPOINT = os.getenv("KIWI_ENDPOINT")
KIWI_KEY = os.getenv("KIWI_KEY")
CSV_FILE = "cities_to_follow.csv"


class DataManager:

    def __init__(self, cities_list, prices_list):
        self.kiwi_iata_endpoint = KIWI_ENDPOINT + "/locations/query"
        self.kiwi_key = {"apikey": KIWI_KEY}

        self.cities_to_csv = [city.title() for city in cities_list]
        self.prices_to_csv = prices_list
        self.iata_to_csv = []
        for city in self.cities_to_csv:
            self.iata_to_csv.append(self.write_iata(city_name=city))
        self.create_csv()
        self.city_file = pandas.read_csv(CSV_FILE, delimiter=",")
        print(self.city_file)

    def write_iata(self, city_name):
        kiwi_json = requests.get(url=self.kiwi_iata_endpoint,
                                 params={"term": city_name},
                                 headers=self.kiwi_key).json()
        city_iata = kiwi_json["locations"][0]["code"]
        return city_iata

    def create_csv(self):
        cities_dict = {"city": self.cities_to_csv,
                       "max_price": self.prices_to_csv,
                       "iata": self.iata_to_csv}
        cities_data_frame = pandas.DataFrame(cities_dict)
        cities_data_frame.to_csv(CSV_FILE, index=False)

# import os
# import requests
# from dotenv import load_dotenv
#
# load_dotenv("venv/.env")
# SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
# TOKEN = os.getenv("TOKEN")
#
#
# class DataManager:
#    # This class is responsible for talking to the Google Sheet.
#
#    def __init__(self):
#        self.bearer_headers = {"Authorization": TOKEN}
#
#    def read_sheety(self):
#        response = requests.get(url=SHEETY_ENDPOINT, headers=self.bearer_headers)
#        response_json = response.json()
#        return response_json
#
#    def write_sheety(self, json_data):
#        response = requests.post(url=SHEETY_ENDPOINT, json=json_data, headers=self.bearer_headers)
#        return response
#
#    def modify_sheety(self, obj_id, json_data):
#        response = requests.put(url=f"{SHEETY_ENDPOINT}/{obj_id}", json=json_data, headers=self.bearer_headers)
#        return response
#
