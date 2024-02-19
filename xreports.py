import time
import requests
from config import *


import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def request_csv_generation(token):
    """Request the generation of a CSV report."""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "attributes": REPORT_ATTRS,
        "document_format": "csv",
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "chapters": REPORT_CHAPTERS,
        "first_name": None,
        "last_name": None
    }
    response = requests.post(REPORT_GENERATE_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        print("CSV generation request successful.")
        response_data = response.json()
        report_ws = response_data['ws']
        report_id = report_ws.split('/')[-2]
        return report_id
    else:
        print("CSV generation request failed.")
        print(f"Status Code: {response.status_code}, Response: {response.content}")
        return None


# Check the status of the CSV generation and download when ready
def check_csv_status_and_download(token, report_id, max_retries=10, retry_delay=30):
    status_url = f'{API_BASE_URL_V2}/reports/cemetery/{CEMETERY_NAME}/status/'
    headers = {'Authorization': f'Bearer {token}'}
    while True:
        response = requests.get(status_url, headers=headers)
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
def download_csv_report(file_url, report_id):
    response = requests.get(file_url)
    if response.status_code == 200:
        filename = f'report_{report_id}.csv'
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"CSV report downloaded successfully as {filename}.")
        logging.info(f"download_csv_report: {file_url}")
        return filename
    else:
        print(f"Failed to download CSV. Status Code: {response.status_code}")
        logging.info(f"CSV file would be downloaded from: {file_url}")
        return None

def delete_report(report_id, token):
    """Delete the CSV report from the server."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL_V2}/delete/{report_id}", headers=headers)
    if response.status_code == 204:
        print("Report deleted successfully.")
    else:
        print("Failed to delete report.")