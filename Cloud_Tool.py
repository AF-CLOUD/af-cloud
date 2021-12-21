"""
============================================
    "Cloud_Tool" Module
============================================
.. note::
    'TITLE'             : [Police-Lab 2.0] Research on Data Acquisition and Analysis for Counter Anti-Forensics\n
    'TEAM'              : Korea Univ. DFRC\n
    'VERSION'           : \n
    'RELEASE-DATE'      : 2021-\n

--------------------------------------------

Member
===========


"""
import os
import argparse
import Cloud_Display as display
from GoogleDrive import GDrive
from Cloud_Output import Export

def Tool_Argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store", dest="cred", type=str, default=os.path.abspath(os.path.dirname(__file__)) + os.sep + "credentials.json", required=False, help="credential file path")
    parser.add_argument("-e", action="store", dest="export", type=str, default=os.path.abspath(os.path.dirname(__file__)) + os.sep + "export", required=False, help="csv export path")
    parser.add_argument("-d", action="store", dest="download", type=str, default=os.path.abspath(os.path.dirname(__file__)) + os.sep + "extract", required=False, help="file download path")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    argv = Tool_Argument()
    display.start_tool()
    # 로그인 정보 입력
    # display.login_data()

    cloud_type = display.select_cloud()
    if cloud_type == "1": # Google Drive
        try:
            TOKEN_FILE = argv.cred
            PORT = 3377
            SCOPES = ['https://www.googleapis.com/auth/drive']

            gdrive = GDrive(argv.download, TOKEN_FILE, PORT, SCOPES)
            result = gdrive.run()
            for cnt, info in enumerate(result, start=1):
                export = Export(argv.export, "GDrive_search_" + str(cnt))
                export.input_dict(info)
            print(" [*] Export csv")

        except Exception as e:
            print(" [-] Failed to execute; ", e)
    elif cloud_type == "2" or cloud_type == "3" or cloud_type == "4" or cloud_type == "5":
        pass
    else:
        print(" [!] You CAN input number range(1 ~ 5). Try Again.")





