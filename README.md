# Report Validation Guide

## Overview
This guide provides instructions on how to use our software to download, validate, and compare cemetery reports. The validation process ensures that the downloaded reports correctly align with the expected reference templates, both in format and data integrity.

## Prerequisites
- Python must be installed on your system.
- All required Python dependencies should be installed: `requests`, `csv`, `os`, `sys`, and `time`.
- The `config.py` file should be set up with the necessary configurations, such as `BASE_URL`, `API_VERSION`, `CEMETERY_NAME`, plus authentication credentials and file paths.

## Configuration Setup
Set the appropriate values in `config.py`:

- `BASE_URL`: The API's base URL.
- `API_VERSION`: The version of the API in use.
- `CEMETERY_NAME`: The target cemetery name for report management.
- `USERNAME`, `PASSWORD`: The API authentication credentials.
- `LOCAL_CSV_FILES`: A dictionary mapping report types to paths of local reference CSV templates.
- `DOWNLOAD_PATH`: Directory path where CSV reports will be downloaded.

## Process Workflow

### 1. Authentication
Run `auth.py`, which first authenticates against the API using the provided credentials and retrieves an access token.

### 2. Report Generation
The script requests report generation from the API. It waits until the report is processed and ready for download.

### 3. Report Retrieval
After report readiness is confirmed, the script downloads it to the specified `DOWNLOAD_PATH`.

### 4. Report Validation
The script compares the downloaded report with the corresponding reference template in `LOCAL_CSV_FILES`:

- It verifies that both files match in the number of rows and columns.
- It checks each cell for data consistency.
- Discrepancies are reported, detailing the specific location(s) within the file where mismatches occur.

### 5. Clean-Up
Upon successful validation, the script instructs the server to delete the generated report, ensuring efficient data management.

## Usage
Execute the script via the command line with:

```bash
python main.py