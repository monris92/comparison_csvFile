import time

import requests
from config import *

# Contoh URL endpoint APIs
# API_BASE_URL = "https://map.chronicle.rip/api/v2/reports/cemetery/Astana_Tegal_Gundul"


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
def check_csv_status_and_download(token):
    status_url = f"{API_BASE_URL_V2}/reports/cemetery/{CEMETERY_NAME}/status/"
    headers = {'Authorization': f'Bearer {token}'}

    while True:
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            reports = response.json()
            for report in reports:
                if report.get('status').lower() == "finished":
                    download_url = report.get('file')  # Ini adalah URL langsung ke file CSV yang ingin diunduh
                    file_name = report.get('file_name')  # Ini adalah nama file yang dihasilkan
                    print(f"Report {report['id']} is finished. Downloading CSV file: {file_name}")
                    return download_csv_report(download_url, file_name)
            print("Waiting for report to finish...")
            time.sleep(30)  # Wait before checking again
        else:
            print(f"Failed to check report status. Status Code: {response.status_code}")
            return None

def download_csv_report(download_url, file_name):
    csv_response = requests.get(download_url)
    if csv_response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(csv_response.content)
        print(f"CSV report downloaded successfully as {file_name}.")
        return file_name
    else:
        print(f"Failed to download report. Status Code: {csv_response.status_code}")
        return None

def delete_report(report_id, token):
    """Delete the CSV report from the server."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL_V2}/delete/{report_id}", headers=headers)
    if response.status_code == 204:
        print("Report deleted successfully.")
    else:
        print("Failed to delete report.")