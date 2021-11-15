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
        for info in tmp_csv:
            export = CSVExport("GDrive_search_")
            export.input_dict(info)
        print(" [*] Export csv!")
    except Exception as e:
        print(" [-] Login Failed; ", e)

else:
    pass

# while True:
#     DIS.start_menu()
#     menu = DIS.select_menu()
#
#     if menu == 1:
#         # DIS.add_file(file_list)
#         DIS.show_file_list(file_list)
#     elif menu == 2:
#         file_list = []
#         DIS.add_file(file_list)
#         DIS.show_file_list(file_list)
#         dl_item = int(input("Select Item: "))
#         dl_path = input("Select Path: ")
#         DIS.download_item(file_list, dl_item, dl_path)
#     elif menu == 3:
#         type = DIS.search_type()
#         if type == 1:
#             period = []
#             keyword, period = DIS.search_with_period()
#             file_list_search = drive.get_period_flist(keyword, period)
#             DIS.show_file_list(file_list_search)
#         elif type == 2:
#             keyword = DIS.search_with_keyword()
#             file_list_search = drive.get_keyword_flist(keyword)
#             DIS.show_file_list(file_list_search)
#         else:
#             DIS.invalid_menu()
#     elif menu == 4:
#         break
#     else:
#         DIS.invalid_menu()