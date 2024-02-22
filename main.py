from auth import *
from report_utils import *


def main():
    token = get_access_token(USERNAME, PASSWORD)
    if not token:
        print("Failed to authenticate.")
        sys.exit(1)

    # Define payloads for different reports

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
        "sections": [],
        "cemeteries": [CEMETERY_NAME]
    }

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

    act_summary_payload_cemetery = {}

    act_summary_payload_sections = {
        "attributes": [
            "section",
            "entombment",
            "burial",
            "other",
            "cremation"
        ],
        "document_format": "csv",
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "chapters": [
            "interments",
            "rois"
        ],
        "date_from": "2000-01-01T00:00:00Z",
        "date_to": "2024-01-01T00:00:00Z"
    }

    interment_payload_cemetery = {
        "attributes": [
            "section",
            "entombment",
            "burial",
            "other",
            "cremation"
        ],
        "document_format": "csv",
        "sections": [],
        "cemeteries": [CEMETERY_NAME],
        "chapters": [
            "interments",
            "rois"
        ],
        "date_from": "2000-01-01T00:00:00Z",
        "date_to": "2024-01-01T00:00:00Z"
    }

    interment_payload_section = {
        "attributes": [
            "plot_id",
            "date_of_birth",
            "name",
            "date_of_death",
            "interment_date",
            "interments_type",
            "funeral_director",
            "religion",
            "funeral_minister",
            "interment_number",
            "next_of_kin",
            "cremation_location",
            "interment_depth",
            "container_type",
            "age",
            "container_dimensions",
            "returned_serviceman",
            "applicant_relationship",
            "occupation",
            "next_of_kin_relationship",
            "cause_of_death"
        ],
        "document_format": "csv",
        "custom_fields": [
            "astana_tegal_gundul_maiden_name",
            "astana_tegal_gundul_baby_section",
            "astana_tegal_gundul_military_branch"
        ],
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "date_from": "2000-01-01T00:00:00Z",
        "date_to": "2024-01-01T00:00:00Z"
    }

    people_payload_cemetery = {
        "attributes": [
            "plot_id",
            "person_name",
            "contact_number",
            "contact_address",
            "postal_address",
            "email",
            "roi_certificate",
            "roi_payment_date",
            "interment_date",
            "interment_type",
            "interment_number",
            "date_of_birth",
            "date_of_death",
            "age"
        ],
        "document_format": "csv",
        "sections": [],
        "cemeteries": [CEMETERY_NAME],
        "chapters": [
            "roi_holders",
            "roi_applicants",
            "interments",
            "next_of_kins",
            "interment_applicants"
        ],
        "first_name": None,
        "last_name": None
    }

    people_payload_sections = {
        "attributes": [
            "plot_id",
            "person_name",
            "contact_number",
            "contact_address",
            "postal_address",
            "email",
            "roi_certificate",
            "roi_payment_date",
            "interment_date",
            "interment_type",
            "interment_number",
            "date_of_birth",
            "date_of_death",
            "age"
        ],
        "document_format": "csv",
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "chapters": [
            "roi_holders",
            "roi_applicants",
            "interments",
            "next_of_kins",
            "interment_applicants"
        ],
        "first_name": None,
        "last_name": None
    }

    business_payload_cemetery = {
        "attributes": [
            "business_name",
            "person_name",
            "contact_number",
            "contact_address",
            "postal_address",
            "email"
        ],
        "document_format": "csv",
        "sections": [],
        "cemeteries": [CEMETERY_NAME],
        "chapters": [
            "funeral_ministers",
            "funeral_directors",
            "interment_applicants"
        ],
        "business_name": None
    }

    business_payload_sections = {
        "attributes": [
            "business_name",
            "person_name",
            "contact_number",
            "contact_address",
            "postal_address",
            "email"
        ],
        "document_format": "csv",
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "chapters": [
            "funeral_ministers",
            "funeral_directors",
            "interment_applicants"
        ],
        "business_name": None
    }

    ROI_payload_cemetery = {
        "attributes": [
            "plot_id",
            "roi_holder_1",
            "application_date",
            "payment_date",
            "contact_number",
            "payment_status",
            "contact_address",
            "payment_amount",
            "postal_address",
            "right_type",
            "email",
            "roi_certificate",
            "roi_holder_2",
            "service_need",
            "roi_holder_3",
            "plot_status",
            "expiry_date",
            "term_of_right",
            "roi_holder_2_3_contacts"
        ],
        "document_format": "csv",
        "custom_fields": [
            "astana_tegal_gundul_place_of_birth",
            "astana_tegal_gundul_place_of_death"
        ],
        "sections": [],
        "cemeteries": [CEMETERY_NAME],
        "date_from": "2000-01-01T00:00:00Z",
        "date_to": "2024-01-01T00:00:00Z"
    }

    ROI_payload_sections = {
        "attributes": [
            "plot_id",
            "roi_holder_1",
            "application_date",
            "payment_date",
            "contact_number",
            "payment_status",
            "contact_address",
            "payment_amount",
            "postal_address",
            "right_type",
            "email",
            "roi_certificate",
            "roi_holder_2",
            "service_need",
            "roi_holder_3",
            "plot_status",
            "expiry_date",
            "term_of_right",
            "roi_holder_2_3_contacts"
        ],
        "document_format": "csv",
        "custom_fields": [
            "astana_tegal_gundul_place_of_birth",
            "astana_tegal_gundul_place_of_death"
        ],
        "sections": REPORT_SECTIONS,
        "cemeteries": [],
        "date_from": "2000-01-01T00:00:00Z",
        "date_to": "2024-01-01T00:00:00Z"
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
            "cover_image"
        ],
        "document_format": "csv",
        "sections": [],
        "cemeteries": [CEMETERY_NAME],
        "date_from": "2023-01-01T00:00:00Z",
        "date_to": "2024-01-01T00:00:00Z",
        "mon_year": "02/2024",
        "status_event": "all",
        "assigned_party": None,
        "responsible_person": None,
        "event_type": None,
        "event_sub_type": None,
        "event_status": None
    }

    log_activity_payload = {
        "document_format": "csv",
        "sections": [],
        "cemeteries": [],
        "mon_year": "01/2024"
    }

    # Process each report
    process_report(token, 'inv_summary_cemetery', inv_summary_payload_cemetery, 'inv_summary/'),
    process_report(token, 'inv_summary_sections', inv_summary_payload_section, 'inv_summary/')

    # process_report(token, 'act_summary_cemetery', act_summary_payload_cemetery, 'act_summary/')
    process_report(token, 'act_summary_sections', act_summary_payload_sections, 'act_summary/')

    # process_report(token, 'interment_cemetery', interment_payload_cemetery, 'interment/')
    process_report(token, 'interment_sections', interment_payload_section, 'interments/')

    # process_report(token, 'people_cemetery', people_payload_cemetery, 'people/')
    process_report(token, 'people_sections', people_payload_sections, 'people/')

    # process_report(token, 'business_cemetery', business_payload_cemetery, 'business/')
    process_report(token, 'business_sections', business_payload_sections, 'business/')

    # process_report(token, 'ROI_cemetery', ROI_payload_cemetery, 'roi/')
    process_report(token, 'ROI_sections', ROI_payload_sections, 'roi/')

    process_report(token, 'events', events_payload, 'events/')
    process_report(token, 'log_activity', log_activity_payload, 'log_activity/')

    # process_report(token, 'events', events_payload, 'events/')

    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/inv_summary/ done
    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/interments/ done
    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/people/ done
    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/business/ done
    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/roi/ done
    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/act_summary/
    # - {{baseUrl-v2}}/reports/cemetery/{{cemetery-unique_name}}/generate/log_activity/

if __name__ == "__main__":
    main()
