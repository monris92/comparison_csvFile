# main.py
import sys
# import requests
from utilities import *
from config import *


def download_csv(csv_file_url, download_path):
    response = requests.get(csv_file_url)
    if response.status_code == 200:
        with open(download_path, 'w', newline='', encoding='utf-8') as file:
            file.write(response.content.decode('utf-8'))
        return True
    print(f"Failed to download CSV. Status Code: {response.status_code}")
    return False

def main():
    token = get_access_token(USERNAME, PASSWORD)
    if not token:
        sys.exit(1)

    report_id = request_csv_generation(token)
    if not report_id:
        sys.exit(1)

    csv_file_url = check_csv_status_and_download(token)
    if not csv_file_url:
        sys.exit(1)

    # Menyimpan CSV yang di-download ke path lokal
    if download_csv(csv_file_url, DOWNLOAD_PATH):
        if compare_csv(DOWNLOAD_PATH, LOCAL_CSV_FILE):
            print("CSV validation successful.")
            delete_report(token, report_id)
        else:
            print("CSV validation failed.")
            sys.exit(1)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()