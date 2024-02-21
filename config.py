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
    'inv_summary_cemetery': 'data_file/astana_tegal_gundul_template-inv_summary_cemetery.csv',
    'inv_summary_sections': 'data_file/astana_tegal_gundul_template-inv_summary_sections.csv',
    'interment_cemetery': 'data_file/astana_tegal_gundul_template-interments_cemetery.csv',
    'interment_sections': 'data_file/astana_tegal_gundul_template-interments_sections.csv',
    'people_cemetery': 'data_file/astana_tegal_gundul_template-people_cemetery.csv',
    'people_sections': 'data_file/astana_tegal_gundul_template-people_sections.csv',
    'business_cemetery': 'data_file/astana_tegal_gundul_template-business_cemetery.csv',
    'business_sections': 'data_file/astana_tegal_gundul_template-business_sections.csv',
    'ROI_cemetery': 'data_file/astana_tegal_gundul_template-business_cemetery.csv',
    'ROI_sections': 'data_file/astana_tegal_gundul_template-business_sections.csv',


    'events': 'data_file/astana_tegal_gundul_template-events.csv'

}