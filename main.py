from report_utils import process_csv_files
from config import URL_100USER, URL_1000USER


def main():
    # Define file names and the corresponding URLs
    files_to_process = {
        'customers-100.csv': URL_100USER,
        'customers-1000.csv': URL_1000USER,
    }

    # Process the CSV files
    process_csv_files(files_to_process)


if __name__ == "__main__":
    main()