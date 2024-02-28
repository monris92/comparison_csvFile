# Comparison CSV File

## Introduction

This project is designed to download CSV files from specified URLs and compare them with local templates to ensure they match. It's particularly useful for validating data integrity and consistency across different datasets.

## Installation

### Prerequisites

- Python 3.x
- Required Python packages: `requests`

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/monris92/comparison_csvFile.git
   ```
2. Navigate to the project directory:
   ```
   cd comparison_csvFile
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the necessary configuration in `config.py`, including the download URLs and local CSV file paths.
2. Run the main script:
   ```
   python main.py
   ```
3. The script will download the specified CSV files and compare them with the local templates.

## Functionalities

### `main.py`

- **Main Functionality**: Orchestrates the process of downloading and comparing CSV files.
- **Key Functions**:
 - `main()`: Initializes the process by defining file names and URLs, then calls `process_csv_files()` to handle the CSV file processing.

### `file_utils.py`

- **Main Functionality**: Provides utility functions for file handling and CSV comparison.
- **Key Functions**:
 - `normalize_newlines(text)`: Normalizes newline characters in a given text.
 - `compare_csv(downloaded_csv_path, local_csv_file)`: Compares a downloaded CSV file with a local template file.
 - `compare_with_local_template(downloaded_csv_path, local_csv_key, local_csv_files)`: Compares the downloaded CSV file with the appropriate local template based on a key.

### `report_utils.py`

- **Main Functionality**: Handles the downloading of CSV files from URLs and processing them.
- **Key Functions**:
 - `download_csv_from_url(download_url, downloaded_csv_path)`: Downloads a CSV file from a given URL and saves it to a specified path.
 - `process_csv_files(files_to_process, file_utils)`: Processes a list of CSV files by downloading them and comparing them with local templates.

## Contribution

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
