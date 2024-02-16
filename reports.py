import time
import requests
from config import *



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
def check_csv_status_and_download(token, report_id):
    status_url = f'{API_BASE_URL_V2}/reports/cemetery/{CEMETERY_NAME}/status/'
    headers = {'Authorization': f'Bearer {token}'}
    while True:
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            reports = response.json()
            for report in reports:
                if report.get('id') == report_id and report.get('status').lower() == "finished":
                    file_url = report.get('file')
                    print(f"Report {report_id} is finished. Downloading CSV file from: {file_url}")
                    return download_csv_report(file_url, report_id)
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
        return filename
    else:
        print(f"Failed to download CSV. Status Code: {response.status_code}")
        return None

def delete_report(report_id, token):
    """Delete the CSV report from the server."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL_V2}/delete/{report_id}", headers=headers)
    if response.status_code == 204:
        print("Report deleted successfully.")
    else:
        print("Failed to delete report.")