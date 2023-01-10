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
        self.all_cheapest_flights_list = []

    def update_all_iata_codes(self):
        for row in self.data_manager.sheety_json["prices"]:
            row["iataCode"] = self.flight_search.get_city_iata_code(row["city"])
            print(row)
            self.data_manager.update_row(row_id=row["id"], new_data=row)

    def update_cheapest_flights(self):
        all__low_flights_dict = {f"{row['iataCode']}": self.flight_search.get_flights_by_cities(f"{row['iataCode']}")
                                 for row in self.data_manager.sheety_json["prices"]}

        new_cheapest_flights_list = []

        for row in self.data_manager.sheety_json["prices"]:
            message = ''
            try:
                current_flight_price = all__low_flights_dict[row["iataCode"]]["data"][0]["price"]
            except IndexError:
                message = f"No non-stop flights to {row['city']}-{row['iataCode']} found from anywhere in Chicago..."
            else:
                last_lowest_price = row["lowestPrice"]
                row["lowestPrice"] = current_flight_price
                row_id = row["id"]
                if current_flight_price != last_lowest_price:
                    self.data_manager.update_row(row_id=row_id, new_data=row)
                departure_airport_code = all__low_flights_dict[row["iataCode"]]["data"][0]["route"][0]["flyFrom"]
                arrival_airport_code = all__low_flights_dict[row["iataCode"]]["data"][0]["route"][0]["flyTo"]
                departure_datetime = datetime.datetime.strptime(
                    all__low_flights_dict[row["iataCode"]]["data"][0]["local_departure"],
                    '%Y-%m-%dT%H:%M:%S.%f%z'
                )
                departure_date_formatted = departure_datetime.strftime("%m/%d/%Y")
                departure_time_formatted = departure_datetime.strftime("%-I:%M%p")
                link = all__low_flights_dict[row["iataCode"]]["data"][0]["deep_link"]

                formatted_price_drop = self.format_price_to_usd(last_lowest_price)
                formatted_low_price = self.format_price_to_usd(row['lowestPrice'])

                connecting_flight = None
                try:
                    connecting_flight = all__low_flights_dict[row["iataCode"]]["data"][0]["route"][1]
                except IndexError:
                    pass
                else:
                    connecting_flight_city = connecting_flight["cityFrom"]
                    connecting_flight_code = connecting_flight["flyFrom"]
                    connecting_flight = (f'Flight has one stop in '
                                         f'{connecting_flight_city}-{connecting_flight_code}\n\n')

                message = (
                    f"Low price to {row['city']}-{arrival_airport_code} from Chicago-{departure_airport_code} "
                    f"{f'down from {formatted_price_drop} ' if current_flight_price < last_lowest_price else ''}"
                    f"now at {formatted_low_price}"
                    "\n\n"
                    f"Flight leaves {departure_date_formatted} at {departure_time_formatted}"
                    "\n\n"
                    f"{connecting_flight if connecting_flight else ''}"
                    f"Link to check it out:\n"
                    f"{link}"
                )
            finally:
                # self.notification_manager.send_text_message(message=message)
                new_cheapest_flights_list.append(message)

        self.all_cheapest_flights_list = new_cheapest_flights_list

    def get_sheety_data_as_dict(self):
        sheety_dict = {f"{row['iataCode']}": row for row in self.data_manager.sheety_json["prices"]}
        return sheety_dict

    @staticmethod
    def format_price_to_usd(price):
        return '${:,.2f}'.format(price)

    def email_all_members_deals(self):
        all_members_json = self.data_manager.get_sheety_users()
        email_body = f"\n\n{'_' * 50}\n\n".join(self.all_cheapest_flights_list)

        for row in all_members_json["users"]:
            recipient = row["email"]
            user_first_name = row["firstName"]
            # print(recipient)
            # print(user_first_name)
            # print(email_body)
            subject_str = f"Here's your flight deals, {user_first_name}"
            self.notification_manager.send_email(recipient_email=recipient, subject=subject_str, body=email_body)
