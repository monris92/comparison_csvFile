from config import BASE_URL

def get_api_url(version, endpoint, cemetery_name=None):
    if cemetery_name:
        return f'{BASE_URL}/{version}/{endpoint}/{cemetery_name}/'
    return f'{BASE_URL}/{version}/{endpoint}/'