import sys
import time

from config import *
from file_utils import *


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


# Function to delete a report
def delete_report(token, report_id):
    delete_url = get_api_url(API_VERSION_V1, 'reports/cemetery', CEMETERY_NAME) + f'delete/{report_id}/'
    print(f"Attempting to delete report with ID: {report_id}")
    delete_headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json, text/plain, */*'}
    response = requests.delete(delete_url, headers=delete_headers)
    if response.status_code == 204:
        print(f"Report with ID: {report_id} has been successfully deleted.")
    else:
        print(
            f"Failed to delete report with ID: {report_id}. Status Code: {response.status_code}, Response: {response.content}")


def get_api_url(version, endpoint, cemetery_name=None):
    if cemetery_name:
        return f'{BASE_URL}/{version}/{endpoint}/{cemetery_name}/'
    return f'{BASE_URL}/{version}/{endpoint}/'


def process_report(token, report_type, payload, report_type_suffix):
    report_id = request_report(token, report_type_suffix, CEMETERY_NAME, payload)
    if report_id:
        csv_url = check_csv_status_and_download(token, report_id)
        if csv_url:
            csv_path = os.path.join(DOWNLOAD_PATH, f'{report_type}_report.csv')
            if download_csv(csv_url, csv_path):
                if compare_with_local_template(csv_path, report_type,
                                               LOCAL_CSV_FILES):  # Add the LOCAL_CSV_FILES argument
                    print(f"{report_type.capitalize()} CSV validation successful.")
                else:
                    print(f"{report_type.capitalize()} CSV validation failed. Data comparison did not match.")
                    sys.exit(1)
            else:
                print(f"Failed to download {report_type} report CSV.")
                sys.exit(1)
            delete_report(token, report_id)
        else:
            print(f"Failed to download or validate {report_type} report CSV for report ID: {report_id}.")
            sys.exit(1)
    else:
        print(f"Failed to request {report_type} report.")
        sys.exit(1)
