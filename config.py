import os
# Simpan konfigurasi dan variabel lingkungan yang umum di sini
username = os.environ['USER_SUPER_ADMIN']
password = os.environ['PASS_SUPER_ADMIN']
local_csv_file = 'astana_tegal_gundul_people-template.csv'
API_BASE_URL_V2 = "https://map.chronicle.rip/api/v2"
CEMETERY_NAME = "Astana_Tegal_Gundul"

# report variable
REPORT_GENERATE_ENDPOINT = f"{API_BASE_URL_V2}/reports/cemetery/{CEMETERY_NAME}/generate/people/"
REPORT_ATTRS = ["plot_id"]
REPORT_SECTIONS = ["Section A", "Section B"]
REPORT_CHAPTERS = [
    "roi_holders",
    "roi_applicants",
    "interments",
    "next_of_kins",
    "interment_applicants",
]