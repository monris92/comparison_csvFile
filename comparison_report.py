import requests
import csv
import time
import os
import sys

# Function to get the access token
def get_access_token(username, password):
    login_url = 'https://map.chronicle.rip/api/v1/auth/'
    login_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, json=login_payload)
    if response.status_code == 200:
        print("Login successful.")
        return response.json()['access']
    else:
        print("Login failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None

# Function to request CSV generation
def request_csv_generation(token, null=None):
    # Replace this URL and payload with the correct endpoint and payload for your application
    generate_url = 'https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul/generate/people/'
    generate_headers = {
        'Authorization': f'Bearer {token}'
    }
    generate_payload = {
        
            "attributes": [
                "plot_id"
            ],
            "document_format": "csv",
            "sections": [
                "Section A",
                "Section B"
            ],
            "cemeteries": [],
            "chapters": [
                "roi_holders",
                "roi_applicants",
                "interments",
                "next_of_kins",
                "interment_applicants"
            ],
            "first_name": null,
            "last_name": null
        
    }  # Your payload here
    response = requests.post(generate_url, headers=generate_headers, json=generate_payload)
    if response.status_code == 200:
        print("CSV generation request successful.")
        response_data = response.json()
        report_ws = response_data['ws']
        report_id = report_ws.split('/')[-2]  # Mengambil angka dari akhir string '/ws/report_cemetery/Astana_Tegal_Gundul/5186/'
        return report_id
    else:
        print("CSV generation request failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None

# Function to check the status of the CSV generation
def check_csv_status_and_download(token):
    status_url = 'https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul/status/'
    status_headers = {
        'Authorization': f'Bearer {token}'
    }
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

# Function to compare two CSV files
# Function to compare two CSV files based on specific validations
def compare_csv(downloaded_csv, local_csv_file, validations):
    # Open the local CSV file and read it into memory
    with open(local_csv_file, newline='', encoding='utf-8') as file:
        local_csv_reader = csv.reader(file)
        local_csv = list(local_csv_reader)

    # Perform validations
    for (row_index, col_index), expected_value in validations.items():
        # Adjust indices if your CSV has headers
        if local_csv[row_index][col_index] != expected_value:
            print(f"Validation failed at row {row_index + 1}, column {col_index + 1}. "
                  f"Expected: {expected_value}, Found: {local_csv[row_index][col_index]}")
            return False
    print("All validations passed.")
    return True

# Fungsi untuk menghapus laporan
def delete_report(token, report_id):
    delete_url = f'https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul/delete/{report_id}/'
    delete_headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json, text/plain, */*',
        # ... (header lainnya jika perlu)
    }
    response = requests.delete(delete_url, headers=delete_headers)
    if response.status_code == 204:
        print(f"Report {report_id} successfully deleted.")
    else:
        print(f"Failed to delete report {report_id}. Status Code: {response.status_code}, Response: {response.content}")


# Main function
def main():
    username = os.environ['USER_SUPER_ADMIN']
    password = os.environ['PASS_SUPER_ADMIN']
    local_csv_file = 'astana_tegal_gundul_people-template.csv'

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
