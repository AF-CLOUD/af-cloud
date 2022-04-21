from audioop import add
import json
import requests
import re 
import csv
import os
class get_file_list:
    def __init__(self, string, cookies):
        self.string = string
        self.jsondata =""
        self.cookies = cookies


    def parsing_file_list(self, string, root):
        r = re.compile("Box.postStreamData")
        string2 = "".join(filter(r.search, string))
        string2 = string2.split("Box.postStreamData = ")
        folder_list = json.loads(string2[-1])
        folder_itemcount  = folder_list[root]["folderItemCount"]
        folder_lencount = len(folder_list[root]["items"])
        return folder_list, folder_itemcount, folder_lencount

    def next_page(self, url, root, itemcount, file_list):
        res = requests.get(url, cookies=self.cookies)
        split_data = "folderItemCount\":"+str(itemcount)+",\"items\":(.+?),\"pageCount\":"
        add_string = re.search(split_data,str(res.content)).group(1)
        add_string = json.loads(add_string)
        len_addsring = len(add_string)
        for i in range(0,len_addsring):
            file_list[root]["items"].append(add_string[i])
            i+=1
        return file_list

    def next_page_folder(self, url, root, itemcount, file_list):
        res = requests.get(url, cookies=self.cookies)
        split_data = "folderItemCount\":"+str(itemcount)+",\"items\":(.+?),\"nextMarker\":"
        add_string = re.search(split_data,str(res.content)).group(1)
        add_string = json.loads(add_string)
        len_addsring = len(add_string)
        for i in range(0,len_addsring):
            file_list[root]["items"].append(add_string[i])
            i+=1
        return file_list

    def folder_file_list(self, url, root):
        res = requests.get(url, cookies=self.cookies)
        folder_list, folder_itemcount, folder_lencount = self.parsing_file_list(res.text.split(';'), root)
        print(folder_lencount, folder_itemcount)
        return folder_list, folder_itemcount, folder_lencount

    def check_type(self, i):
        folder_list={}
        if i["type"]=="folder":
            url = "https://app.box.com/folder/"+str(i["id"])
            root = "/app-api/enduserapp/folder/"+str(i["id"])
            folder_list, folder_itemcount, folder_lencount = self.folder_file_list(url, root)
            if folder_itemcount>folder_lencount:
                folder_list = self.next_page_folder(url, root, folder_itemcount, folder_list)
            path = folder_list[root]["folder"]["path"]
            s_path = "0\\"
            for j in range(0,len(path)):
                s_path +=path[j]['name']+"\\"
                print(s_path)

            if not os.path.exists(str(s_path)):
                os.makedirs(str(s_path))
            with open(s_path + str(i["id"])+".txt",'w') as f:
                json.dump(folder_list, f)   

            for j in folder_list[root]["items"]: 
                folder_list = self.check_type(j)
            return folder_list

    def file_list(self):
        root = "/app-api/enduserapp/folder/0"
        self.jsondata, itemcount, lencount = self.parsing_file_list(self.string, root)

        while itemcount>lencount:
            url = "https://app.box.com/app-api/enduserapp/folder/0?itemOffset="+str(lencount-1)
            self.jsondata = self.next_page(url, root, itemcount, self.jsondata)
            lencount = len(self.jsondata["/app-api/enduserapp/folder/0"]["items"])
            
            print("len count : ", lencount)
        print("루트 총 파일, 폴더 수 : ", lencount-1)

        if not os.path.exists("0"):
            os.makedirs("0")
        with open("0\\0.txt",'w') as f:
            json.dump(self.jsondata, f)  
        for i in  self.jsondata["/app-api/enduserapp/folder/0"]["items"]:
            # self.jsondata.append(self.check_type(i)) #root 조심
            if i["type"]=="folder":
                folder_list = self.check_type(i)
            filename = str(i["id"])+".txt"
        
        return self.jsondata