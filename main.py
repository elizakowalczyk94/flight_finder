# Day 39 capstone project - Flight Deal Finder.
# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve
# the program requirements.

import data_manager
import flight_search
import notification_manager

DEPARTURE_CITY = "Warsaw"

csv_manager = data_manager.DataManager(cities_list=["Paris", "New york", "CRACOW"], prices_list=[400, 3000, 150])
csv_data = csv_manager.city_file
DEPARTURE_IATA = csv_manager.get_iata(DEPARTURE_CITY)

for destination_iata in csv_data.iata:
    flight_object = flight_search.FlightSearch(departure_iata=DEPARTURE_IATA, arrival_iata=destination_iata)
    flight_found = flight_object.search_direct_flights()
    if flight_found:
        print(DEPARTURE_CITY, "-->", flight_found.arrival_city, flight_found.departure_date,
              "with", flight_found.airline, flight_found.kiwi_link)
