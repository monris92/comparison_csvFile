import csv
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
    downloaded_csv_file = check_csv_status_and_download(token, report_id)
    if not downloaded_csv_file:
        sys.exit(1)  # Exit if checking status or downloading failed

    # Open downloaded CSV file and read into memory
    with open(downloaded_csv_file, newline='', encoding='utf-8') as file:
        downloaded_csv = list(csv.reader(file))

    # Define your validations (row_index and col_index should be zero-based)
    validations = {
        # Assume the keys are (row, column) indices for the expected values
        (2, 0): 'A D 2',  # Adjust row_index if your CSV has headers
        (3, 0): 'A D 6',
        # Add more validations as needed
    }

    # Perform validation and compare downloaded_csv with your local_csv
    if not compare_csv(downloaded_csv, local_csv_file, validations):
        print("CSV validation failed.")
        sys.exit(1)  # Exit with status 1 if validation fails
    else:
        print("CSV validation successful.")
        # Delete the report here
        delete_report(token, report_id)

if __name__ == "__main__":
    main()