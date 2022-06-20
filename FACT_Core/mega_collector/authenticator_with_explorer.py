"""
============================================
    "authenticator_with_explorer" Module
============================================
.. moduleauthor:: Siyoon Kim <kim_3738@korea.ac.kr>

.. note::
    'TITLE'             : MEGA - Authenticator and Explorer in AF-Forensics\n
    'AUTHOR'            : Siyoon Kim\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.1\n
    'RELEASE-DATE'      : 2022-06-17\n

--------------------------------------------

Description
===========

    MEGA Cloud 수집에 필요한 인증 및 파일 목록, 메타데이터 수집 하는 모듈

    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부

History
===========

    * 2022-06-17 : 초기 버전

"""

from module.FACT_Cloud_Define import *

class Authentication_with_Exploration:
    def __init__(self, credential):
        self.__id = credential[0]
        self.__password = credential[1]
        self.__mega = Mega()
        self.__m = None
        self.__file_list = None
        self.__account_data = None

    def run(self):
        if self.__login() == FC_ERROR:
            return FC_ERROR

        if self.__set_account_data() == FC_ERROR:
            return FC_ERROR

        if self.__set_file_list() == FC_ERROR:
            return FC_ERROR
        return FC_OK


    def __login(self):
        try:
            self.__m = self.__mega.login(self.__id, self.__password)
        except:
            return FC_ERROR
        return FC_OK


    def __set_account_data(self):
        self.__account_data = self.__m.get_user()
        if len(self.__account_data) == 0:
            return FC_ERROR
        return FC_OK

    def __set_file_list(self):
        self.__file_list = self.__m.get_files()
        if len(self.__file_list) == 0:
            return FC_ERROR
        return FC_OK

    def get_file_list(self):
        return self.__file_list

    def get_account_data(self):
        return self.__account_data

    def get_m(self):
        return self.__m