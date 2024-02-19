# main.py
import csv
import sys
import requests

from utilities import get_access_token, request_csv_generation, check_csv_status_and_download, compare_csv, delete_report
from config import USERNAME, PASSWORD, LOCAL_CSV_FILE

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

    response = requests.get(csv_file_url)
    if response.status_code == 200:
        decoded_content = response.content.decode('utf-8')
        downloaded_csv = list(csv.reader(decoded_content.splitlines()))
        validations = {(2, 0): 'A D 2',
                       (3, 0): 'A D 6'}  # Replace with actual validations
        if compare_csv(downloaded_csv, LOCAL_CSV_FILE, validations):
            print("CSV validation successful.")
            delete_report(token, report_id)
        else:
            print("CSV validation failed.")
            sys.exit(1)
    else:
        print(f"Failed to download CSV. Status Code: {response.status_code}")
        sys.exit(1)

if __name__ == "__main__":
    main()