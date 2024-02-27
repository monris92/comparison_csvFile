from config import URL_100USER, URL_1000USER
from report_utils import process_csv_files
import file_utils


def main():
    # Define file names and the corresponding URLs
    files_to_process = {
        'customers-100.csv': URL_100USER,
        'customers-1000.csv': URL_1000USER,
    }

    # Process the CSV files
    process_csv_files(files_to_process, file_utils)


if __name__ == "__main__":
    main()