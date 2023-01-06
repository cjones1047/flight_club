from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime


class FlightData:

    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.data_manager = DataManager()
        self.flight_search = FlightSearch()
        self.notification_manager = NotificationManager()

    def update_all_iata_codes(self):
        for row in self.data_manager.sheety_json["prices"]:
            row["iataCode"] = self.flight_search.get_city_iata_code(row["city"])
            print(row)
            self.data_manager.update_row(row_id=row["id"], new_data=row)

    def update_cheapest_flights(self):
        all_flights = {f"{row['iataCode']}": self.flight_search.get_flights_by_cities(f"{row['iataCode']}")
                       for row in self.data_manager.sheety_json["prices"]}

        for row in self.data_manager.sheety_json["prices"]:
            current_flight_price = all_flights[row["iataCode"]]["data"][0]["price"]
            last_lowest_price = row["lowestPrice"]
            row["lowestPrice"] = current_flight_price
            row_id = row["id"]
            if current_flight_price != last_lowest_price:
                self.data_manager.update_row(row_id=row_id, new_data=row)
            if current_flight_price < last_lowest_price:
                departure_airport_code = all_flights[row["iataCode"]]["data"][0]["route"][0]["flyFrom"]
                arrival_airport_code = all_flights[row["iataCode"]]["data"][0]["route"][0]["flyTo"]
                departure_datetime = datetime.datetime.strptime(
                    all_flights[row["iataCode"]]["data"][0]["local_departure"],
                    '%Y-%m-%dT%H:%M:%S.%f%z'
                )
                departure_date_formatted = departure_datetime.strftime("%m/%d/%Y")
                departure_time_formatted = departure_datetime.strftime("%-I:%M%p")
                link = all_flights[row["iataCode"]]["data"][0]["deep_link"]

                message = (
                    f"New low price to {row['city']}-{arrival_airport_code} from Chicago-{departure_airport_code} "
                    f"down from {'${:,.2f}'.format(last_lowest_price)} "
                    f"to {'${:,.2f}'.format(row['lowestPrice'])}"
                    "\n\n"
                    f"Flight leaves {departure_date_formatted} at {departure_time_formatted}"
                    "\n\n"
                    f"Link to check it out:\n"
                    f"{link}"
                )
                self.notification_manager.send_text_message(message=message)

    def get_sheety_data_as_dict(self):
        sheety_dict = {f"{row['iataCode']}": row for row in self.data_manager.sheety_json["prices"]}
        return sheety_dict
