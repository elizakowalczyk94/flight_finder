class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, price, departure_city, departure_airport, arrival_city,
                 arrival_airport, departure_date, arrival_date):
        self.price = price
        self.departure_city = departure_city
        self.departure_airport = departure_airport
        self.arrival_city = arrival_city
        self.arrival_airport = arrival_airport
        self.departure_date = departure_date
        self.arrival_date = arrival_date
