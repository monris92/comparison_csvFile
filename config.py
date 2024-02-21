import os

# API Endpoints
BASE_URL = "https://map.chronicle.rip/api"
API_VERSION_V1 = "v1"
API_VERSION_V2 = "v2"
DOWNLOAD_PATH = "temp/"

# Report Configurations
REPORT_ATTRS = ["plot_id"]
REPORT_SECTIONS = ["Section A", "Section B"]
REPORT_CHAPTERS = [
    "roi_holders",
    "roi_applicants",
    "interments",
    "next_of_kins",
    "interment_applicants",
]
CEMETERY_NAME = "Astana_Tegal_Gundul"

# Credentials (should be environment variables for security)
USERNAME = os.environ['USER_SUPER_ADMIN']
PASSWORD = os.environ['PASS_SUPER_ADMIN']

# Filepaths
LOCAL_CSV_FILES = {
    'people': 'data_file/astana_tegal_gundul_template-people.csv',
    'events': 'data_file/astana_tegal_gundul_template-events.csv',
    'inv_summary_section': 'data_file/astana_tegal_gundul_template-inv_summary_section.csv',
    'inv_summary_cemetery': 'data_file/astana_tegal_gundul_templated-inv_summary_cemeteryss.csv'
}