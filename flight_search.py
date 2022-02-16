import requests
import datetime
import data_manager
import flight_data
import os
from dotenv import load_dotenv

load_dotenv()

KIWI_ENDPOINT = os.getenv("KIWI_ENDPOINT")
KIWI_KEY = os.getenv("KIWI_KEY")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self, departure_airport, arrival_airports):
        self.sheety_manager = data_manager.DataManager()
        self.kiwi_iata_endpoint = KIWI_ENDPOINT + "/locations/query"
        self.kiwi_key = {"apikey": KIWI_KEY}

        self.departure_airport = departure_airport
        self.arrival_airports = arrival_airports
        self.kiwi_flight_data = KIWI_ENDPOINT + "/v2/search"
        self.tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
        self.half_year = datetime.datetime.today() + datetime.timedelta(days=6 * 30)

    def write_iata(self, city_name):
        city_name = city_name.title()
        city_list = self.sheety_manager.read_sheety()["prices"]
        for city_dict in city_list:
            if city_dict["city"] == city_name:
                obj_id = city_dict["id"]
                kiwi_json = requests.get(url=self.kiwi_iata_endpoint,
                                         params={"term": city_name},
                                         headers=self.kiwi_key).json()
                iata = kiwi_json["locations"][0]["code"]
                iata_json = {"price": {"iataCode": iata}}
                self.sheety_manager.modify_sheety(obj_id=obj_id, json_data=iata_json)
            else:
                return False

    def search_direct_flights(self):
        search_flight_params = {
            "fly_from": self.departure_airport,
            "fly_to": self.arrival_airports,
            "date_from": self.tomorrow_date.strftime("%d/%m/%Y"),
            "date_to": self.half_year.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "PLN"}

        flight_kiwi = requests.get(url=self.kiwi_flight_data, params=search_flight_params, headers=self.kiwi_key)

        try:
            print(flight_kiwi.json()["data"][0])
            flight_kiwi = flight_kiwi.json()["data"][0]
        except IndexError:
            print("No flight found for the destination.")
            return None

        flight_data_kiwi = flight_data.FlightData(
            price=flight_kiwi["price"],
            departure_city=flight_kiwi["cityFrom"],
            departure_airport=flight_kiwi["cityCodeFrom"],
            arrival_city=flight_kiwi["cityTo"],
            arrival_airport=flight_kiwi["cityCodeTo"],
            departure_date=flight_kiwi["local_departure"].split("T")[0],
            arrival_date=flight_kiwi["local_arrival"].split("T")[0])

        return flight_data_kiwi
