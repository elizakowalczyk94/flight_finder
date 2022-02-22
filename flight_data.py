class FlightData:

    def __init__(self, price, departure_city, departure_airport, arrival_city,
                 arrival_airport, departure_date, airline, kiwi_link, return_date,
                 stop_overs=0, via_city=""):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.arrival_city = arrival_city
        self.arrival_airport = arrival_airport
        self.departure_date = departure_date
        self.return_date = return_date
        self.airline = airline
        self.kiwi_link = kiwi_link
        self.stop_overs = stop_overs
        self.via_city = via_city
