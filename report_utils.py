import os
import requests

from file_utils import compare_with_local_template
from config import *


def download_csv_from_url(download_url, local_file_path):
    """
    Downloads a CSV file from the specified URL and saves it to the local file path.

    Args:
        download_url (str): The URL from which to download the CSV file.
        local_file_path (str): The local file path where the CSV will be saved.

    Returns:
        bool: True if the download was successful, False otherwise.
    """
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
        print(f"File downloaded successfully from {download_url} to {local_file_path}.")
        return True
    else:
        print(f"Failed to download file from {download_url}. Status Code: {response.status_code}")
        return False

def process_csv_files(files_to_process):
    """
    Downloads CSV files from the specified URLs and compares each to the local template.

    Args:
        files_to_process (dict): A dictionary mapping local file names to download URLs.
    """
    for local_file_name, download_url in files_to_process.items():
        downloaded_csv_path = os.path.join(DOWNLOAD_PATH, local_file_name)

        # Download the CSV from the URL
        print(f"Downloading {local_file_name} from {download_url}...")
        if download_csv_from_url(download_url, downloaded_csv_path):
            # Compare the downloaded CSV with the local template
            print(f"Comparing downloaded {local_file_name} with local template...")
            if compare_with_local_template(downloaded_csv_path, local_file_name):
                print(f"Validation successful for {local_file_name}.")
            else:
                print(f"Validation failed for {local_file_name}. Data comparison did not match.")
        else:
            print(f"Failed to download {local_file_name}.")

# Define the function to process the CSV files
# def process_csv_files(files_to_process):
#     """
#     Downloads CSV files from the specified URLs and compares each to a local template.
#
#     Args:
#         files_to_process (dict): A dictionary mapping local file names to download URLs.
#     """
#     for local_file_name, download_url in files_to_process.items():
#         downloaded_csv_path = os.path.join(DOWNLOAD_PATH, local_file_name)
#         local_csv_path = LOCAL_CSV_FILES.get(local_file_name)
#
#         if not local_csv_path:
#             print(f"No local CSV file defined for {local_file_name} in LOCAL_CSV_FILES.")
#             continue
#
#         # Download the CSV from the URL
#         print(f"Downloading {local_file_name} from {download_url}...")
#         if download_csv_from_url(download_url, downloaded_csv_path):
#             # Compare the downloaded CSV with the local template
#             print(f"Comparing downloaded {local_file_name} with local template...")
#             if compare_with_local_template(downloaded_csv_path, local_csv_path):
#                 print(f"Validation successful for {local_file_name}.")
#             else:
#                 print(f"Validation failed for {local_file_name}. Data comparison did not match.")
#         else:
#             print(f"Failed to download {local_file_name}.")
