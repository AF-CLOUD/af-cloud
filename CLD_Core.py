# Ver 0.1.1 : 2021.10.18
# Ver 0.2.1 : 2021.10.19 / input 분리 적기엔 너무 많이 수정해버렸네

import display as DIS
from API_GoogleCloud import GDrive
from output_csv import CSVExport

file_list = []

# 시작 디스플레이
DIS.start_display()

# 클라우드 종류 선택
cloud = DIS.cloud_type()

# 로그인 정보 입력
DIS.login_data()

############################################
### 로그인 정보로 credentials.json 파일 생성 ###
############################################

# Google Drive
if cloud == 1:
    try:
        TOKEN_FILE = 'credentials.json'
        PORT = 3377
        SCOPES = ['https://www.googleapis.com/auth/drive']
        drive = GDrive(TOKEN_FILE, PORT, SCOPES)
        tmp_csv = drive.run()

        # make csv file
        export_path = os.path.abspath(os.path.dirname(__file__)) + os.sep + 'export'
        Path(export_path).mkdir(parents=True, exist_ok=True)
        for cnt, info in enumerate(tmp_csv, start=1):
            export = CSVExport(export_path + os.sep + "GDrive_search_" + str(cnt))
            export.input_dict(info)
        print(" [*] Export csv!")
    except Exception as e:
        print(" [-] Login failed; ", e)
