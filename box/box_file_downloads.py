import requests
import json
class box_download:
    def __init__(self, file_list, requestToken):
        self.flist = json.loads(file_list)
        # self.fidlist = 
        # self.request_token = requestToken
        
        # self.file_id = fID
        
        # print(self.flist['/app-api/enduserapp/folder/0'])
    def fdownloda(self):
        # request #1
        url = "https://app.box.com/index.php?rm=box_v2_download_file&file_id="+self.file_id
        # res = requests.post(url, data=self.request_token)
        # print(res.text)