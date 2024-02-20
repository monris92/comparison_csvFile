import sys
import os
from utilities import *
from config import *

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
                "person_name",
                "contact_number",
                "contact_address",
                "postal_address",
                "roi_payment_date"
            ],
            "document_format": "pdf",
            "sections": [],
            "cemeteries": CEMETERY_NAME,
            "chapters": [
                "roi_holders",
                "roi_applicants",
                "interments",
                "next_of_kins",
                "interment_applicants"
            ],
            "first_name": "",
            "last_name": None

    }

    inv_summary_payload = {

            "attributes": [
                "section",
                "reserved"
            ],
            "document_format": "csv",
            "sections": [],
            "cemeteries": CEMETERY_NAME

    }

    # Request and process 'people' report
    people_report_id = request_report(token, 'people/', CEMETERY_NAME, people_payload)
    if people_report_id:
        people_csv_url = check_csv_status_and_download(token, people_report_id)
        if people_csv_url:
            people_csv_path = os.path.join(DOWNLOAD_PATH, 'people_report.csv')
            if download_csv(people_csv_url, people_csv_path):
                if compare_with_local_template(people_csv_path, 'people'):
                    print("People CSV validation successful.")
                else:
                    print("People CSV validation failed.")
            delete_report(token, people_report_id)
        else:
            print("Failed to download or validate 'people' report CSV.")
            sys.exit(1)

    # Request and process 'events' report
    events_report_id = request_report(token, 'events/', CEMETERY_NAME, events_payload)
    if events_report_id:
        events_csv_url = check_csv_status_and_download(token, events_report_id)
        if events_csv_url:
            events_csv_path = os.path.join(DOWNLOAD_PATH, 'events_report.csv')
            if download_csv(events_csv_url, events_csv_path):
                if compare_with_local_template(events_csv_path, 'events'):
                    print("Events CSV validation successful.")
                else:
                    print("Events CSV validation failed.")
            delete_report(token, events_report_id)
        else:
            print("Failed to download or validate 'events' report CSV.")
            sys.exit(1)

    # Request and process 'inv_summary' report
    inv_summary_report_id = request_report(token, 'inv_summary/', CEMETERY_NAME, inv_summary_payload)
    if inv_summary_report_id:
        inv_summary_csv_url = check_csv_status_and_download(token, inv_summary_report_id)
        if inv_summary_csv_url:
            inv_summary_csv_path = os.path.join(DOWNLOAD_PATH, 'inv_summary_report.csv')
            if download_csv(inv_summary_csv_url, inv_summary_csv_path):
                if compare_with_local_template(inv_summary_csv_path, 'inv_summary'):
                    print("Inventory Summary CSV validation successful.")
                else:
                    print("Inventory Summary CSV validation failed.")
            delete_report(token, inv_summary_report_id)
        else:
            print("Failed to download or validate 'inv_summary' report CSV.")
            sys.exit(1)

if __name__ == "__main__":
    main()