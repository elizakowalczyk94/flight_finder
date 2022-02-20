import requests
import datetime
import flight_data
import os
from dotenv import load_dotenv

load_dotenv("venv/.env")

KIWI_ENDPOINT = os.getenv("KIWI_ENDPOINT")
KIWI_KEY = os.getenv("KIWI_KEY")


class FlightSearch:

    def __init__(self, departure_iata, arrival_iata):
        self.kiwi_iata_endpoint = KIWI_ENDPOINT + "/locations/query"
        self.kiwi_key = {"apikey": KIWI_KEY}
        self.kiwi_flight_data = KIWI_ENDPOINT + "/v2/search"
        self.departure_iata = departure_iata
        self.arrival_iata = arrival_iata
        self.tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
        self.half_year = datetime.datetime.today() + datetime.timedelta(days=6 * 30)

    def search_direct_flights(self):
        search_flight_params = {
            "fly_from": self.departure_iata,
            "fly_to": self.arrival_iata,
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
            flight_kiwi = flight_kiwi.json()["data"][0]
        except IndexError:
            print(f"No flight found for {self.arrival_iata}.")
            return False

        flight_data_kiwi = flight_data.FlightData(
            price=flight_kiwi["price"],
            departure_city=flight_kiwi["cityFrom"],
            departure_airport=flight_kiwi["flyFrom"],
            arrival_city=flight_kiwi["cityTo"],
            arrival_airport=flight_kiwi["flyTo"],
            departure_date=flight_kiwi["route"][0]["local_departure"].split("T")[0],
            return_date=flight_kiwi["route"][1]["local_arrival"].split("T")[0],
            airline=flight_kiwi["airlines"][0],
            kiwi_link=flight_kiwi["deep_link"])

        return flight_data_kiwi
