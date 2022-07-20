"""
============================================
    "explorer" Module
============================================
.. moduleauthor:: Seung Ah Kang <kyn0503121@korea.ac.kr>
.. note::
    'TITLE'             : Box - Explorer in AF-Forensics\n
    'AUTHOR'            : Seung Ah Kang\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.1\n
    'RELEASE-DATE'      : 
--------------------------------------------
Description
===========
    Box Internal APIs 를 사용해서 Box에 저장된 데이터 파싱하는 모듈
    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부
"""
import os
class Exploration:
    def __init__(self, auth_data):
        self.auth_data = auth_data
        self.print_list = []
        self.k=1

    def __parsing_mt(self, client, item, trash_flag):
        file_info=None
        if trash_flag:
            file_to_retrieve = client.file(file_id=item.id)
            file_info = client.trash().get_item(file_to_retrieve)
        else:
            file_info = client.file(item.id).get()
        f_name = file_info.name
        f_id = file_info.id
        content_created_at = file_info.content_created_at
        content_modified_at = file_info.content_modified_at
        created_at = file_info.created_at
        modified_at = file_info.modified_at
        # print("created by : "+file_info.created_by["name"])
        created_by_name = file_info.created_by["name"]
        created_by_email = file_info.created_by["login"]
        description = file_info.description
        version_count = item.etag
        file_version_id = file_info.file_version["id"]
        file_version_sha1 = file_info.file_version["sha1"]
        owned_by_email = file_info.owned_by["login"]
        owned_by_name = file_info.owned_by["name"]
        path = file_info.parent
        purged_at = file_info.purged_at
        sha1 = file_info.sha1

        # shared_link = file_info.shared_link["download_url"]
        # unshared_at = file_info.unshared_at
        size = file_info.size
        trashed_at = file_info.trashed_at
        # print(f_name, f_id, content_created_at, content_modified_at, created_at, modified_at, created_by_name, created_by_email, description, file_version_id, file_version_sha1, owned_by_email, owned_by_name, path, purged_at, sha1, shared_link, unshared_at, size, trashed_at)
        path = []
        for i in range(len(file_info.path_collection["entries"])):
            # print(i, file_info.path_collection["entries"][i]["name"])
            path.append(file_info.path_collection["entries"][i]["name"])
        path = "/".join(path)
        templist = [self.k, f_name, f_id, content_created_at, content_modified_at, created_at, modified_at, created_by_name, created_by_email, description, version_count, file_version_id, owned_by_email, owned_by_name, path, purged_at, sha1, size, trashed_at, path]
        print(templist)
        self.k+=1
        self.print_list.append(templist)

    def __get_thumb(self, client, item):
        thumbnail = client.file(item.id).get_thumbnail_representation('320x320', extension='jpg')
        if len(thumbnail):
            with open(".thumbnail/"+str(item.id)+".jpg", 'wb') as f:
                f.write(thumbnail)

    def __explorer_folder(self, client, folder_id):
        root_folder = client.folder(folder_id).get()
        # print("debug log : the root folder is owned by : {0}".format(root_folder.owned_by['login']))
        items = root_folder.get_items()
        # print("debug log : in the root folder : ")
        for item in items : 
            # print(item.name, item.type, item.id)
            if item.type=="folder":
                self.__explorer_folder(client, item.id)

            else : 
                self.__parsing_mt(client, item, 0)
                # self.__get_thumb(client,item)
                pass
    
    def __in_trash_folder(self, folder_id):
        self.auth_data.folder(folder_id=folder_id)

    def __explorer_trash_folder(self):
        trash_folder = self.auth_data.trash().get_items()
        for trash_item in trash_folder:
            if trash_item.type=='folder':
                self.__in_trash_folder
            else : 
                self.__parsing_mt(self.auth_data, trash_item, 1)
                
    def run(self):
        print("Box Exploration Strart ! ")
        if not os.path.exists(".thumbnail"):
            os.makedirs(".thumbnail")
        self.__explorer_folder(self.auth_data, '0')
        self.__explorer_trash_folder()
        return self.print_list


    