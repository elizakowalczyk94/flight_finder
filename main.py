# Day 39 capstone project - Flight Deal Finder.
# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve
# the program requirements.

import data_manager
import flight_search

DEPARTURE_CITY = "Katowice"

sheety_manager = data_manager.DataManager()

# sheety_data json is used because number of requests for Sheety is exceeded.
sheety_data = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 54, 'id': 2},
                          {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 42, 'id': 3},
                          {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 485, 'id': 4},
                          {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 551, 'id': 5},
                          {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 95, 'id': 6},
                          {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 414, 'id': 7},
                          {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 240, 'id': 8},
                          {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 260, 'id': 9},
                          {'city': 'Cape Town', 'iataCode': 'CPT', 'lowestPrice': 378, 'id': 10}]}

# for city_dict in sheety_manager.read_sheety()["prices"]:
for city_dict in sheety_data["prices"]:
    f_search = flight_search.FlightSearch(departure_airport=DEPARTURE_CITY, arrival_airports=city_dict["city"])
    f_search.write_iata(city_name=city_dict["city"])
    flight_found = f_search.search_direct_flights()
    min_price = city_dict["lowestPrice"]
    if flight_found.price <= min_price:
        message = f"There is a flight from {flight_found.departure_city} ({flight_found.departure_airport}) " \
                  f"to {flight_found.arrival_city} ({flight_found.arrival_airport}). " \
                  f"Departure on {flight_found.departure_date}. The price is only {flight_found.price} PLN."
        print(message)
