# Coding by YES
# Reference: Google

import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None

    # Oauth 인증으로 생성된 token.json 파일의 유무를 확인하는 코드
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Credential.json 파일은 실행하는 .py 파일과 동일한 위치에 있어야 함
        # Credential.json은 Google Cloud Platform API 서비스에서 다운 가능.
        # Oauth 인증은 Desktop client / Web client 두팀으로 나눠서 진행예정
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential_oat.json', scopes=SCOPES)
            creds = flow.run_local_server(port=1517)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

###############################################################

    page_token = None
    # while True:
    #     response = service.files().list(q="not name contains 'test'",
    #                                           spaces='drive',
    #                                           fields='nextPageToken, files(id, name)',
    #                                           pageToken=page_token).execute()
    #     print(response)
    #     for file in response.get('files', []):
    #         # Process change
    #         print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    #     page_token = response.get('nextPageToken', None)
    #     if page_token is None:
    #         break

    # Filelist 뽑기
    while True:
        response = service.files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name, shared, trashed, trashedTime, linkShareMetadata, exportLinks, resourceKey)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            # print('Found file: %s (%s) %s [%s]' % (file.get('name'), file.get('id'), file.get('trashed'), file.get('trashedTime')))
            print('File Shared: %s %s %s %s %s' % (file.get('name'), file.get('shared'), file.get('resourceKey'), file.get('linkShareMetadata'), file.get('exportLinks')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break


    # file_id = '10-DOeFKsnhKy8XmMb_EXc1uaQjWYMoeG'
    # request = service.files().get_media(fileId=file_id)
    # fh = io.FileIO()
    # downloader = MediaIoBaseDownload(fh, request)
    # done = False
    # while done is False:
    #     status, done = downloader.next_chunk()
    #     print("Download %d%%." % int(status.progress() * 100))

if __name__ == '__main__':
    main()