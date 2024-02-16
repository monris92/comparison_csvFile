import sys
import requests
from config import username, password, local_csv_file
from auth import get_access_token
from reports import request_csv_generation, check_csv_status_and_download, delete_report
from validators import compare_csv

# Fungsi utama
def main():
    token = get_access_token(username, password)
    if not token:
        sys.exit(1)  # Exit if login failed

    # Request to generate a CSV, check if the response includes an ID
    report_id = request_csv_generation(token)
    if not report_id:
        sys.exit(1)  # Exit if report generation failed

    # Check the status of the CSV generation and download when ready
    csv_file_url = check_csv_status_and_download(token)
    if not csv_file_url:
        sys.exit(1)  # Exit if checking status or downloading failed

    # Download the CSV file
    response = requests.get(csv_file_url)
    if response.status_code == 200:
        decoded_content = response.content.decode('utf-8')
        downloaded_csv = list(csv.reader(decoded_content.splitlines()))

        # Define your validations (row_index and col_index should be zero-based)
        validations = {
            # Assume the keys are (row, column) indices for the expected values
            (2, 0): 'A D 2',  # Adjust row_index if your CSV has headers
            (3, 0): 'A D 6',
            # Add more validations as needed
        }

        # Lakukan validasi dan bandingkan downloaded_csv dengan local_csv Anda
        if not compare_csv(downloaded_csv, local_csv_file, validations):
            print("CSV validation failed.")
            sys.exit(1)  # Keluar dengan status 1 jika validasi gagal
        else:
            print("CSV validation successful.")
            # Hapus laporan disini
            delete_report(token, report_id)
    else:
        print(f"Failed to download CSV. Status Code: {response.status_code}")
        sys.exit(1)  # Keluar dengan status 1 jika pengunduhan CSV gagal


if __name__ == "__main__":
    main()