# Coding by YES
# Reference: Google
# Ver 1.0: Get Filelist + Searching Option(keyword(+text), modified period)
# Ver 1.0.1: File download

import os.path
import io
import csv
import shutil
import time
from pprint import pprint
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

    def no_search(self):
        try:
            service = self.__G_Oauth()
            file_list = self.__get_flist(service)
            # csv or db 만드는 코드 추가
            # ex) save csv file
            self.make_csv(file_list)
            print(" [*] Success ")
        except Exception as error:
            print(" [!] Failed to no_search(); %s" % error)
        exit(1)

    def search(self):
        try:
            keyword = input("Input your Keyword: ")
            service = self.__G_Oauth()
            file_list = self.__get_keyword_flist(service, keyword)
            self.__file_download(service, file_list[1][10], file_list[1][0], file_list[1][11])
            # csv or db 만드는 코드 추가
            # ex) save csv file
            # self.make_csv(file_list)
            print(" [*] Success ")
        except Exception as error:
            print(" [!] Failed to search(); %s" % error)
        exit(1)

    def search_with_period(self):
        try:
            period = list()
            keyword = input("Input your Keyword: ")
            period.append(input("Input the Start Time Point: "))
            period.append(input("Input the End Time Point: "))
            service = self.__G_Oauth()
            file_list = self.__get_period_flist(service, keyword, period)
            # csv or db 만드는 코드 추가
            # ex) save csv file
            self.make_csv(file_list)
            print(" [*] Success ")
        except Exception as error:
            print(" [!] Failed to search(); %s" % error)
        exit(1)

    def make_csv(self, file_list):
        with open("GDrive_search_%s.csv" % time.time(), 'w', newline='', encoding='UTF-16') as csvfile:
            columns = file_list[0]
            wr = csv.DictWriter(csvfile, fieldnames=columns, delimiter='\t')
            wr.writeheader()
            for i in range(1, len(file_list)):
                tmp = {}
                for row in range(len(columns)):
                    tmp[columns[row]] = file_list[i][row]
                wr.writerow(tmp)

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
        result = []
        result.append(['File name', 'size', 'is_shared', 'is_trashed', 'CreatedTime', 'modifiedTime', 'lastModifyingUser',
                      'SharedWithMeTime', 'SharingUser.emailAddress', 'sharingUser.permissionID', 'FileID', 'mimeType'])

        page_token = None
        # get filelist
        while True:
            response = service.files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, size, name, trashed, createdTime, modifiedTime, lastModifyingUser, shared,'
                                                   'sharedWithMeTime, sharingUser, mimeType)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                # print('Found file: %s (%s) %s [%s]' % (file.get('name'), file.get('id'), file.get('trashed'), file.get('trashedTime')))
                # print('File Shared: %s %s %s %s %s' % (file.get('name'), file.get('shared'), file.get('resourceKey'), file.get('linkShareMetadata'), file.get('exportLinks')))
                result.append([file.get('name'), file.get('size'), file.get('shared'), file.get('trashed'), file.get('createdTime'), file.get('modifiedTime'),
                              file.get('lastModifyingUser.displayName'), file.get('SharedWithMeTime'), file.get('sharingUser.emailAddress'), file.get('sharingUser.permissionID'),
                              file.get('id'), file.get('mimeType')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        for i in result:
            print(i)

        return result

    def __get_keyword_flist(self, service, search_keyword: str):

        search_result = []
        search_result.append(['File name', 'size', 'is_shared', 'is_trashed', 'CreatedTime', 'modifiedTime', 'lastModifyingUser',
                              'SharedWithMeTime', 'SharingUser.emailAddress', 'sharingUser.permissionID', 'FileID', 'mimeType'])

        page_token = None

        # get filelist result of Keyword searching
        keyword = '\'' + search_keyword + '\''
        # Filelist 뽑기
        while True:
            response = service.files().list(q="name contains %s or fullText contains %s and mimeType != 'application/vnd.google-apps.folder'" % (keyword, keyword),
                                            spaces='drive',
                                            fields='nextPageToken, files(id, size, name, trashed, createdTime, modifiedTime, lastModifyingUser, shared,'
                                                   'sharedWithMeTime, sharingUser, mimeType)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                search_result.append([file.get('name'), file.get('size'), file.get('shared'), file.get('trashed'), file.get('createdTime'), file.get('modifiedTime'),
                                      file.get('lastModifyingUser'), file.get('SharedWithMeTime'),file.get('sharingUser.emailAddress'), file.get('sharingUser.permissionID'),
                                      file.get('id'), file.get('mimeType')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        for i in search_result:
            print(i)

        return search_result

    def __get_period_flist(self, service, search_keyword: str, period: list):

        search_result = []
        search_result.append(['File name', 'size', 'is_shared', 'is_trashed', 'CreatedTime', 'modifiedTime', 'lastModifyingUser',
                              'SharedWithMeTime', 'SharingUser.emailAddress', 'sharingUser.permissionID', 'FileID', 'mimeType'])

        page_token = None

        # get filelist result of Keyword searching
        keyword = '\'' + search_keyword + '\''
        s_period = '\'' + period[0] + '\''
        e_period = '\'' + period[1] + '\''
        print(' [*] Keyword: %s\tPeriod: %s' % (keyword, period))
        # Filelist 뽑기
        while True:
            response = service.files().list(
                q="name contains %s or fullText contains %s and mimeType != 'application/vnd.google-apps.folder' and modifiedTime > %s and modifiedTime < %s" % (keyword, keyword, s_period, e_period),
                spaces='drive',
                fields='nextPageToken, files(id, size, name, trashed, createdTime, modifiedTime, lastModifyingUser, shared,'
                       'sharedWithMeTime, sharingUser, mimeType)',
                pageToken=page_token).execute()
            for file in response.get('files', []):
                search_result.append([file.get('name'), file.get('size'), file.get('shared'), file.get('trashed'), file.get('createdTime'), file.get('modifiedTime'),
                                      file.get('lastModifyingUser'), file.get('SharedWithMeTime'),file.get('sharingUser.emailAddress'), file.get('sharingUser.permissionID'),
                                      file.get('id'), file.get('mimeType')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return search_result

    # FILE DOWNLOAD
    def __file_download(self, service, file_id, file_name, mimetype):

        if 'application/vnd.google-apps.' in mimetype:
            request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            fh.seek(0)
            with open(file_name + '.pdf', 'wb') as f:
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
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)

if __name__ == '__main__':
    TOKEN_FILE = 'credentials.json'
    PORT = 1234
    SCOPES = ['https://www.googleapis.com/auth/drive']
    g_drive = GDrive(TOKEN_FILE, PORT, SCOPES)

    while True:
        select = input('1. get all of file\n'
                       '2. search file with keyword\n'
                       'Select number: ')
        if select == '1':
            g_drive.no_search()
        elif select == '2':
            while True:
                tmp = input('***********************************\n'
                            '1. Settings Files modified after a given date\n'
                            '2. No period\n'
                            'period input example: 20212-06-04T00:00:00\n'
                            'Select number: ')

                if tmp == '1':
                    g_drive.search_with_period()
                elif tmp =='2':
                    g_drive.search()
