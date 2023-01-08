import requests
import os
import dotenv
import datetime
from dateutil.relativedelta import relativedelta


class FlightSearch:

    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        dotenv.load_dotenv()
        self.tequila_api_key = os.getenv("TEQUILA_API_KEY")
        self.tequila_headers = {
            "accept": "application/json",
            "apikey": f"{self.tequila_api_key}"
        }

    def get_city_iata_code(self, city_name):
        get_city_endpoint = "https://api.tequila.kiwi.com/locations/query?" \
                            f"term={city_name}&locale=en-US&location_types=city&limit=10&active_only=true"
        get_city_json = requests.get(url=get_city_endpoint, headers=self.tequila_headers).json()
        city_code = get_city_json["locations"][0]["code"]
        return city_code

    def get_flights_by_cities(self, city_code):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        six_months_away = tomorrow + relativedelta(months=6)
        tomorrow = self.format_date(tomorrow)
        six_months_away = self.format_date(six_months_away)
        search_endpoint = "https://api.tequila.kiwi.com/v2/search"
        search_params = {
            "fly_from": "CHI",
            "fly_to": f"{city_code}",
            "date_from": f"{tomorrow}",
            "date_to": f"{six_months_away}",
            "one_for_city": "1",
            "curr": "USD",
            "max_stopovers": "0"
        }
        all_flights_response = requests.get(url=search_endpoint, params=search_params, headers=self.tequila_headers)
        all_flights_response.raise_for_status()
        print(all_flights_response.text)
        all_flights_json = all_flights_response.json()
        return all_flights_json

    @staticmethod
    def format_date(this_date):
        return this_date.strftime("%m/%d/%Y")
