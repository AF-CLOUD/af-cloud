"""
============================================
    "collector" Module
============================================
.. moduleauthor:: Seung Ah Kang <kyn0503121@korea.ac.kr>
.. note::
    'TITLE'             : Box - Collector in AF-Forensics\n
    'AUTHOR'            : Seung Ah Kang\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.1\n
    'RELEASE-DATE'      : 
--------------------------------------------
Description
===========
    Box Open APIs 를 사용해서 원하는 기능을 제공하는 모듈
    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부
History
===========
"""


from tabulate import tabulate
from this import d
import os
from module import FACT_Cloud_Define

class Collector:
    def __init__(self, auth_data, box_data):
        self.__box=box_data
        self.__auth_data = auth_data

    def get_num_of_file_list(self):
        return len(self.__box)

    def search_file(self, q):
        search_result=[]
        search_response = None

    def download_file(self, file_num):
        file_name = self.__box[file_num-1][1]
        file_id = self.__box[file_num-1][2]
        try : 
            if not (os.path.isdir('./download')):
                os.makedirs('./download')

            with open('./download/'+file_name,'wb') as f:
                # f.write(file_content)
                # file_content=self.__auth_data.download_to(file_num).content()
                file_content=self.__auth_data.file(file_id).download_to(f)
            print("Download " +file_name+" Done !")
            FACT_Cloud_Define.PRINTI("Download " +file_name+" Done")
        except:
            FACT_Cloud_Define.PRINTE("Download " +file_name+" error !")
            print("Download " +file_name+" error !")

    def show_file_list(self):
        print("======BOX_FILE_LIST======")
        print(tabulate(self.__box, headers=["num", "Name", "ID", "Content_created_at", "Content_modified_at", "Created_at", "Modified_at", "Created_by_name", "Created_by_email", "Description", "Version_count", "File_version_id", "Owned_by_email", "Owned_by_name", "Path", "Purged_at", "SHA1", "Size", "Trashed_at", "Path"], tablefmt='github', showindex=False, numalign="left"))





