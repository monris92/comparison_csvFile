import sys
from utilities import *

def process_report(token, report_type, payload, report_type_suffix):
    report_id = request_report(token, report_type_suffix, CEMETERY_NAME, payload)
    if report_id:
        csv_url = check_csv_status_and_download(token, report_id)
        if csv_url:
            csv_path = os.path.join(DOWNLOAD_PATH, f'{report_type}_report.csv')
            if download_csv(csv_url, csv_path):
                if compare_with_local_template(csv_path, report_type):
                    print(f"{report_type.capitalize()} CSV validation successful.")
                else:
                    print(f"{report_type.capitalize()} CSV validation failed. Data comparison did not match.")
                    sys.exit(1)
            else:
                print(f"Failed to download {report_type} report CSV.")
                sys.exit(1)
            delete_report(token, report_id)
        else:
            print(f"Failed to download or validate {report_type} report CSV for report ID: {report_id}.")
            sys.exit(1)
    else:
        print(f"Failed to request {report_type} report.")
        sys.exit(1)


def main():
    token = get_access_token(USERNAME, PASSWORD)
    if not token:
        print("Failed to authenticate.")
        sys.exit(1)

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


if __name__ == "__main__":
    main()
