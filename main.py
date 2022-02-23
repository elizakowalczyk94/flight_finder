import data_manager
import flight_search
import notification_manager

DEPARTURE_CITY = "Warsaw"

print("Welcome! Sign in if you want to join flight club.")

# users_manager = new_user_manager.NewUserManager(user_name, user_last_name, user_email)
# users_manager.add_new_user()

cities_manager = data_manager.DataManager()
csv_cities = cities_manager.city_file
departure_iata = cities_manager.get_iata(DEPARTURE_CITY)

flight_object = flight_search.FlightSearch()

for destination_iata in csv_cities.iata:
    flight_found = flight_object.search_direct_flights(departure_iata, destination_iata)
    max_flight_price = csv_cities.loc[csv_cities.iata == destination_iata, "max_price"].iloc[0]

    if flight_found is None:
        print(f"No flight found for {destination_iata}")
        continue

    if flight_found.price <= max_flight_price:
        message = f"{DEPARTURE_CITY} {flight_found.departure_airport} --> {flight_found.arrival_city} " \
                  f"{flight_found.arrival_airport} ({flight_found.departure_date} - {flight_found.return_date}). " \
                  f"Total price {flight_found.price} PLN" \
                  f"\n\nCheck the details {flight_found.kiwi_link}"
        if flight_found.stop_overs > 0:
            message = f"{DEPARTURE_CITY} {flight_found.departure_airport} --> {flight_found.arrival_city} " \
                      f"{flight_found.arrival_airport} ({flight_found.departure_date} - {flight_found.return_date}). " \
                      f"Total price {flight_found.price} PLN. " \
                      f"\n\nThe flight has 1 stop over via {flight_found.via_city}" \
                      f"\n\nCheck the details {flight_found.kiwi_link}"
        print(message)
        email_sender = notification_manager.NotificationManager()
        email_sender.send_email_to_all_users(message.encode('ascii', 'ignore').decode('ascii'))
