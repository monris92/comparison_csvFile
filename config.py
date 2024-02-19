import os

# API Endpoints
BASE_URL = "https://map.chronicle.rip/api"
API_VERSION_V1 = "v1"
API_VERSION_V2 = "v2"
DOWNLOAD_PATH = "temp/temporaryFile.csv"

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
LOCAL_CSV_FILE = 'astana_tegal_gundul_people-template.csv'