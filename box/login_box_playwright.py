from math import factorial
from xml.sax.xmlreader import Locator
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import requests

def run(playwright: Playwright) -> None:  #2단계 앱 인증(이미 등록된 신뢰하는 앱), 구글, 기본 인증 가능
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://account.box.com/login")
    page.type('input[type="text"]',"kyn0503121@korea.ac.kr")
    page.click("#login-submit")


    page.type('input[type="password"]', 'forensic4738')
    page.click('#login-submit-password')


    if(page.url=="https://account.box.com/login/mfa?redirectUrl=%2Ffolder%2F0"):
        factor_auth = input("2단계 인증 코드 : ")
        with page.expect_navigation():
            page.type('input[type="text"]', factor_auth)
            page.locator("//*[@id=\"app\"]/div[5]/span/div/div[2]/main/div/div/div/form/button").click()
    

    box_cookie= context.cookies()    
    cookie_z = next((item for item in box_cookie if item['name']=='z'),None) #z의 value only
    cookies = {'z':str(cookie_z['value'])}
    res = requests.get("https://app.box.com/folder/0", cookies=cookies) #자바스크립트 내부에 <script></script>파일,폴더 리스트 등 나옴 (res.text)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright: #구글 로그인
    run(playwright)
