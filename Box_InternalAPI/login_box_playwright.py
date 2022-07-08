from playwright.sync_api import Playwright, sync_playwright
import time
import re
import requests
import json
from box_tools import get_box_file_list
from box_tools import Box_explorer
import urllib3
from tabulate import tabulate
import os 
from pyfiglet import Figlet
from termcolor import colored

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Box:
    def __init__(self, path):
        self.box = "box"
        self.request_token = ""
        self.path = path
    def run(self, playwright: Playwright) -> None:  #2단계 앱 인증(이미 등록된 신뢰하는 앱), 구글, 기본 인증 가능
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://account.box.com/login")
        page.type('input[type="text"]',"kim_3738@korea.ac.kr")
        page.click("#login-submit")

        page.type('input[type="password"]', 'dfrc4738')
        page.click('#login-submit-password')

        #if 2-factor(SMS or TOTP)
        if(page.url=="https://account.box.com/login/mfa?redirectUrl=%2Ffolder%2F0"):
            factor_auth = input("2단계 인증 코드 : ")
            with page.expect_navigation():
                page.type('input[type="text"]', factor_auth)
                page.locator("//*[@id=\"app\"]/div[5]/span/div/div[2]/main/div/div/div/form/button").click()
        
        #get cookie :z
        box_cookie= context.cookies()    
        cookies = next((item for item in box_cookie if item['name']=='z'),None) #z value only
        z = str(cookies['value'])
        cookies_z = {'z': z}

        #browser close
        context.close()
        browser.close()

        string =""
        flag =1
        while(flag):
            try:
                #get token & file_list(root folder)
                res = requests.get("https://app.box.com/folder/0", cookies=cookies_z) #자바스크립트 내부에 <script></script>파일,폴더 리스트, requestToken
                #parsing request_token
                string = res.text.split(';')
                self.request_token = re.search(',\"requestToken\":\"(.+?)\",\"billing\":{', res.text).group(1)
                print("필수 정보 : ")
                print("cookie z : ", cookies_z)
                print("Request_Token : ", self.request_token)
                print("")
                flag =0
            except:
                pass
        # parsing all file list (root & other folder)
        print("로그인 성공, 메타데이터 수집을 시작합니다. ")
        make_file_list = get_box_file_list.get_file_list(string, cookies_z, self.request_token)
        parsing_dt, printlist = make_file_list.file_list()
        with open("meta.txt",'w') as f:
            json.dump(parsing_dt, f)
        print("메타데이터 및 썸네일 수집이 완료되었습니다. 작업을 골라주세요. ")
        #임시! PARSING DT에 파일에서 불러온 딕셔너리 저장
        # parsing_dt=""

        user_action =Box_explorer.user_menu(cookies_z, printlist, parsing_dt,  self.request_token)
        # user_action =Box_explorer.user_menu(cookies_z,  self.request_token)
        user_action.main_explorer()

if __name__ =="__main__":
    with sync_playwright() as playwright: #구글 로그인, box로그인 둘 다 가능

        os.system('cls')
        f = Figlet(font='big')
        print(colored(f.renderText('< FACT >\n                        - CLOUD'), 'blue'))
        print(colored("[Police-Lab 2.0] Research on Data Acquisition and Analysis for Counter Anti-Forensics\n\n", 'blue'))
        path = r"D:\승아\AF안티포렌식\box\playwright\0"
        box_forensics = Box(path)
        box_forensics.run(playwright)