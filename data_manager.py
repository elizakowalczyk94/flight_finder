import os
import requests
from dotenv import load_dotenv

load_dotenv()
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
TOKEN = os.getenv("TOKEN")


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.bearer_headers = {"Authorization": TOKEN}

    def read_sheety(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=self.bearer_headers)
        response_json = response.json()
        return response_json

    def write_sheety(self, json_data):
        response = requests.post(url=SHEETY_ENDPOINT, json=json_data, headers=self.bearer_headers)
        return response
