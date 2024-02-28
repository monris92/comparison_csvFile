# Comparison CSV File Project

## Introduction

This project is designed to download CSV files from specified URLs and compare them with local template files. The comparison is done to ensure that the downloaded files match the expected format and content. This can be particularly useful for validating data integrity and consistency across different sources.

## Project Structure

The project is organized into several key components:

- `config.py`: Contains configuration settings such as API endpoints, download paths, and mappings of local CSV file names to their paths.
- `file_utils.py`: Utility functions for file operations, including normalizing newlines, comparing CSV files, and comparing a downloaded CSV file with a local template file.
- `report_utils.py`: Utility functions for downloading CSV files from URLs and processing them, including comparing them with local templates.
- `main.py`: The entry point of the application, which defines the files to process and initiates the CSV file comparison process.

## Setting Up the Project

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Ensure you have Python installed on your machine. This project does not require any external libraries beyond the standard Python library.
3. **Configure the Project**: Update the `config.py` file with the appropriate API endpoints and local CSV file paths as needed.

## Running the Project

1. **Navigate to the Project Directory**: Open a terminal or command prompt and navigate to the root directory of the project.
2. **Run the Main Script**: Execute the `main.py` script using Python. This will initiate the process of downloading and comparing the CSV files.

## Usage

The `main.py` script is designed to process a predefined set of CSV files. It downloads each file from its specified URL and compares it with a local template file. If the files match, a success message is printed; otherwise, a failure message is printed.

## Contributing

Contributions to this project are welcome. Please feel free to submit pull requests or open issues for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

