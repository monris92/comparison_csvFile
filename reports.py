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

def check_csv_status_and_download(token):
    status_url = f"{API_BASE_URL_V2}/reports/cemetery/{CEMETERY_NAME}/status/"
    headers = {'Authorization': f'Bearer {token}'}
    while True:
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            reports = response.json()
            for report in reports:
                if report.get('status').lower() == "finished":
                    report_id = report.get('id')  # Asumsikan bahwa ini adalah ID yang dibutuhkan
                    download_url = report.get('file')
                    print(f"Report {report_id} is finished. Downloading CSV file.")
                    csv_response = requests.get(download_url)
                    if csv_response.status_code == 200:
                        with open(f'report_{report_id}.csv', 'wb') as f:
                            f.write(csv_response.content)
                        print(f"CSV report {report_id} downloaded successfully.")
                        return f'report_{report_id}.csv'
            print("Waiting for report to finish...")
            time.sleep(30)  # Wait before checking again
        else:
            print(f"Failed to check report status. Status Code: {response.status_code}")
            return None

def delete_report(report_id, token):
    """Delete the CSV report from the server."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL_V2}/delete/{report_id}", headers=headers)
    if response.status_code == 204:
        print("Report deleted successfully.")
    else:
        print("Failed to delete report.")