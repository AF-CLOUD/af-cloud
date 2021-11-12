# Coding by YES
# Reference: Google
# Ver 1.0: Get Filelist + Searching Option(keyword, modified period)

import os.path
import io
import shutil
import time
import display as DIS
from input import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GDrive:

    def __init__(self, token_file: str, port: int, scopes: list):
        print(" [*] Init Google Drive")
        self.token_file = token_file
        self.port = port
        self.scopes = scopes

    def run(self):
        service = self.__G_Oauth()
        while True:
            DIS.start_menu()
            menu = DIS.select_menu()
            if menu == 0: # exit
                exit(1)
            if menu >= 3:
                DIS.invalid_menu()
                continue

            # print file list
            file_list = []
            if menu == 1: # all of file
                file_list = self.__no_search(service)
            elif menu == 2: # select file
                file_list = self.__search(service)

            DIS.show_file_list(file_list)
            # download file
            try:
                print("\n"
                      "If you want to download file, enter the number of the files you want by dividing it into spacing.\n"
                      "If you don't want, please click enter\n"
                      "download input example: 19 2 10\n")
                download_number = input("Input your number: ")
                if download_number:
                    for i in download_number.split(" "):
                        down_start = time.time()
                        #self.__file_download(service, file_list[int(i, 10)][0], file_list[int(i, 10)][1])
                        self.__file_download(service, file_list[int(i)][0], file_list[int(i)][1])
                        down_end = time.time()
                        print("%s | download time(s) : "%file_list[int(i)][1], down_end - down_start)
            except Exception as e:
                print(" [-] Failed to file_download(); ", e)

            #return file_list

    def __no_search(self, service):
        try:
            file_list = self.__get_flist(service)
            print(" [*] Success ")
            return file_list
        except Exception as error:
            print(" [!] Failed to no_search(); %s" % error)
            exit(1)

    def __search(self, service):
        try:
            g_input = CInput()
            g_input.set_gdrive_inputs()

            search_query = "mimeType != 'application/vnd.google-apps.folder'"
            search_keyword = g_input.get_keyword()
            if search_keyword:
                search_keyword = '\'' + search_keyword + '\''
                search_query = "".join([search_query, " and ", "name contains %s" % search_keyword])

            search_period = g_input.get_m_period()
            if search_period[0] and search_period[1]:
                s_period = '\'' + search_period[0] + "T00:00:00" + '\''
                e_period = '\'' + search_period[1] + "T23:59:59" + '\''
                search_query = "".join([search_query, " and ", "modifiedTime > %s" % s_period,
                                                      " and ", "modifiedTime < %s" % e_period])
            g_input.show_input()

            file_list = self.__get_selection_flist(service, search_query)
            print(" [*] Success ")
            return file_list
        except Exception as error:
            print(" [!] Failed to search(); %s" % error)
            exit(1)

    def __G_Oauth(self):
        creds = None

        # Oauth 인증으로 생성된 token.json 파일의 유무를 확인하는 코드
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # Credential.json 파일은 실행하는 .py 파일과 동일한 위치에 있어야 함
            # Credential.json은 Google Cloud Platform API 서비스에서 다운 가능.
            # Oauth 인증은 Desktop client / Web client 두팀으로 나눠서 진행예정
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.token_file, scopes=self.scopes)
                creds = flow.run_local_server(port=self.port)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        return service

    def __get_flist(self, service):
        result = list()
        result.append(['FileID', 'File name', 'is_shared', 'is_trashed', 'ctime'])  # 나중에 승아가 정리하면 변경 #
        page_token = None
        while True:
            response = service.files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, shared, trashed, createdTime)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                result.append([file.get('id'), file.get('name'), file.get('shared'), file.get('trashed'), file.get('createdTime')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return result

    def __get_selection_flist(self, service, search_query: str):
        result = list()
        result.append(['FileID', 'File name', 'is_shared', 'is_trashed', 'ctime'])  # 나중에 승아가 정리하면 변경 #
        page_token = None
        while True:
            response = service.files().list(q=search_query,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, shared, trashed, createdTime)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                result.append([file.get('id'), file.get('name'), file.get('shared'), file.get('trashed'), file.get('createdTime')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return result

    def __file_download(self, service, file_id, file_name):
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        # with open('./' + file_id, 'wb') as f:
        #     f.write(downloader)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            #print(status)
            print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)
