import csv

import requests


def download_csv(download_url, local_file_path):
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV downloaded successfully to {local_file_path}.")
        return True
    else:
        print("Failed to download CSV.")
        return False


def compare_csv(downloaded_csv_path, local_csv_file):
    with open(downloaded_csv_path, newline='', encoding='utf-8') as downloaded_file:
        downloaded_csv_reader = csv.reader(downloaded_file)
        downloaded_csv = list(downloaded_csv_reader)

    with open(local_csv_file, newline='', encoding='utf-8') as local_file:
        local_csv_reader = csv.reader(local_file)
        local_csv = list(local_csv_reader)

    if len(downloaded_csv) != len(local_csv):
        print("Validation failed: Number of rows does not match.")
        return False

    for row_index, (downloaded_row, local_row) in enumerate(zip(downloaded_csv, local_csv)):
        if downloaded_row != local_row:
            print(f"Validation failed at row {row_index + 1}:")
            print(f"Downloaded: {downloaded_row}")
            print(f"Local: {local_row}")
            return False

    print("All validations passed.")
    return True


def compare_with_local_template(downloaded_csv_path, report_type_suffix, local_csv_files):
    local_csv_file = local_csv_files.get(report_type_suffix)
    if not local_csv_file:
        print(f"No local CSV template found for report type '{report_type_suffix}'.")
        return False

    return compare_csv(downloaded_csv_path, local_csv_file)
