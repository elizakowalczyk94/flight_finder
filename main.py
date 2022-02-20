# Day 39 capstone project - Flight Deal Finder.

import data_manager
import flight_search
import notification_manager

DEPARTURE_CITY = "Katowice"
RECEIVER_EMAIL = ""

csv_manager = data_manager.DataManager(cities_list=["Barcelona"], prices_list=[400])
csv_data = csv_manager.city_file
DEPARTURE_IATA = csv_manager.get_iata(DEPARTURE_CITY)

for destination_iata in csv_data.iata:
    flight_object = flight_search.FlightSearch(departure_iata=DEPARTURE_IATA, arrival_iata=destination_iata)
    flight_found = flight_object.search_direct_flights()
    if flight_found:
        if flight_found.price <= 400:
            message = f"{DEPARTURE_CITY} {flight_found.departure_date} --> {flight_found.arrival_city} " \
                      f"{flight_found.return_date}. Total price {flight_found.price}PLN. " \
                      f"\n\nCheck the details {flight_found.kiwi_link}"
            email_sender = notification_manager.NotificationManager(RECEIVER_EMAIL, message)
            email_sender.send_email()
