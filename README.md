# Report Validation Guide

## Overview
This guide covers the process of downloading, validating, and comparing cemetery reports using our software. The validation ensures that the downloaded report matches the expected reference file in terms of layout and data consistency.

## Prerequisites
- Ensure you have Python installed on your system.
- Install necessary Python packages if not already installed: `requests`, `csv`, `time`.
- Configure `config.py` with necessary details like `BASE_URL`, `API_VERSION`, `CEMETERY_NAME`, `USERNAME`, `PASSWORD`, `LOCAL_CSV_FILE`, and `DOWNLOAD_PATH`.

## Steps

### 1. Configuration
Before running the script, you must configure the system by setting the following variables in `config.py`:

- `BASE_URL`: The base URL of the server where the API is hosted.
- `API_VERSION`: The API version you are interacting with.
- `CEMETERY_NAME`: The name of the cemetery you are managing.
- `USERNAME` and `PASSWORD`: Credentials for API authentication.
- `LOCAL_CSV_FILE`: The full path to the local CSV file that will be used as a reference for validation.
- `DOWNLOAD_PATH`: The path where the downloaded CSV reports will be temporarily stored.

### 2. Generating a Report
Run the `main.py` script. This will authenticate with the server, request CSV report generation, and wait for the report to be prepared.

### 3. Downloading the Report
Once the report is ready, the script will automatically download it to the `DOWNLOAD_PATH`.

### 4. Validating the Report
The script will then compare the downloaded report against the `LOCAL_CSV_FILE`:

- It checks if both files have the same number of rows and columns.
- It validates that every cell in the downloaded CSV matches the corresponding cell in the reference CSV.
- If any discrepancies are found, the script will output an error indicating the row and column of the mismatch.

### 5. Cleaning Up
If the validation is successful, the script will delete the generated report from the server to maintain cleanliness and prevent data clutter.

## Usage
Simply execute the script from the command line:

```bash
python main.py
```

Follow any on-screen prompts, and the script will handle the rest.

---
