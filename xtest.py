import requests
import csv
import time
import os
import sys

# Constants for API endpoints
LOGIN_URL = 'https://map.chronicle.rip/api/v1/auth/'
GENERATE_CSV_URL = 'https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul/generate/people/'
STATUS_URL = 'https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul/status/'

# Function to get the access token
def get_access_token(username, password):
    login_payload = {"username": username, "password": password}
    response = requests.post(LOGIN_URL, json=login_payload)
    if response.status_code == 200:
        print("Login successful.")
        return response.json()['access']
    else:
        print("Login failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None

# Function to request CSV generation
def request_csv_generation(token):
    generate_headers = {'Authorization': f'Bearer {token}'}
    generate_payload = {
        "attributes": ["plot_id"],
        "document_format": "csv",
        "sections": ["Section A", "Section B"],
        "cemeteries": [],
        "chapters": [
            "roi_holders",
            "roi_applicants",
            "interments",
            "next_of_kins",
            "interment_applicants"
        ]
    }
    response = requests.post(GENERATE_CSV_URL, headers=generate_headers, json=generate_payload)
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
    status_headers = {'Authorization': f'Bearer {token}'}
    while True:
        response = requests.get(STATUS_URL, headers=status_headers)
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
    print(f"Attempting to delete report with ID: {report_id}")
    delete_url = f'https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul/delete/{report_id}/'
    delete_headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json, text/plain, */*'}
    response = requests.delete(delete_url, headers=delete_headers)
    if response.status_code == 204:
        print(f"Report with ID: {report_id} has been successfully deleted.")
    else:
        print(f"Failed to delete report with ID: {report_id}. Status Code: {response.status_code}, Response: {response.content}")

# Main execution function
def main():
    username = os.environ['USER_SUPER_ADMIN']
    password = os.environ['PASS_SUPER_ADMIN']
    local_csv_file = 'astana_tegal_gundul_people-template.csv'

    token = get_access_token(username, password)
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
        validations = {(2, 0): 'A D 2', (3, 0): 'A D 6'}  # Replace with actual validations
        if compare_csv(downloaded_csv, local_csv_file, validations):
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