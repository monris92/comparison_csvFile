import csv
from io import StringIO
import sys
from config import LOCAL_CSV_FILES


def normalize_newlines(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


def compare_csv(downloaded_csv_path, local_csv_file):
    """
    Compares a downloaded CSV file with a local template file.

    Args:
        downloaded_csv_path (str): The path to the downloaded CSV file.
        local_csv_file (str): The path to the local template CSV file.

    Returns:
        bool: True if the files match, False otherwise.
    """
    # Normalize newlines and read the contents of the downloaded file
    with open(downloaded_csv_path, 'r', encoding='utf-8') as downloaded_file:
        downloaded_csv_content = normalize_newlines(downloaded_file.read())

    # Normalize newlines and read the contents of the local file
    with open(local_csv_file, 'r', encoding='utf-8') as local_file:
        local_csv_content = normalize_newlines(local_file.read())

    # Use StringIO to treat strings as file-like objects for csv.reader
    downloaded_csv = csv.reader(StringIO(downloaded_csv_content))
    local_csv = csv.reader(StringIO(local_csv_content))

    # Compare the content row by row
    for downloaded_row, local_row in zip(downloaded_csv, local_csv):
        if downloaded_row != local_row:
            print("Validation failed: Rows do not match.")
            print(f"Downloaded: {downloaded_row}")
            print(f"Local: {local_row}")
            sys.exit(1)

    # Check if we've reached the end of both files
    if next(downloaded_csv, None) or next(local_csv, None):
        print("Validation failed: One of the files has extra rows.")
        return False

    # If all rows match and there are no extra rows, the files are the same
    print("Validation passed: Files are identical.")
    return True



def compare_with_local_template(downloaded_csv_path, local_csv_key, local_csv_files):
    """
    Compares the downloaded CSV file with the appropriate local template.

    Args:
        downloaded_csv_path (str): The path to the downloaded CSV file.
        local_csv_key (str): The key to identify the local CSV file template.
        local_csv_files (dict): A dictionary mapping keys to local CSV file paths.

    Returns:
        bool: True if the files match, False otherwise.
    """
    local_csv_path = local_csv_files.get(local_csv_key)
    if not local_csv_path:
        print(f"No local CSV template found for key '{local_csv_key}'.")
        return False

    return compare_csv(downloaded_csv_path, local_csv_path)