"""
============================================
    "collector" Module
============================================
.. moduleauthor:: Ho Yoon<ymaul2@korea.ac.kr>

.. note::
    'TITLE'             : Dropbox - Collector in AF-Forensics\n
    'AUTHOR'            : Ho Yoon\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.4\n
    'RELEASE-DATE'      : 2022-06-24\n

--------------------------------------------

Description
===========

    OneDrive Internal APIs 를 사용해서 원하는 기능을 제공하는 모듈

    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부

History
===========

    * 2022-06-24 : 초기 버전 - 생성: 파일 목록 추가, 파일 다운로드 추가, 파일 버전 정보 수집 추가, 파일 버전 다운로드 추가

    * 해야할 일들 : 검색 기능

"""

from dropbox_collector.explorer import *

class Collector:
    def __init__(self, dropbox_data, auth_data):
        self.__dropbox = dropbox_data
        self.__auth_data = auth_data

    def file_download(self, file_list, cookies):
        downloadble_file = []  # 삭제된 파일(메타데이터상 파일 크기가 "-1") 제외한 다운로드 가능한 파일 리스트, 파일별 메타데이터 정보 포함
        if not os.path.exists("./Download"):
            os.mkdir("./Download")

        for i in range(len(file_list)):
            if file_list[i][2] > 0:  # 크기가 "-1"이면 삭제된 파일
                downloadble_file.append(file_list[i])

        for i in range(len(downloadble_file)):
            print("[%d]" % (i + 1), downloadble_file[i][1])

        to_download = int(input("\n[System] >>> Type the number of file you wish to download: "))
        print("[System] >>> File: [%s] selected. Please wait" % downloadble_file[(to_download - 1)][1])
        print("[System] >>> Downloading...")

        get_param = downloadble_file[(to_download - 1)][3]  # 파일별 메타데이터 중 다운로드에 필요한 Param값인 "subject_uid" 및 "w" 획득

        s_filter = re.compile('(=)(.*?)(&w)')
        subject_uid = s_filter.findall(get_param)
        w_filter = re.compile('(w=)(.*?)($)')
        w = w_filter.findall(get_param)

        params = {
            '_notify_domain': 'www.dropbox.com',
            '_subject_uid': subject_uid[0][1],
            'w': w[0][1],
        }

        url = "https://www.dropbox.com/pri/get" + downloadble_file[(to_download - 1)][1] + "?"
        response = requests.get(url, params=params, cookies=cookies, verify=False)

        filename = downloadble_file[(to_download - 1)][1]
        finalname = filename.replace("/", "_")

        with open('Download/%s' % finalname, 'wb') as f:
            f.write(response.content)

        print("[System] >>> Download Completed")

    def file_revisions_download(self, revisionable_file, cookies):
        print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡList of Files with revisionsㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
        for i in range(len(revisionable_file)):
            print("[%d]" % (i + 1), revisionable_file[i][0][1])  # List of revisionable Files
        if not os.path.exists("./Revision"):
           os.mkdir("./Revision")

        to_download = int(input("\n[System] >>> Type the number of file you wish to download: "))
        print("[System] >>> Downloading Revisions of [%s] ..." % revisionable_file[to_download - 1][0][1])
        os.mkdir("./Revision/%s" % revisionable_file[to_download - 1][1]["revisions"][0]["filename"])

        for x in range(len(revisionable_file[to_download - 1][1]["revisions"])):
            downloadable_url = "https:" + revisionable_file[to_download - 1][1]["revisions"][x]["preview_info"]["href"]
            s_filter = re.compile('(subject_uid=)(.*?)(&r)')
            subject_uid = s_filter.findall(downloadable_url)
            r_filter = re.compile('(revision_id=)(.*?)(&s)')
            revision_id = r_filter.findall(downloadable_url)
            w_filter = re.compile('(w=)(.*?)($)')
            w = w_filter.findall(downloadable_url)

            params = {
               '_notify_domain': 'www.dropbox.com',
               '_subject_uid': subject_uid[0][1],
               "revision_id": revision_id[0][1],
               "source": "_private_jsinfo_helper",
               'w': w[0][1],
            }

            url = "https://www.dropbox.com/pri/get" + revisionable_file[to_download-1][0][1] + "?"
            response = requests.get(url, params=params, cookies=cookies, verify=False)

            with open("Revision/%s/[Ver.%d]%s" % (
            revisionable_file[to_download - 1][1]["revisions"][0]["filename"], (x + 1),
            revisionable_file[to_download - 1][1]["revisions"][0]["filename"]), "wb") as f:
                f.write(response.content)

        print("[System] >>> Download Completed")