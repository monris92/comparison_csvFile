import requests
import csv
import time
from config import *

def get_api_url(version, endpoint, cemetery_name=None):
    if cemetery_name:
        return f'{BASE_URL}/{version}/{endpoint}/{cemetery_name}/'
    return f'{BASE_URL}/{version}/{endpoint}/'

def get_access_token(username, password):
    login_url = get_api_url(API_VERSION_V1, 'auth')
    login_payload = {"username": username, "password": password}
    response = requests.post(login_url, json=login_payload)
    if response.status_code == 200:
        print("Login successful.")
        return response.json()['access']
    else:
        print("Login failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None

# Function to request CSV generation
def request_csv_generation(token):
    generate_url = get_api_url(API_VERSION_V2, 'reports/cemetery', CEMETERY_NAME) + 'generate/people/'
    generate_headers = {'Authorization': f'Bearer {token}'}
    generate_payload = {
        "attributes": REPORT_ATTRS,
        "document_format": "csv",
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "chapters": REPORT_CHAPTERS
    }
    response = requests.post(generate_url, headers=generate_headers, json=generate_payload)
    if response.status_code == 200:
        print("CSV generation request successful.")
        report_ws = response.json()['ws']
        report_id = report_ws.split('/')[-2]
        return report_id
    else:
        print("CSV generation request failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None

# Function to check the status of the CSV generation
def check_csv_status_and_download(token):
    status_url = get_api_url(API_VERSION_V2, 'reports/cemetery', CEMETERY_NAME) + 'status/'
    status_headers = {'Authorization': f'Bearer {token}'}
    while True:
        response = requests.get(status_url, headers=status_headers)
        if response.status_code == 200:
            reports = response.json()
            for report in reports:
                if report['status'].lower() == "finished":
                    print(f"Report {report['id']} is finished. Downloading CSV file.")
                    return report['file']
            print("Waiting for report to finish...")
            time.sleep(30)  # Wait before checking again
        else:
            print(f"Failed to check report status. Status Code: {response.status_code}")
            return None

# Function to compare two CSV files based on specific validations
def compare_csv(downloaded_csv, local_csv_file, validations):
    with open(local_csv_file, newline='', encoding='utf-8') as file:
        local_csv_reader = csv.reader(file)
        local_csv = list(local_csv_reader)

    for (row_index, col_index), expected_value in validations.items():
        if local_csv[row_index][col_index] != expected_value:
            print(f"Validation failed at row {row_index + 1}, column {col_index + 1}. "
                  f"Expected: {expected_value}, Found: {local_csv[row_index][col_index]}")
            return False
    print("All validations passed.")
    return True

# Function to delete a report
def delete_report(token, report_id):
    delete_url = get_api_url(API_VERSION_V1, 'reports/cemetery', CEMETERY_NAME) + f'delete/{report_id}/'
    print(f"Attempting to delete report with ID: {report_id}")
    delete_headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json, text/plain, */*'}
    response = requests.delete(delete_url, headers=delete_headers)
    if response.status_code == 204:
        print(f"Report with ID: {report_id} has been successfully deleted.")
    else:
        print(f"Failed to delete report with ID: {report_id}. Status Code: {response.status_code}, Response: {response.content}")
