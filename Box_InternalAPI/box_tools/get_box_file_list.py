import json
import requests
import re 
import os
import time
class get_file_list:
    def __init__(self, string, cookies, request_token):
        self.string = string
        self.jsondata =""
        self.cookies = cookies
        self.request_token = request_token
        self.k=0
        self.metadict = {}
        self.printlist=[]

    def making_json(self, name,fid,  path, size, is_shared, is_trashed, server_ctime, content_ctime, server_mtime, lastmod_user, version_count, version_num, extension, owner, sha1, sharing_user, sharing_email, durl):
        tempjson={"num":self.k, "name":str(name), "id":fid, "path":path, "size":size, "extension":extension, "server Created":server_ctime, "conent Created":content_ctime, "is_shared":is_shared, "lastmodified User":lastmod_user, "version_count":version_count,"version_num":version_num, "owner":owner, "sha1":sha1, "sharing_user":sharing_user, "sharing_email":sharing_email, "download url":durl}
        templist =[name, fid, path, size, extension, server_ctime, lastmod_user, version_count, version_num, owner, sha1]
        self.printlist.append(templist)
        self.metadict[self.k]=tempjson
        self.k+=1
        self.error_thumb=[]
        self.error_meta=[]
        self.error_sidebar=[]
        self.error_collabo=[]
    
    def collabo(self,fid):
        flag = 5
        while(flag):
            try:
                url = "https://app.box.com/file/"+str(fid)+"/collaborators"
                res = requests.get(url=url, cookies=self.cookies, verify=False)
                split_data = "Box.postStreamData = (.+?);"
                collabo_name = list()
                collabo_email=list()
                string = re.search(split_data, str(res.content)).group(1)
                collabojson = json.loads(string)
                root = "\\/app-api\\/enduserapp\\/item\\/f_"+str(fid)+"\\/collaborators"

                for users in range(len(collabojson[root]["collaborators"])):
                    collabo_name.append(collabojson[root]["collaborators"][users]["name"])
                    collabo_email.append(collabojson[root]["collaborators"][users]["email"])
                print("collaborator : "+collabo_email, collabo_name)
                flag =0
            except Exception as e:
                if(flag>1):
                    flag-=1
                    # print(e)
                    print("collabo : request error, retry...")
                    #shared link는 생성했지만 collaboration기능은 사용하지 않은 경우
                    collabo_name = ""
                    collabo_email =""
                    time.sleep(30)
                else:
                    print("collabo 수집에 실패하여 error 리스트에 저장됩니다. fid : {}".format(fid))
                    self.error_collabo.append(fid)
            return collabo_name, collabo_email

    def get_thumbnail(self, fid, fname, thumbnail):
        flag = 5
        while(flag):
            try:
                if thumbnail:
                    thumbnail = "https://app.box.com"+thumbnail.split("thumb_320.jpg")[0]+"thumb_1024.jpg"
                    res = requests.get(url=thumbnail, cookies=self.cookies, verify=False)
                    # print(res.content)
                    with open(".thumbnail/"+str(fid)+".jpg", 'wb') as f:
                        f.write(res.content)
                flag=0
            except:
                if(flag>1):
                    flag-=1
                    print("thumbnail {} : request error, retry...".format(fname))
                    time.sleep(40)
                else:
                    print("썸네일 다운로드에 실패하여 error 리스트에 저장됩니다. fid : {}, fname : {}".format(fid, fname.encode('utf-8').decode('unicode-escape')))
                    self.error_thumb.append(thumbnail)
                    flag=0

    #get metadata ---
    def meta(self, fid):
        flag=5
        sharedlink=""
        sha1=""
        while(flag):
            try:
                # url = https://app.box.com/index.php?fileIDs[]=955100044758
                url = "https://app.box.com/index.php?fileIDs[]="+str(fid)+"&rm=preview_get_files_metadata"
                res = requests.get(url=url, cookies=self.cookies, verify=False)
                metajson = res.json()
                sharedlink = metajson["filesMetadata"][0]["shared_link"]
                sha1 = metajson["filesMetadata"][0]["sha1"]
                flag = 0
            except:
                if(flag>1):
                   flag-=1
                   print("meta : request error, retry...")
                   time.sleep(30)
                else:
                    print("메타데이터 로드(meta)에 실패하여 error 리스트에 저장됩니다. fid : {}".format(fid))
                    self.error_meta.append(fid)
            return sharedlink, sha1

    def sidebar(self, fid):
        flag = 5
        name= f_created= f_contentCreated= f_contentUpdated= owner= extension= comment_count= thumbnail=""
        itemsize=0
        version_count=0
        while(flag):
            try:
                url = "https://app.box.com/app-api/enduserapp/file/"+str(fid)+"/sidebar"
                res=requests.get(url=url, cookies=self.cookies)
                sidejson = res.json()
                for i in range(0, len(sidejson["items"])):
                    name = sidejson["items"][i]["name"]
                    f_created = sidejson["items"][i]["created"]
                    f_contentCreated = sidejson["items"][i]["contentCreated"]
                    f_contentUpdated = sidejson["items"][i]["contentUpdated"]
                    version_count = sidejson["items"][i]["versionCount"]
                    itemsize = sidejson["items"][i]["itemSize"]
                    # uploader = sidejson["items"][i]["uploader"]
                    owner = sidejson["items"][i]["ownerName"]
                    extension = sidejson["items"][i]["extension"]
                    comment_count = sidejson["items"][i]["commentsCount"]
                    if sidejson["items"][i]["thumbnailURLs"] == "None":
                        thumbnail = None
                    else : thumbnail=sidejson["items"][i]["thumbnailURLs"]["large"]
                    flag=0
            except Exception as e:
                if (flag>1):
                    flag-=1        
                    print("sidebar : request error, retry...")
                    time.sleep(30)
                else:
                    print("메타데이터 로드(sidebar)에 실패하여 error 리스트에 저장됩니다. fid : {}".format(fid))
                    self.error_sidebar.append(fid)
            return name, f_created, f_contentCreated, f_contentUpdated, version_count, itemsize, owner, extension, comment_count, thumbnail


    def parsing_file_list(self, string, root, r):
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
        try:
            res = requests.get(url, cookies=self.cookies)
            r = re.compile("Box.postStreamData")
            folder_list, folder_itemcount, folder_lencount = self.parsing_file_list(res.text.split(';'), root, r)
        except:
            flag = 1
            while(flag):
                try:
                
                    res = requests.get(url, cookies=self.cookies)
                    r = re.compile("Box.postStreamData")
                    folder_list, folder_itemcount, folder_lencount = self.parsing_file_list(res.text.split(';'), root, r)
                    flag =0
                    return folder_list, folder_itemcount, folder_lencount
                except:
                    print("parsing file list : request error, retry...")
                    time.sleep(40)
                    pass
            
        return folder_list, folder_itemcount, folder_lencount

    def get_version1(self, i, _path):
        fid = i["id"]
        #1. get tokens
        url1 = "https://app.box.com/app-api/enduserapp/elements/tokens"
        data = "{\"fileIDs\":["+str(fid)+"]}"
        headers ={
            'X-Request-Token':self.request_token
        }
        flag = 5
        while(flag):
            try : 
                response1 = requests.post(url = url1, cookies=self.cookies,  headers=headers, data=data, verify=False)
                tokenjson = response1.json()
                root1 = str(fid)
                token1 = "Bearer "+tokenjson[root1]["read"]
                stream = "/versions?offset=0&limit=1000&fields=authenticated_download_url,created_at,extension,is_download_available,modified_at,modified_by,name,permissions,restored_at,restored_by,retention,size,trashed_at,trashed_by,uploader_display_name,version_number"
                url2 = "https://api.box.com/2.0/files/"+str(fid)+stream
                headers = {
                    'Authorization': token1
                }
                response2 = requests.get(url = url2, cookies=self.cookies, headers=headers, verify=False)
                vinfojson=response2.json()
                for vcount in range(len(vinfojson["entries"])):
                    vfid = vinfojson["entries"][vcount]["id"]
                    downloadtoken = "1%%21"+tokenjson[root1]["read"][2:]
                    durl = "https://public.boxcloud.com/api/2.0/files/"+str(fid)+"/content?access_token="+downloadtoken+"&version="+str(vfid)
                    is_trashed=""
                    if vinfojson["entries"][vcount]["trashed_at"]:
                        is_trashed="YES"
            except:
                if(flag>1):
                    print("version request error, retry...({})".format(flag))
                else:
                    print("버전 수집에 실패하여 error list에 저장합니다. fid : {}, fname : {}".format(fid, i["name"]))
                    self.erorr_version.append(fid)
                
            return vinfojson["entries"][vcount]["name"], vfid, _path, vinfojson["entries"][vcount]["size"], is_trashed, vinfojson["entries"][vcount]["trashed_at"], vinfojson["entries"][vcount]["created_at"], vinfojson["entries"][vcount]["modified_at"], vinfojson["entries"][vcount]["modified_by"]["login"], vinfojson["entries"][vcount]["version_number"], vinfojson["entries"][vcount]["extension"], vinfojson["entries"][vcount]["uploader_display_name"], durl

    def get_metadata(self, i, _path):
        name, f_created, f_contentCreated, f_contentUpdated, version_count, itemsize,  owner, extension, comment_count, thumbnail=self.sidebar(i["id"])
        lastupdateduser = i["lastUpdatedByName"]
        path=_path
        name = name
        self.get_thumbnail(i["id"], i["name"], thumbnail)
        sharedlink, sha1 = self.meta(i["id"])
        is_trashed = None
        trashed_at=""
        is_shared=None
        server_mtime=""
        collabo_email=""
        collabo_name=""
        version_num=1
        if sharedlink:
            is_shared ="YES"
            collabo_name, collabo_email = self.collabo(i["id"])
        noteflag = 0
        durl = None
        if i["extension"]=="boxnote":
            noteflag=1
        if version_count and noteflag==0:
            vname, vfid, _path, vsize, vis_trashed, vtrashed_at, vf_created,  vserver_mtime, vlastupdateduser, vversion_num, vextension, vowner, vdurl=self.get_version1(i,_path)
            vsha1=""
            
            self.making_json(vname, vfid, _path, vsize, is_shared, vis_trashed, vtrashed_at, vf_created,f_contentCreated, vserver_mtime, vlastupdateduser, vversion_num, vextension, vowner, vsha1, collabo_name, collabo_email, vdurl)
        self.making_json(name, i["id"], path, itemsize, is_shared, is_trashed, f_created, f_contentCreated, server_mtime, lastupdateduser, version_count, version_num, extension, owner, sha1, collabo_name, collabo_email, durl)



    def check_type(self, i, path):
        #check file or folder , if file : get metadata
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
                folder_list = self.check_type(j, path)
            return folder_list

        else : #get metadata
            self.get_metadata(i, path)



    def file_list(self):
        root = "/app-api/enduserapp/folder/0"
        r = re.compile("Box.postStreamData")
        self.jsondata, itemcount, lencount = self.parsing_file_list(self.string, root, r)
        self.metajson = {}
        self.metajson['items']=[]
        while itemcount>lencount:
            url = "https://app.box.com/app-api/enduserapp/folder/0?itemOffset="+str(lencount-1)

            self.jsondata = self.next_page(url, root, itemcount, self.jsondata)
            lencount = len(self.jsondata["/app-api/enduserapp/folder/0"]["items"])
            
            # print("len count : ", lencount)
        print("루트 총 파일, 폴더 수 : ", lencount-1)

        if not os.path.exists("0"):
            os.makedirs("0")
        with open("0\\0.txt",'w') as f:
            json.dump(self.jsondata, f)  

        if not os.path.exists(".thumbnail"):
            os.makedirs(".thumbnail")
        for i in  self.jsondata["/app-api/enduserapp/folder/0"]["items"]:
            if i["type"]=="folder":
                folder_list = self.check_type(i, "0")
            else:
                #get file metadata
                path="0"
                self.get_metadata(i, path)
            print("count : {}".format(self.k))    
        # print(self.error_thumb)
        # print(self.error_collabo)
        # print(self.error_meta)
        # print(self.error_sidebar)
        return self.metadict, self.printlist