from utilities import *
from config import *
import sys


def get_api_url(version, endpoint, cemetery_name=None):
    if cemetery_name:
        return f'{BASE_URL}/{version}/{endpoint}/{cemetery_name}/'
    return f'{BASE_URL}/{version}/{endpoint}/'
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