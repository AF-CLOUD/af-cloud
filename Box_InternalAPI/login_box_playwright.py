from playwright.sync_api import Playwright, sync_playwright
import time
import re
import requests
import json
from box_tools import get_box_file_list
from box_tools import box_file_downloads
from box_tools import file_download
from box_tools import get_boxnotes_link
class Box:
    def __init__(self):
        self.box = "box"
        self.request_token = ""

    def run(self, playwright: Playwright) -> None:  #2단계 앱 인증(이미 등록된 신뢰하는 앱), 구글, 기본 인증 가능
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://account.box.com/login")
        page.type('input[type="text"]',"kyn0503121@korea.ac.kr")
        page.click("#login-submit")

        page.type('input[type="password"]', 'forensic4738')
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

        #get token & file_list(root folder)
        res = requests.get("https://app.box.com/folder/0", cookies=cookies_z) #자바스크립트 내부에 <script></script>파일,폴더 리스트, requestToken 등 나옴 (res.text)
        
        #parsing request_token
        string = res.text.split(';')
        self.request_token = re.search(',\"requestToken\":\"(.+?)\",\"billing\":{', res.text).group(1)

        #parsing all file list (root & other folder)
        make_file_list = get_box_file_list.get_file_list(string, cookies_z)
        parsing_dt = make_file_list.file_list()


        file_id = "f_943706767031" #사용자가 지정한 파일로 교체할 예정~
        
        #file download   
        fd=file_download.f_download(z, file_id, self.request_token, "0.jpg", "file")
        fd.f_dload()

        #Box Notes
        file_id = "f_885745754197"
        notes = get_boxnotes_link.notes_link(z, self.request_token, file_id)
        notes.f_link()
    

if __name__ =="__main__":
    with sync_playwright() as playwright: #구글 로그인
        box_forensics = Box()
        box_forensics.run(playwright)
