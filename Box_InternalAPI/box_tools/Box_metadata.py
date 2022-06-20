import json
import requests
import os

class file_metadata:
    def __init__(self, z, path):
        self.cookie = z
        self.path = path
        
    def sidebar(self):
        url =""

    def making_json(self, name):
        root = "/app-api/enduserapp/folder/"+name
        self.metajson["items"]=name
        print(str(self.jsondata[root]["items"]["id"]))
        self.metajson["items"]["id"]=self.jsondata[root]["items"]["id"]
        fpath = ""
        for i in range(len(self.jsondata[root]["folder"]["path"])):
            fpath += self.jsondata[root]["folder"]["path"]["name"]
        print(fpath)
        # self.metajson["items"]["path"]=self.jsondata[root]["folder"]["path"]
        


    def get_filelist(self):
        for (path, dir, files) in os.walk(self.path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext =='.txt':
                    fullpath = path+"\\"+filename
                    with open(fullpath,'r') as fl:
                        name = os.path.splitext(filename)[0]
                        flist =  fl.read()
                        self.jsondata = json.loads(flist)
                        self.metajson = dict()
                        self.making_json(name)


    def get_metadata(self):
        self.get_filelist()
        # url1 = "https://app.box.com/app-api/enduserapp/file/"+f_id+"/sidebar"

        # url2= "https://app.box.com/app-api/enduserapp/folder/0/items"
