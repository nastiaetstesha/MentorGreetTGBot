import json
import os
import requests


# API_BASE_URL = "https://my-json-server.typicode.com/devmanorg/congrats-mentor"
# https://my-json-server.typicode.com/devmanorg/congrats-mentor/mentors
API_BASE_URL = "http://127.0.0.1:8080"


def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            return data
    return []


print(fetch_data("mentors"))
print(fetch_data("postcards"))