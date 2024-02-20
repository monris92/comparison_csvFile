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
                "event_purchaser",
                "story_data_id",
                "responsible_person",
                "cover_image"
            ],
            "document_format": "csv",
            "sections": [],
            "cemeteries": [
                "Cootamundra_Cemetery"
            ],
            "date_from": None,
            "date_to": None,
            "mon_year": "11/2023",
            "status_event": "Upcoming",
            "assigned_party": None,
            "responsible_person": None,
            "event_type": None,
            "event_sub_type": None,
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
            "sections": [
                "Section A",
                "Section B"
            ],
            "cemeteries": []
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