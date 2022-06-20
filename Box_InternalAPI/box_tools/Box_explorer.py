import json
import requests

class user_menu:
    def __init__(self, cookie, parsing_dt, request_token):
        self.cookie = cookie
        self.metajson = parsing_dt
        self.request_token = request_token

    def f_dload(self, select_n):
        fid = self.metajson[select_n][select_n]["id"]

        data = {
            'request_token': self.request_token,
        }
        
        params = {
            'rm': 'box_v2_download_file',
            'file_id': fid,
        }
        res = requests.post(url='https://app.box.com/index.php', data=data, cookies=self.cookie, params=params,verify=False)


        with open(self.file_name,'wb') as f:
            f.write(res.content)

        print("file download success, f id : ", fid)

    def user_req(self, select):
        print(self.metajson[select])
