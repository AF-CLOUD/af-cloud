import requests
import json

class notes_link:
    def __init__(self, z, file_id):
        self.z = z
        self.file_id = file_id

    def f_link(self):
        cookies = {
            'z': self.z,
        }
        url = "https://app.box.com/app-api/enduserapp/item/" + self.file_id+"/shared-link"
        res = requests.post(url='https://app.box.com/index.php',cookies=cookies, verify=False)
        print(res.content)
