from auth import *
from report_utils import *


def main():
    token = get_access_token(USERNAME, PASSWORD)
    if not token:
        print("Failed to authenticate.")
        sys.exit(1)

    # Define payloads for different reports
    inv_summary_payload_section = {
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

    inv_summary_payload_cemetery = {
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
        "cemeteries": [CEMETERY_NAME],
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

    # Process each report
    process_report(token, 'inv_summary_section', inv_summary_payload_section, 'inv_summary/')
    process_report(token, 'inv_summary_cemetery', inv_summary_payload_cemetery, 'inv_summary/')
    # process_report(token, 'interment', interment_payload, 'interment/')
    # process_report(token, 'interment', interment_payload, 'interment/')
    # process_report(token, 'inv_summary', inv_summary_payload, 'inv_summary/')
    # process_report(token, 'inv_summary', inv_summary_payload, 'inv_summary/')
    process_report(token, 'people', people_payload, 'people/')
    # process_report(token, 'people', people_payload, 'people/')
    process_report(token, 'events', events_payload, 'events/')
    # process_report(token, 'events', events_payload, 'events/')


if __name__ == "__main__":
    main()
