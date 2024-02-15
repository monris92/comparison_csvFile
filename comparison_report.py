import requests
import csv
import time
import os

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
        return response.json()  # The response must include a report ID or similar
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

# Main function
def main():
    username = os.environ('USERNAME')
    password = os.environ('PASSWORD')
    local_csv_file = 'astana_tegal_gundul_people-template.csv'

    token = get_access_token(username, password)
    if not token:
        return  # Exit if login failed

    # Request to generate a CSV, check if the response includes an ID
    report_info = request_csv_generation(token)
    if not report_info:
        return  # Exit if report generation failed

    # Check the status of the CSV generation and download when ready
    csv_file_url = check_csv_status_and_download(token)
    if not csv_file_url:
        return  # Exit if checking status or downloading failed

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

        # Perform validations and compare downloaded_csv with your local CSV
        validation_passed = compare_csv(downloaded_csv, local_csv_file, validations)
        if validation_passed:
            print("CSV validation successful.")
        else:
            print("CSV validation failed.")
    else:
        print(f"Failed to download CSV. Status Code: {response.status_code}")

if __name__ == "__main__":
    main()
