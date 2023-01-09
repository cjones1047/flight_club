import requests
import os
import dotenv


class DataManager:

    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        dotenv.load_dotenv()
        self.sheety_flight_deals_endpoint = os.getenv("SHEETY_FLIGHT_DEALS_ENDPOINT")
        self.sheety_users_endpoint = os.getenv("SHEETY_USERS_ENDPOINT")
        self.sheety_flight_deals_token = os.getenv("SHEETY_FLIGHT_DEALS_TOKEN")
        self.sheety_headers = {
            "Authorization": f"Bearer {self.sheety_flight_deals_token}"
        }
        self.sheety_json = self.get_sheety_data()

    def get_sheety_data(self):
        new_sheety_response = requests.get(url=self.sheety_flight_deals_endpoint, headers=self.sheety_headers)
        new_sheety_response.raise_for_status()
        print(new_sheety_response.text)
        new_sheety_json = new_sheety_response.json()
        return new_sheety_json

    def get_sheety_users(self):
        all_users_response = requests.get(url=self.sheety_users_endpoint, headers=self.sheety_headers)
        all_users_response.raise_for_status()
        print(all_users_response.text)
        all_users_json = all_users_response.json()
        return all_users_json

    def update_row(self, row_id, new_data):
        sheety_put_endpoint = f"{self.sheety_flight_deals_endpoint}/{row_id}"
        put_json = {
            "price": new_data
        }
        put_response = requests.put(url=sheety_put_endpoint, headers=self.sheety_headers, json=put_json)
        put_response.raise_for_status()
        print(f"Put request to row {row_id}: {put_response}")
