import json
import sys
from utilities import *

# Make sure the following variable placeholders are defined or passed appropriately:
# USERNAME, PASSWORD, CEMETERY_NAME, DOWNLOAD_PATH, REPORT_ATTRS, REPORT_SECTIONS, REPORT_CHAPTERS

def process_report(token, report_name, payload, report_type_suffix):
    try:
        report_id = request_report(token, report_type_suffix, CEMETERY_NAME, payload)
        if report_id:
            csv_url = check_csv_status_and_download(token, report_id)
            if csv_url:
                csv_path = os.path.join(DOWNLOAD_PATH, f'{report_name}_report.csv')
                if download_csv(csv_url, csv_path):
                    if compare_with_local_template(csv_path, report_name):
                        print(f"{report_name.capitalize()} CSV validation successful.")
                    else:
                        print(f"{report_name.capitalize()} CSV validation failed. Data comparison did not match.")
                        sys.exit(1)
                else:
                    print(f"Failed to download {report_name} report CSV.")
                    sys.exit(1)
                delete_report(token, report_id)
            else:
                print(f"Failed to download or validate {report_name} report CSV for report ID: {report_id}.")
                sys.exit(1)
        else:
            print(f"Failed to request {report_name} report.")
            sys.exit(1)
    except Exception as e:
        error_message = str(e)
        print(f"An error occurred while processing {report_name} report: {error_message}")
        print("Payload for failed request:")
        print(json.dumps(payload, indent=4))  # Assumes 'payload' is a dictionary
        raise  # Re-raise the exception to handle it in the main function

def main():
    try:
        token = get_access_token(USERNAME, PASSWORD)
        if not token:
            raise Exception("Failed to authenticate.")

        # Define payloads for different reports
        people_payload = {
            "attributes": REPORT_ATTRS,
            "document_format": "csv",
            "sections": REPORT_SECTIONS,
            "cemeteries": [],
            "chapters": REPORT_CHAPTERS,
            "first_name": None,
            "last_name": None
        }

        events_payload = {
    "attributes": [
        "plot_id",
        "event_name",
        "event_types",
        "event_subtypes_id",
        "event_status_id",
        "descriptions",
        "location_type",
        "cremation_location",
        "event_date",
        "start_time",
        "end_time",
        "repeating",
        "assigned_party",
        "created_by",
        "related_interment",
        "event_payment",
        "event_purchaser"
    ],
    "document_format": "csv",
    "sections": [],
    "cemeteries": CEMETERY_NAME,
    "date_from": None,
    "date_to": None,
    "mon_year": "02/2024",
    "status_event": "all",
    "assigned_party": None,
    "responsible_person": None,
    "event_type": 28313,
    "event_sub_type": 32089,
    "event_status": None
}

        inv_summary_payload = {
            "attributes": [
                "section",
                "reserved",
                "total",
                "occupied",
                "vacant",
                "unavailable",
                "for_sale"
            ],
            "document_format": "csv",
            "sections": REPORT_SECTIONS,
            "cemeteries": []
        }

        # Process each report
        process_report(token, 'people', people_payload, 'people/')
        process_report(token, 'events', events_payload, 'events/')
        process_report(token, 'inv_summary', inv_summary_payload, 'inv_summary/')

    except Exception as e:
        print(f"An unknown error occurred: {e}")
        sys.exit(1)  # Exit the script with an error code

if __name__ == "__main__":
    main()