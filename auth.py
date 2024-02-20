import requests

from config import BASE_URL, API_VERSION_V1


def get_api_url(endpoint):
    return f'{BASE_URL}/{API_VERSION_V1}/{endpoint}/'


def get_access_token(username, password):
    login_url = get_api_url('auth')
    login_payload = {"username": username, "password": password}
    response = requests.post(login_url, json=login_payload)
    if response.status_code == 200:
        print("Login successful.")
        return response.json().get('access')
    else:
        print("Login failed.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")
        return None
