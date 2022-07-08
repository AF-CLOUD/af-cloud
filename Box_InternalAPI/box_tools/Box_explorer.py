import json
import requests
import re
import datetime
from tabulate import tabulate
import os
class user_menu:
    def __init__(self, cookie, printlist, parsing_dt, request_token):
        self.cookie = cookie
        self.metajson = parsing_dt
        self.request_token = request_token
        self.trashsearchlist=[]
        self.searchlist=[]
        self.printlist = printlist

# to.. 미래의 나 -> download url에 뭐 있는 경우 바로 request

    def __f_dload_fid(self):
        fid = input("다운로드할 파일의 아이디를 입력하세요(note제외) :")
        if fid =="0":
            print("선택을 취소하고 이전메뉴로 돌아갑니다. ")
            return 0
        data = {
            'request_token': self.request_token,
        }
        
        params = {
            'rm': 'box_v2_download_file',
            'file_id': fid,
        }
        res = requests.post(url='https://app.box.com/index.php', data=data, cookies=self.cookie, params=params,verify=False)
        if not os.path.exists(".downloads"):
            os.makedirs(".downloads")
        with open(fid,'wb') as f:
            f.write(res.content)

        print("file download success, f id : ", fid)

    def __f_dload(self):
        select_n = input("다운로드할 파일의 번호를 선택하세요 : ")
        print(self.metajson[int(select_n)]["id"],"파일 수집 중...")
        fid = self.metajson[int(select_n)]["id"]

        if self.metajson[int(select_n)]["download url"]:
            its="notes"
        else:
            data = {
                'request_token': self.request_token,
            }
            
            params = {
                'rm': 'box_v2_download_file',
                'file_id': fid,
            }
            res = requests.post(url='https://app.box.com/index.php', data=data, cookies=self.cookie, params=params,verify=False)
            name = self.metajson[int(select_n)]["name"]
            if not os.path.exists(".downloads"):
                os.makedirs(".downloads")
            with open(".downloads/"+name,'wb') as f:
                f.write(res.content)

            print("파일 수집 완료, f id : ", fid)

    def __search(self):
        #검색
        updatedTimeTo=""
        updatedTimeFrom=""
        self.searchlist=[]
        tempsearchlist=[]
        query = input("검색할 단어 : ")
        print("선별 검색을 원하지 않을 경우 엔터를 입력하세요. ")
        kinds = input("검색할 영역 ex.file_content, name, comments, description, file_content, tags : \n")
        print("types 검색 ex. pdf, file, folder, audio, boxnote, document, drawing, image, spreadsheet, presentation, video : \n")
        print("types 는 두 가지 이상 검색이 가능합니다. 두 가지 이상일 경우 types사이에 %2C를 넣어주세요. ex. audio%2Cboxnote : \n")
        types =input("검색할 포맷 입력 : \n") 
        print("기간검색 : ex. 하루: 1, 1년 : 365, 기간검색 : customrange  : ")
        updatedTime =input()
        if updatedTime =="customrange":
            updatedTimeFrom = input("기간 검색(마지막으로 수정한 날짜) 시작 시간 : ")
            updatedTimeTo = input("기간 검색(마지막으로 수정한 날짜) : ")
            updatedTimeFrom=str(int(datetime.datetime.strptime(updatedTimeFrom,'%Y-%m-%d').timestamp()*1000))
            updatedTimeTo=str(int(datetime.datetime.strptime(updatedTimeTo,'%Y-%m-%d').timestamp()*1000))

        # isTrashSearch =input("휴지통 검색시 : 1, 일반 파일 검색시 : 0") : 둘다 개발!
        url_notrash = "https://app.box.com/folder/0/search?query="+query+"&isTrashSearch=0&kinds="+kinds+"&types="+types+"&updatedTime="+updatedTime+"&updatedTimeTo="+updatedTimeTo+"&updatedTimeFrom="+str(updatedTimeFrom)
        url_trash =  "https://app.box.com/folder/0/search?query="+query+"&isTrashSearch=1&kinds="+kinds+"&types="+types+"&updatedTime="+updatedTime+"&updatedTimeTo="+updatedTimeTo+"&updatedTimeFrom="+str(updatedTimeFrom)

        
        response_notrash = requests.get(url_notrash, cookies=self.cookie, verify=False)
        response_trash = requests.get(url_trash, cookies=self.cookie, verify=False)
        split_data = "Box.postStreamData = (.+?)searchItems"

        string1 = re.search(split_data, str(response_notrash.content)).group(1) 
        string2 = re.search(split_data, str(response_trash.content)).group(1)
        string1 = string1[:-2]+"}}"
        string2 = string2[:-2]+"}}"
        notrash_searchjson= json.loads(string1)
        trash_searchjson= json.loads(string2)
        root = "\/app-api\/enduserapp\/folder\/0\/search"
        notrashjsonlen = len(notrash_searchjson[root]["items"])
        trashjsonlen = len(trash_searchjson[root]["items"])

        for num in range(notrashjsonlen):
            name = notrash_searchjson[root]["items"][num]["name"]
            name = name.encode('utf-8').decode('unicode-escape')
            id = notrash_searchjson[root]["items"][num]["id"]
            date = notrash_searchjson[root]["items"][num]["date"]
            lastupdatedByname = notrash_searchjson[root]["items"][num]["lastUpdatedByName"]
            contentupdated = notrash_searchjson[root]["items"][num]["contentUpdated"]
            testsearch=[name, id, date, lastupdatedByname, contentupdated]
            self.searchlist.append(testsearch)
            tempsearchlist.append(testsearch)
        print(tabulate(tempsearchlist, headers =["name", "id", "date", "lastUpdateUser",  "contentUpdated_date"]))
        print("----------------------------------------------------------------------------------")
        # for num in range(trashjsonlen):
        #     name = trash_searchjson[root]["items"][num]["name"]
        #     id = trash_searchjson[root]["items"][num]["id"]
        #     deldate = trash_searchjson[root]["items"][num]["deletedFromTrash"]
        #     deletedby = trash_searchjson[root]["items"][num]["deletedBy"]

        #     testsearch=[name, id, deldate, deletedby]
        #     self.trashsearchlist.append(testsearch)
        # print("In Trash : \n")
        # print(tabulate(self.searchlist, headers=["name", "id", "deldate", "deletedby"]))
 


    def __showlist(self):
        print(tabulate(self.printlist, headers = ["name", "file ID", "path", "size", "extension", "server_ctime", "lastmod_user", "version_count", "version_num", "owner", "sha1"], tablefmt='github', showindex=True, numalign="left"))





    def __explorer(self):
        print("###########################")
        print("######### M.E.N.U #########")
        print("###########################")
        print("#    0. EXIT              #")
        print("#    1. SHOW_FILE_LIST    #")
        print("#    2. SEARCH_FILE       #")
        print("#    3. FILE_DOWNLOAD     #")
        num1 = input("Select Menu : ")
        return num1


    def main_explorer(self):
        while True:
            menu = self.__explorer()
            if menu == "0":
                break
            elif menu =="1":
                self.__showlist()
            elif menu =="2":
                self.__search()
            elif menu=="3":
                while True:
                    print("수집 방법을 선택하세요. ")
                    print("0. 메뉴로 돌아가기")
                    print("1. 인덱스로 파일 수집")
                    print("2. 파일 아이디로 파일 수집")
                    select = input()
                    if select=="0":
                        break
                    elif select=="1":
                        self.__f_dload()
                    elif select=="2":
                        self.__f_dload_fid()
                    else :
                        print("잘못누르셨습니다. 다시 입력하세요. ")



