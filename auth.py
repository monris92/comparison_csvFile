import requests

def get_access_token(username, password):
    """
    Function to authenticate users and retrieve an access token from the API.
    :param username: The username for authentication.
    :param password: The password for authentication.
    :return: The access token if successful, or None otherwise.
    """
    login_url = 'https://map.chronicle.rip/api/v1/auth/'
    login_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, json=login_payload)
    if response.status_code == 200:
        print("Login successful.")
        return response.json().get('access')
    else:
        print("Login failed.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")
        return None