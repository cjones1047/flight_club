import requests
import os
import dotenv


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        dotenv.load_dotenv()
        self.sheety_flight_deals_endpoint = os.getenv("SHEETY_FLIGHT_DEALS_ENDPOINT")
        self.sheety_flight_deals_token = os.getenv("SHEETY_FLIGHT_DEALS_TOKEN")
        self.sheety_headers = {
            "Authorization": f"Bearer {self.sheety_flight_deals_token}"
        }
        sheety_json = requests.get(url=self.sheety_flight_deals_endpoint, headers=self.sheety_headers).json()
        print(sheety_json)
