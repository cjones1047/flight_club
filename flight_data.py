from data_manager import DataManager
from flight_search import FlightSearch


class FlightData:

    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.data_manager = DataManager()
        self.flight_search = FlightSearch()

    def update_all_iata_codes(self):
        for row in self.data_manager.sheety_json["prices"]:
            row["iataCode"] = self.flight_search.get_city_iata_code(row["city"])
            print(row)
            self.data_manager.update_row(row_id=row["id"], new_data=row)

    def get_all_cheapest_flights(self):
        all_flights = [self.flight_search.get_flights_by_cities(f"{row['iataCode']}")
                       for row in self.data_manager.sheety_json["prices"]]
        print(all_flights)
