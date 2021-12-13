# Ver 0.1.1 : 2021.10.18
# Ver 0.2.1 : 2021.10.19 / input 분리 적기엔 너무 많이 수정해버렸네
# testestsetsetstet
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
        cnt = 0

        # make csv file
        for info in tmp_csv:
            export = CSVExport("GDrive_search_" + str(cnt))
            export.input_dict(info)
            cnt += 1
        print(" [*] Export csv!")
    except Exception as e:
        print(" [-] Login Failed; ", e)
