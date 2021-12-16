# Coding by YES
# Reference: Google
# Ver 1.0: Get Filelist + Searching Option(keyword, modified period)

import os
import os.path
from pathlib import Path
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
        tmp_csv = []
        while True:
            DIS.start_menu()
            menu = DIS.select_menu()
            if menu == "0": # exit
                break
            elif menu == "1":  # all of file
                file_list = self.__no_search(service)
            elif menu == "2":  # select file
                file_list = self.__search(service)
            else:
                DIS.invalid_menu()
                continue

            DIS.show_file_list(file_list)
            # download file
            print("\n"
                  "To download file(s), put file numbers separated by space.\n"
                  "If you don't want to download file(s), hit enter.\n"
                  "Example input: 1~4 19 10~11\n")
            download_number_str = input("Put file numbers: ")
            if download_number_str:
                download_number = []
                for s in download_number_str.split(" "):
                    if "~" in s:
                        start_num, end_num = s.split("~")
                        download_number.extend([i for i in range(int(start_num), int(end_num) + 1)])
                    else:
                        download_number.append(int(s))

                for i in download_number:
                    try:
                        down_start = time.time()
                        self.__file_download(service, file_list[i][10], file_list[i][0], file_list[i][11])
                        down_end = time.time()
                        print("%s | Download time(s) : " % file_list[i][1], down_end - down_start)
                    except Exception as e:
                        print(" [-] Failed to download; ", e)

            tmp_csv.append(file_list)

        return tmp_csv

    def __no_search(self, service):
        try:
            file_list = self.__get_flist(service)
            print(" [*] Success no_search()")
            return file_list
        except Exception as error:
            print(" [!] Failed to no_search(); %s" % error)
            exit(1)

    def __search(self, service):
        try:
            g_input = CInput()
            g_input.set_gdrive_inputs()

            search_query = "mimeType != 'application/vnd.google-apps.folder'"
            # Set keyword - name & text
            search_keyword_name = g_input.get_keyword_name()
            if search_keyword_name:
                search_keyword_name = '\'' + search_keyword_name + '\''
                search_query = "".join([search_query, " and ", "name contains %s" % search_keyword_name])
            # Set keyword - text
            search_keyword_text = g_input.get_keyword_text()
            if search_keyword_text:
                search_keyword_text = '\'' + search_keyword_text + '\''
                search_query = "".join([search_query, " and ", "fullText contains %s" % search_keyword_text])
            # Set period
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
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.token_file, scopes=self.scopes)
                creds = flow.run_local_server(port=self.port)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)
        os.remove('token.json')
        return service

    def __get_flist(self, service):
        result = list()
        result.append(
            ['file name', 'size', 'is_shared', 'is_trashed', 'createdTime', 'modifiedTime', 'lastModifyingUser',
             'sharedWithMeTime', 'sharingUser.emailAddress', 'sharingUser.permissionID', 'fileID', 'mimeType'])
        page_token = None
        while True:
            response = service.files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, size, name, trashed, createdTime, '
                                                   'modifiedTime, lastModifyingUser, shared,'
                                                   'sharedWithMeTime, sharingUser, mimeType)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                result.append([file.get('name'), file.get('size'), file.get('shared'), file.get('trashed'),
                               file.get('createdTime'), file.get('modifiedTime'),
                               file.get('lastModifyingUser.displayName'), file.get('SharedWithMeTime'),
                               file.get('sharingUser.emailAddress'), file.get('sharingUser.permissionID'),
                               file.get('id'), file.get('mimeType')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return result

    def __get_selection_flist(self, service, search_query: str):
        result = list()
        result.append(['file name', 'size', 'is_shared', 'is_trashed', 'createdTime', 'modifiedTime', 'lastModifyingUser',
                       'sharedWithMeTime', 'sharingUser.emailAddress', 'sharingUser.permissionID', 'fileID', 'mimeType'])
        page_token = None
        while True:
            response = service.files().list(q=search_query,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, size, name, trashed, createdTime, '
                                                   'modifiedTime, lastModifyingUser, shared,'
                                                   'sharedWithMeTime, sharingUser, mimeType)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                result.append([file.get('name'), file.get('size'), file.get('shared'), file.get('trashed'), file.get('createdTime'), file.get('modifiedTime'),
                                      file.get('lastModifyingUser'), file.get('SharedWithMeTime'),file.get('sharingUser.emailAddress'), file.get('sharingUser.permissionID'),
                                      file.get('id'), file.get('mimeType')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return result

    def __file_download(self, service, file_id, file_name, mimetype):
        Path('./extract').mkdir(parents=True, exist_ok=True)

        dic_mimetype = {
            'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.google-apps.presentation': ['application/vnd.openxmlformats-officedocument.presentationml.presentation', 'pptx']
        }
        mime_to_ext = {
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx'
        }

        if 'application/vnd.google-apps.' in mimetype:
            request = service.files().export_media(fileId=file_id, mimeType=dic_mimetype[mimetype])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            fh.seek(0)
            with open("./extract/" + file_name + mime_to_ext[dic_mimetype[mimetype]], 'wb') as f:
                shutil.copyfileobj(fh, f)

        else:
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            # with open('./' + file_id, 'wb') as f:
            #     f.write(downloader)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(status)
                print("Download %d%%." % int(status.progress() * 100))
            fh.seek(0)
            with open("./extract/"+file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)
