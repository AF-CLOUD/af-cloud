import requests
import json
import re

class notes_link:
    def __init__(self, z, request_token,  file_id):
        self.z = z
        self.file_id = file_id
        self.request_token = request_token

    def f_link(self):
        cookies = {
            'z': self.z,
        }
        data = {
            'request_token': self.request_token,
        }
        url = "https://app.box.com/app-api/enduserapp/item/" + self.file_id+"/shared-link"
        res = requests.post(url,cookies=cookies, data =data, verify=False)
        # print(res.content)
        split_data = "\"sharedLink\":(.+?),\"type\""
        string = re.search(split_data,str(res.content)).group(1)
        # print(string)
        
        
        return string

