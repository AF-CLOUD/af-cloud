"""
============================================
    "explorer" Module
============================================
.. moduleauthor:: Ho Yoon <ymaul2@korea.ac.kr>

.. note::
    'TITLE'             : Dropbox - Explorer in AF-Forensics\n
    'AUTHOR'            : Ho Yoon\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.4\n
    'RELEASE-DATE'      : 2022-06-24\n

--------------------------------------------

Description
===========

    Dropbox Internal APIs 를 사용해서 Dropbox에 저장된 데이터 파싱하는 모듈

    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부

History
===========

    * 2022-06-24 : 초기 버전 - 생성: 파일 목록 추가, 파일 다운로드 추가, 파일 버전 정보 수집 추가, 파일 버전 다운로드 추가

    * 해야할 일들 : 검색 기능

"""

from dropbox_collector.authenticator_dropbox import *
from tqdm import tqdm

class Exploration:

    def __init__(self, auth_data):
        """
            :param list auth_data: auth_data from authenticator.py
        """
        self.__auth_data = auth_data
        self.__file_list = []
        self.__folder_list = ["/"]
        self.__revisionable_file = []

    def run(self):
        print("[System] >>> Browsing Dropbox...")
        print("[System] >>> Folder Browsing Start!")
        self.__recursive_search_folder("", self.__auth_data.headers(), self.__auth_data.cookies())  # Root Directory부터 재귀적으로 모든 폴더 목록 획득
        print("[System] >>> Done")

        print("\n[System] >>> File Browsing Start!")
        for i in range(len(self.__folder_list)):  # 획득한 폴더 각각을 input으로 해당 폴더에 존재하는 파일 목록 획득
            self.__recursive_search_file(self.__folder_list[i], self.__auth_data.headers(), self.__auth_data.cookies())
        print("[System] >>> Done")

        print("\n[System] >>> File Revisions Browsing Start!")
        self.__file_revision(self.__auth_data.headers(), self.__auth_data.cookies())
        print("[System] >>> Done")

        print("\n[System] >>> File Thumbnails Browsing Start!")
        #self.__get_thumbnails(self.__auth_data.headers(), self.__auth_data.cookies()) #임시로 꺼둠
        print("[System] >>> Done")

    def __recursive_search_folder(self, fq_path, headers, cookies):
        try:
            data = {"path": fq_path, "max_height": 1, "limit_sub_folder_count": 150}
            response = requests.post('https://www.dropbox.com/2/files/list_subfolders', headers=headers,
                                     cookies=cookies, data=json.dumps(data), verify=False)

            result = json.loads(response.content)

            if len(result['subfolder_entries']) != 0:
                for i in range(len(result['subfolder_entries'])):
                    self.__folder_list.append(result['subfolder_entries'][i]['folder_metadata']['path_display'])
                    self.__recursive_search_folder(result['subfolder_entries'][i]['folder_metadata']['path_display'], headers, cookies)
                    # 해당 폴더에 하위 폴더가 존재하는 경우 재귀적으로 조회

            else:
                flag = 0

        except:
            return FC_ERROR

        return FC_OK

    def __recursive_search_file(self, fq_path, headers, cookies):
        try:
            path = {"fq_path": fq_path, "include_deleted": True, "sort_type": {".tag": "files_by_name"},
                    "sort_is_ascending": True}
            response = requests.post('https://www.dropbox.com/2/files/browse', headers=headers, cookies=cookies,
                                     data=json.dumps(path), verify=False)
            result = json.loads(response.content)
            file_folder = []  # input으로 주어진 경로(fq_path/folder)에 존재하는 모든 파일/폴더가 담기는 리스트

            for i in tqdm(range(len(result['paginated_file_info']))):
                file_folder.append([result['paginated_file_info'][i]['file_info']['type'][".tag"],
                                    result['paginated_file_info'][i]['file_info']['fq_path'],
                                    result['paginated_file_info'][i]['file_info']['size_bytes'],
                                    result['paginated_file_info'][i]['file_info']['direct_blockserver_link'],
                                    result['paginated_file_info'][i]['file_info']['file_id'],
                                    result['paginated_file_info'][i]['file_info']['ns_id'],
                                    result['paginated_file_info'][i]['file_info']['sjid'],
                                    result['paginated_file_info'][i]['file_info']['ext']])
                # 필요한 메타 정보만 가공한 최종 형태: [type][fq_path][size][link][file_id][ns_id][sjid][ext] - 필요에 따라 보완 예정

            for x in tqdm(range(len(file_folder))):  # Type이 폴더는 제외한 파일만 가공하는 과정
                if file_folder[x][0] == "file":
                    self.__file_list.append(file_folder[x])

            if result['has_more'] == True:  # 해당 경로에 파일이 30개 이상인경우 별도 처리
                cursor = {}
                path_continue = result['next_request_voucher']
                cursor["cursor"] = path_continue
                self.__recursive_search_file_continue(headers, cookies, cursor)  # 커서값과 함께 담당 재귀함수로 전달

        except:
            return FC_ERROR

        return FC_OK

    def __recursive_search_file_continue(self, headers, cookies, cursor):
        try:
            file_folder_continue = []

            response_continue = requests.post('https://www.dropbox.com/2/files/browse_continue', headers=headers,
                                              cookies=cookies, data=json.dumps(cursor), verify=False)

            result_continue = response_continue.content
            result_continue_json = json.loads(result_continue)

            for i in tqdm(range(len(result_continue_json['paginated_file_info']))):
                file_folder_continue.append([result_continue_json['paginated_file_info'][i]['file_info']['type'][".tag"],
                                    result_continue_json['paginated_file_info'][i]['file_info']['fq_path'],
                                    result_continue_json['paginated_file_info'][i]['file_info']['size_bytes'],
                                    result_continue_json['paginated_file_info'][i]['file_info']['direct_blockserver_link'],
                                    result_continue_json['paginated_file_info'][i]['file_info']['file_id'],
                                    result_continue_json['paginated_file_info'][i]['file_info']['ns_id'],
                                    result_continue_json['paginated_file_info'][i]['file_info']['sjid'],
                                    result_continue_json['paginated_file_info'][i]['file_info']['ext']])
                                    #필요한 메타 정보만 가공한 최종 형태: [type][fq_path][size][link][file_id][ns_id][sjid] - 보완 예정

            for x in tqdm(range(len(file_folder_continue))): #Type이 폴더는 제외한 파일만 가공하는 과정
                if file_folder_continue[x][0] == "file":
                    self.__file_list.append(file_folder_continue[x])

            if result_continue_json["has_more"] == True: #여전히 불러올 파일 목록이 있는 경우
                cursor_continue = {}
                cursor_continue["cursor"] = result_continue_json["next_request_voucher"]
                self.__recursive_search_file_continue(headers, cookies, cursor_continue) #cursor값과 함께 재귀적으로 처리

        except:
            return FC_ERROR

        return FC_OK

    def __file_revision(self, headers, cookies):
        try:
            revisionable_file_check = []
            revisionable_ext = [".docx", ".pptx", ".xlsx"]

            for i in range(len(self.__file_list)):
                if self.__file_list[i][2] > 0:  # 크기가 "-1"이면 삭제된 파일
                    if self.__file_list[i][7] in revisionable_ext:
                        revisionable_file_check.append(self.__file_list[i])

            param = {
                '_subject_uid': headers['X-Dropbox-Uid'],
                'undelete': '1',
            }

            for i in range(len(revisionable_file_check)):
                print("[System] >>> Checking Revisions of [%s] ..." % revisionable_file_check[i][1])
                url = "https://www.dropbox.com/history" + revisionable_file_check[i][1]
                response = requests.get(url, params=param, cookies=cookies, headers=headers, verify=False)
                revision_content = str(response.content)
                rev_filter = re.compile('("revisions": )(.*?)(, "cursor")')
                rev_filtered = rev_filter.findall(revision_content)
                make_json = '{"revisions": ' + rev_filtered[0][1] + "}"
                encoder = make_json.replace("\\\\", "\\")
                revision = json.loads(encoder)
                # print(revision)
                if len(revision["revisions"]) != 1:
                    self.__revisionable_file.append([revisionable_file_check[i], revision])

        except:
            return FC_ERROR

        return FC_OK

    def get_revisionable_file(self):
        return self.__revisionable_file

    def __get_thumbnails(self, headers, cookies):
        try:
            print("[System] >>> Getting thumbnail data...")
            previewable_file = []  # 삭제된 파일(메타데이터상 파일 크기가 "-1") 제외한 다운로드 가능한 파일 리스트, 파일별 메타데이터 정보 포함
            if not os.path.exists("./Thumbnail"):
                os.mkdir("./Thumbnail")

            for i in range(len(self.__file_list[0:30])):
                if self.__file_list[i][2] > 0:  # 크기가 "-1"이면 삭제된 파일
                    previewable_file.append(self.__file_list[i])

            preview_list = []
            preview_video = []
            preview_ssr_doc = []
            preview_image = []
            count = 0
            repeat = int(len(previewable_file) / 30)  # file이 전체 2000개라면, 30번씩 처리하기위한 반복횟수. 즉, 66번(66*30 = 1980)

            # 만약 2000개라면, 30번씩 66번하면 1980개이고, 나머지 20개가 남기에 이를 위한 코드
            for i in range(repeat * 30):  # 1980개 0부터 1979까지
                count += 1  # 1,2,3,...30
                if count % 30 != 0:  # i가 29일때(30번째일때) count는 30임 고로 여기로 안옴
                    form = {"ns_id": previewable_file[i][5], "sj_id": previewable_file[i][6]}
                    preview_list.append(form)

                if count % 30 == 0:  # preview_list에 form이 30개 쌓였다면
                    form = {"ns_id": previewable_file[i][5], "sj_id": previewable_file[i][6]}
                    preview_list.append(form)
                    data = {"files": preview_list}
                    response = requests.post('https://www.dropbox.com/2/previews/get_preview_data_batch',
                                             cookies=cookies,
                                             headers=headers, data=json.dumps(data), verify=False)
                    preview_list = []  # 초기화
                    result = json.loads(response.content)

                    for x in range(len(result["results"])):
                        if "preview" in result["results"][x]:
                            if result["results"][x]["preview"]["content"][".tag"] == "video":
                                preview_video.append([result["results"][x]["file"]["sj_id"],
                                                      result["results"][x]["preview"]["content"]["poster_url_tmpl"]])
                            if result["results"][x]["preview"]["content"][".tag"] == "ssr_doc":
                                preview_ssr_doc.append([result["results"][x]["file"]["sj_id"],
                                                        result["results"][x]["preview"]["content"]["image_url_tmpl"]])
                            if result["results"][x]["preview"]["content"][".tag"] == "image":
                                preview_image.append([result["results"][x]["file"]["sj_id"],
                                                      result["results"][x]["preview"]["content"]["default_src"]])

            for y in range(repeat * 30, len(previewable_file)):
                form = {"ns_id": previewable_file[y][5], "sj_id": previewable_file[y][6]}
                preview_list.append(form)
                data = {"files": preview_list}
                response = requests.post('https://www.dropbox.com/2/previews/get_preview_data_batch', cookies=cookies,
                                         headers=headers, data=json.dumps(data), verify=False)
                result = json.loads(response.content)

                for z in range(len(result["results"])):
                    if "preview" in result["results"][z]:
                        if result["results"][z]["preview"]["content"][".tag"] == "video":
                            preview_video.append([result["results"][z]["file"]["sj_id"],
                                                  result["results"][z]["preview"]["content"]["poster_url_tmpl"]])
                        if result["results"][z]["preview"]["content"][".tag"] == "ssr_doc":
                            preview_ssr_doc.append([result["results"][z]["file"]["sj_id"],
                                                    result["results"][z]["preview"]["content"]["image_url_tmpl"]])
                        if result["results"][z]["preview"]["content"][".tag"] == "image":
                            preview_image.append([result["results"][z]["file"]["sj_id"],
                                                  result["results"][z]["preview"]["content"]["default_src"]])

            print("[System] >>> Collecting the thumbnail of video files...")
            for ii in tqdm(range(len(preview_video))):
                t_response = requests.get(preview_video[ii][1], cookies=cookies, headers=headers, verify=False)
                for xx in range(len(self.__file_list)):
                    if preview_video[ii][0] == self.__file_list[xx][6]:  # sj_id == sj_id
                        t_video_filename = self.__file_list[xx][1]  # fq_path
                        if t_response.status_code == 200:
                            t_video_finalname = t_video_filename.replace("/", "_")
                            with open('Thumbnail/%s' % t_video_finalname + ".jpg", 'wb') as f:
                                f.write(t_response.content)
                        else:
                            print("Check:", t_video_filename, preview_video[ii])
            print("[System] >>> Video Files - Done")

            print("[System] >>> Collecting the thumbnail of document files...")
            for yy in tqdm(range(len(preview_ssr_doc))):
                t_response = requests.get(preview_ssr_doc[yy][1], cookies=cookies, headers=headers, verify=False)
                for zz in range(len(self.__file_list)):
                    if preview_ssr_doc[yy][0] == self.__file_list[zz][6]:  # sj_id == sj_id
                        t_doc_filename = self.__file_list[zz][1]  # fq_path
                        if t_response.status_code == 200:
                            t_doc_finalname = t_doc_filename.replace("/", "_")
                            with open('Thumbnail/%s' % t_doc_finalname + ".jpg", 'wb') as f:
                                f.write(t_response.content)
                        else:
                            print("Check:", t_doc_filename, preview_ssr_doc[yy])
            print("[System] >>> Document Files - Done")

            print("[System] >>> Collecting the thumbnail of image files...")
            for aa in tqdm(range(len(preview_image))):
                t_response = requests.get(preview_image[aa][1], cookies=cookies, headers=headers, verify=False)
                for bb in range(len(self.__file_list)):
                    if preview_image[aa][0] == self.__file_list[bb][6]:  # sj_id == sj_id
                        t_image_filename = self.__file_list[bb][1]  # fq_path
                        if t_response.status_code == 200:
                            t_image_finalname = t_image_filename.replace("/", "_")
                            with open('Thumbnail/%s' % t_image_finalname + ".jpg", 'wb') as f:
                                f.write(t_response.content)
                        else:
                            print("Check:", t_image_filename, preview_image[aa])

            print("[System] >>> Image Files - Done")
        except:
            return FC_ERROR

        return FC_OK

    def get_file_list(self):
        return self.__file_list
