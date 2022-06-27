"""
============================================
    "Cloud_Core" Module
============================================
.. moduleauthor:: Jieon Kim <kijie@korea.ac.kr>
.. note::
    'TITLE'             : Cloud_Core python file in AF-Forensics\n
    'AUTHOR'            : Jieon Kim\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.3\n
    'RELEASE-DATE'      : 2022-05-18\n

--------------------------------------------

Description
===========

    클라우드 스토리지에 저장된 데이터들 수집하는 도구

    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부

Member
===========

    JE. Kim, YS. Hwang, SA. Kang, JH. Yang, H. Yoon, SY. Kim, WJ. Kwon, JH. Kim

History
===========

    * 2022-05-18 Yang(DFRC): 초기 버전
    * 2022-05-20 Yang(DFRC): OneDrive_connector 추가
    * 2022-06-17 Kim(DFRC): MEGA_connector 추가
    * 2022-06-17 Yoon(DFRC): Dropbox_connector 추가


Method
===========
"""
from onedrive_collector.onedrive_connector import *
from mega_collector.mega_connector import *
from dropbox_collector.dropbox_connector import *
import module.Cloud_Display as cd

class FC_Core():
    """ FC_Core Class
                "Core" Module의 메인 클래스

            >>> "Example Code"
                FC_Core()
        """
    def __init__(self, loglevel=3):
        self.__loglevel = loglevel
        self.__service = None
        self.__connector = None
        self.__credential = None

    def run(self):
        cd.start_tool()

        if self.__set_default() == FC_ERROR:
            PRINTE("FACT Cloud Setting Error")
            return False

        if self.__load_module() == FC_ERROR:
            PRINTE("Load Module Error")
            return False

        if self.__run_module() == FC_ERROR:
            PRINTE("Service Start Error")
            return False

        return True


    def __set_default(self):
        FC_log.set_loglevel(self.__loglevel)
        self.__service = int(cd.select_cloud())
        id, pw = cd.login_data()
        self.__credential = [id, pw]
        return FC_OK

    def __load_module(self):
        if self.__service not in [1, 2, 3, 4, 5]:
            return FC_ERROR

        PRINTI("Connecting.... " + SERVICES[self.__service])

        if self.__service == 1:
            self.__connector = OneDrive_connector()
        elif self.__service == 2:
            self.__connector = OneDrive_connector()
        elif self.__service == 3:
            self.__connector = Dropbox_connector()
        elif self.__service == 4:
            self.__connector = OneDrive_connector()
        elif self.__service == 5:
            self.__connector = MEGA_connector()

        return FC_OK

    def __run_module(self):
        self.__connector.excute(self.__credential)

if __name__ == "__main__":
    a = FC_Core(3)
    a.run()