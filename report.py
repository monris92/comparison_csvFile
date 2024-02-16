import requests

# Contoh URL endpoint API
API_BASE_URL = "https://api.example.com/v1/reports"

def request_csv_generation(token):
    """Request the generation of a CSV report."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/generate", headers=headers)
    if response.status_code == 201:
        report_id = response.json().get('id')
        return report_id
    else:
        print("Failed to request CSV generation.")
        return None

def check_csv_status_and_download(report_id, token):
    """Check the status of the CSV report and download it when ready."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/{report_id}/status", headers=headers)
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
    response = requests.delete(f"{API_BASE_URL}/{report_id}", headers=headers)
    if response.status_code == 204:
        print("Report deleted successfully.")
    else:
        print("Failed to delete report.")