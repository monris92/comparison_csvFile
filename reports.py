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

def check_csv_status_and_download(report_id, token):
    """Check the status of the CSV report and download it when ready."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL_V2}/{report_id}/status", headers=headers)
    if response.status_code == 200:
        status = response.json().get('status')
        if status == 'completed':
            download_url = response.json().get('download_url')
            csv_response = requests.get(download_url)
            if csv_response.status_code == 200:
                with open('report.csv', 'wb') as f:
                    f.write(csv_response.content)
                print("CSV report downloaded successfully.")
                return 'report.csv'
    print("CSV report is not ready or failed to download.")
    return None

def delete_report(report_id, token):
    """Delete the CSV report from the server."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL_V2}/delete/{report_id}", headers=headers)
    if response.status_code == 204:
        print("Report deleted successfully.")
    else:
        print("Failed to delete report.")