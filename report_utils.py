import os
import requests
from config import DOWNLOAD_PATH

def download_csv_from_url(download_url, downloaded_csv_path):
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(downloaded_csv_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
            print(f"File downloaded successfully from {download_url} to {downloaded_csv_path}.")
            return True
        else:
            print(f"Failed to download file from {download_url}. Error code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while downloading {download_url}: {e}")
        return False

def process_csv_files(files_to_process, file_utils):
    for local_file_name, download_url in files_to_process.items():
        downloaded_csv_path = os.path.join(DOWNLOAD_PATH, local_file_name)
        local_csv_path = file_utils.LOCAL_CSV_FILES.get(local_file_name)

        if not local_csv_path:
            print(f"No local CSV file defined for {local_file_name}.")
            continue

        if download_csv_from_url(download_url, downloaded_csv_path):
            if file_utils.compare_with_local_template(downloaded_csv_path, local_file_name, file_utils.LOCAL_CSV_FILES):
                print(f"Validation successful for {local_file_name}.")
            else:
                print(f"Validation failed for {local_file_name}.")
        else:
            print(f"Failed to download {local_file_name}.")