# API Endpoints
BASE_URL = "https://drive.google.com/uc?"

# Specific paths for different user-size CSV files
PATH_100USER = "id=1zO8ekHWx9U7mrbx_0Hoxxu6od7uxJqWw&export=download"
PATH_1000USER = "id=1OT84-j5J5z2tHoUvikJtoJFInWmlyYzY&export=download"

# Full download URLs constructed from the base URL and specific paths
URL_100USER = BASE_URL + PATH_100USER
URL_1000USER = BASE_URL + PATH_1000USER

DOWNLOAD_PATH = "temp/"
# Mapping of local CSV file names to their paths
LOCAL_CSV_FILES = {
    'customers-100.csv': 'data_file/customers-100.csv',
    'customers-1000.csv': 'data_file/customers-1000.csv',
}
