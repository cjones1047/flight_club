import requests
import os
import dotenv


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
