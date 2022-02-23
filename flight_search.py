import requests
import datetime
import flight_data
import os
from dotenv import load_dotenv

load_dotenv("venv/.env")

KIWI_LINK = os.getenv("KIWI_LINK")
KIWI_KEY = os.getenv("KIWI_KEY")


class FlightSearch:

    def __init__(self):
        self.kiwi_iata_endpoint = KIWI_LINK + "/locations/query"
        self.kiwi_key = {"apikey": KIWI_KEY}
        self.kiwi_flight_endpoint = KIWI_LINK + "/v2/search"

        self.tomorrow_date = datetime.datetime.today() + datetime.timedelta(days=1)
        self.half_year = datetime.datetime.today() + datetime.timedelta(days=6 * 30)

    def search_direct_flights(self, departure_iata, arrival_iata):
        search_flight_params = {
            "fly_from": departure_iata,
            "fly_to": arrival_iata,
            "date_from": self.tomorrow_date.strftime("%d/%m/%Y"),
            "date_to": self.half_year.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 10,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "PLN"}

        flight_kiwi = requests.get(url=self.kiwi_flight_endpoint, params=search_flight_params, headers=self.kiwi_key)

        try:
            flight_kiwi = flight_kiwi.json()["data"][0]
        except IndexError:
            # TODO: why 2 Maybe 1 is return stop over?
            search_flight_params["max_stopovers"] = 2
            flight_kiwi = requests.get(url=self.kiwi_flight_endpoint, params=search_flight_params,
                                       headers=self.kiwi_key)

            # TODO: Another way than nested try-except?
            try:
                flight_kiwi = flight_kiwi.json()["data"][0]
            except IndexError:
                flight_data_kiwi = None
            else:
                flight_data_kiwi = flight_data.FlightData(
                    price=flight_kiwi["price"],
                    departure_city=flight_kiwi["cityFrom"],
                    departure_airport=flight_kiwi["flyFrom"],
                    arrival_city=flight_kiwi["cityTo"],
                    arrival_airport=flight_kiwi["flyTo"],
                    departure_date=flight_kiwi["route"][0]["local_departure"].split("T")[0],
                    return_date=flight_kiwi["route"][2]["local_arrival"].split("T")[0],
                    airline=flight_kiwi["airlines"][0],
                    kiwi_link=flight_kiwi["deep_link"],
                    stop_overs=1,
                    via_city=flight_kiwi["route"][0]["cityTo"])

        else:
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
