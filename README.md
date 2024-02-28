
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
- `LOCAL_CSV_FILES`: A dictionary mapping report types to paths of local reference CSV templates.
- `DOWNLOAD_PATH`: Directory path where CSV reports will be downloaded.

<!-- file_utils.py
config.py
main.py
report_utils.py 
folder data_file/ for local file csv 
folder data temp/ for temporary csv downloaded-->

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

Based on your request, it seems that you would like to add the capability to handle new data or endpoints using new files. What this means is that you want to expand the software's functionality to accommodate additional report types or different endpoints that aren't currently handled by the existing configuration.

Here's an updated section explaining how to add new data endpoints and the corresponding report templates:

---

## Adding New Data or Endpoints

To extend the software's functionality for new kinds of reports or endpoints, follow these steps:

### Configuration File Updates:

1. Add a new entry in the `LOCAL_CSV_FILES` dictionary within the `config.py` file for the new report type. Ensure you provide a meaningful key and the file path to your new local reference CSV template.

```python
# Filepaths
LOCAL_CSV_FILES = {
    'inv_summary_section': 'data_file/astana_tegal_gundul_template-inv_summary_section.csv',
    'inv_summary_cemetery': 'data_file/astana_tegal_gundul_template-inv_summary_cemetery.csv',
    'new_report_type': 'data_file/new_template-new_report_type.csv'  # Add your new report type here
}
```

2. Define the payload variable for the new report type at file `main.py`. This variable should follow the naming conventions of existing payloads and be descriptive of its purpose.

```python
# Payload for the new report type
new_report_payload = {
    # Define the payload structure here
}
```

### Report Utility Function Updates:

3. In the `main.py` file, use the process_report function to include a call for your new report type, utilizing the report_type_suffix. This suffix is used to determine the correct endpoint in the request_report function from report_utils.py.
```python
def request_report(token, report_type_suffix, cemetery_name, payload):
    # Define the complete endpoint URL using the report type suffix
    endpoint_url = f"{BASE_URL}/{API_VERSION}/{cemetery_name}/{report_type_suffix}/"
```

### Main Script Changes:

4. In the `main.py` file, create a new function or update the existing `process_report` function to include a case for processing your new report type.

```python
    process_report(token, 'inv_summary_section', inv_summary_payload_section, 'inv_summary/')
```

## Usage
Execute the script via the command line with:

```bash
python main.py
