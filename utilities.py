from api_helper import *
from config import *
import requests
import time
import csv



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

def request_report(token, report_type_suffix, cemetery_name, payload):
    generate_url = get_api_url(API_VERSION_V2, 'reports/cemetery', cemetery_name) + f'generate/{report_type_suffix}'
    generate_headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(generate_url, headers=generate_headers, json=payload)
    if response.status_code == 200:
        print(f"Report generation request for {report_type_suffix} successful.")
        report_ws = response.json()['ws']
        report_id = report_ws.split('/')[-2]
        return report_id
    else:
        print(f"Report generation request for {generate_url} {report_type_suffix} failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None

def check_csv_status_and_download(token, report_id):
    status_url = get_api_url(API_VERSION_V2, 'reports/cemetery', CEMETERY_NAME) + f'status/{report_id}/'
    status_headers = {'Authorization': f'Bearer {token}'}
    while True:
        response = requests.get(status_url, headers=status_headers)
        if response.status_code == 200:
            report_status = response.json()['status'].lower()
            if report_status == "finished":
                print(f"Report {report_id} is finished. Downloading CSV file.")
                download_url = response.json()['file']
                return download_url
            elif report_status == "error":
                print(f"Report {report_id} has encountered an error.")
                return None
            print("Waiting for report to finish...")
            time.sleep(30)  # Wait before checking again
        else:
            print(f"Failed to check report status. Status Code: {response.status_code}")
            return None

def download_csv(download_url, local_file_path):
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV downloaded successfully to {local_file_path}.")
        return True
    else:
        print("Failed to download CSV.")
        return False

# Function to compare two CSV files
def compare_csv(downloaded_csv_path, local_csv_file):
    with open(downloaded_csv_path, newline='', encoding='utf-8') as downloaded_file:
        downloaded_csv_reader = csv.reader(downloaded_file)
        downloaded_csv = list(downloaded_csv_reader)

    with open(local_csv_file, newline='', encoding='utf-8') as local_file:
        local_csv_reader = csv.reader(local_file)
        local_csv = list(local_csv_reader)

    if len(downloaded_csv) != len(local_csv):
        print("Validation failed: Number of rows does not match.")
        return False

    for row_index, (downloaded_row, local_row) in enumerate(zip(downloaded_csv, local_csv)):
        if downloaded_row != local_row:
            print(f"Validation failed at row {row_index + 1}:")
            print(f"Downloaded: {downloaded_row}")
            print(f"Local: {local_row}")
            return False

    print("All validations passed.")
    return True

def compare_with_local_template(downloaded_csv_path, report_type_suffix):
    local_csv_file = LOCAL_CSV_FILES.get(report_type_suffix)
    if not local_csv_file:
        print(f"No local CSV template found for report type '{report_type_suffix}'.")
        return False

    return compare_csv(downloaded_csv_path, local_csv_file)

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
