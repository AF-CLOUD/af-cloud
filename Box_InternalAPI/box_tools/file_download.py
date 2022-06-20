import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class f_download:
    def __init__(self, z, file_id, request_token, file_des, file_name):
        self.z = z
        self.file_id = file_id
        self.request_token = request_token
        self.file_des = file_des
        self.file_name=file_name

    def f_dload(self):
        cookies = {
            'z': self.z,
        }

        data = {
            'request_token': self.request_token,
        }
        
        params = {
            'rm': 'box_v2_download_file',
            'file_id': self.file_id,
        }
        res = requests.post(url='https://app.box.com/index.php', data=data, cookies=cookies, params=params,verify=False)


        with open(self.file_name,'wb') as f:
            f.write(res.content)

        print("file download success, f id : ", self.file_id)

    