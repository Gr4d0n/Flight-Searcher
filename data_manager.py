import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    def __init__(self):
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self.prices_endpoint = os.environ['SHEETY_PRICES_ENDPOINT']
        self.users_endpoint = os.environ['SHEETY_USERS_ENDPOINT']
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self._prices_authentication_header = {
            "Authorization": f"Basic {os.environ["AUTH_TOKEN"]}"
        }
        self._users_authentication_header = {
            "Authorization": f"Basic {os.environ["AUTH_TOKEN"]}"
        }
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=os.environ["SHEETY_PRICES_ENDPOINT"], headers=self._prices_authentication_header)
        data = response.json()
        # print(data)
        self.destination_data = data["prices"]

        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{os.environ["SHEETY_PUT_ENDPOINT"]}/{city['id']}",
                json=new_data,
                headers=self._prices_authentication_header
            )

            # print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, headers=self._users_authentication_header)
        data = response.json()
        print(data)
        self.customer_data = data['users']
        return  self.customer_data


