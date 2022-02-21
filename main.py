import data_manager
import flight_search
import notification_manager
import new_user_manager

DEPARTURE_CITY = "Katowice"

print("Welcome! Sign in if you want to join flight club.")
user_name = input("What is your name? ")
user_last_name = input("What is your last name? ")
user_email_1 = input("What is your email? ")
user_email_2 = input("Confirm your email. ")

if user_email_1 == user_email_2:
    user_email = user_email_1

    users_manager = new_user_manager.NewUserManager(user_name, user_last_name, user_email)
    users_manager.add_new_user()

    cities_manager = data_manager.DataManager()
    csv_cities = cities_manager.city_file
    print(csv_cities)
    departure_iata = cities_manager.get_iata(DEPARTURE_CITY)

    for destination_iata in csv_cities.iata:
        print(destination_iata)
        flight_object = flight_search.FlightSearch(departure_iata=departure_iata, arrival_iata=destination_iata)
        flight_found = flight_object.search_direct_flights()
        if flight_found:
            max_flight_price = csv_cities.loc[csv_cities.iata == destination_iata, "max_price"].iloc[0]
            if flight_found.price <= max_flight_price:
                message = f"{DEPARTURE_CITY} {flight_found.departure_airport} --> {flight_found.arrival_city} " \
                          f"{flight_found.arrival_airport} ({flight_found.departure_date} - {flight_found.return_date}). " \
                          f"Total price {flight_found.price} PLN. " \
                          f"\n\nCheck the details {flight_found.kiwi_link}"
                email_sender = notification_manager.NotificationManager(user_email, message)
                email_sender.send_email()

else:
    print("Wrong email.")
