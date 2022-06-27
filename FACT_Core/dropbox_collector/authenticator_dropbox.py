"""
============================================
    "authenticator" Module
============================================
.. moduleauthor:: Jihyeok Yang <piki@korea.ac.kr>

.. note::
    'TITLE'             : Dropbox - Authenticator in AF-Forensics\n
    'AUTHOR'            : Ho Yoon\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.4\n
    'RELEASE-DATE'      : 2022-05-18\n

--------------------------------------------

Description
===========

    OneDrive Internal APIs 를 사용하기 위해 필요한 인증정보(cookie, parameter, header) 수집하는 모듈

    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부

History
===========

    * 2022-05-18 : 초기 버전
    * 2022-06-01 : *로그인 Personal 만 가능하게 수정 -- 추후 변경 여부 파악
    * 2022-06-13 : 코드 안정화 -- add login wait time(sol>> cid, caller)
    * 2022-06-20 : 개인 중요 보관소 추가 --> playwright 버그 존재 사용 잠정 정지

"""

from module.FACT_Cloud_Define import *

class Authentication_dropbox:
    def __init__(self, credential):
        self.__id = credential[0]
        self.__password = credential[1]
        self.__headers = None
        self.__cookies = None

    def run(self):
        if self.__login() == FC_ERROR:
            PRINT('Login Error')
            return FC_ERROR

        return FC_OK

    def __login(self):
        # 버그 존재 사용 금지
        print("""

        <Select Login Mode>
        1.Google Login
        2.Apple Login
        3.Terminate

        """)
        self.__flag = int(input("[Type Number] >>> "))

        if self.__flag ==1: #google login
            driver = uc.Chrome(suppress_welcome=False)
            driver.get('https://www.dropbox.com/login')

            sleep(3)
            driver.find_element(By.CLASS_NAME, "login-form-container__google-div").click()
            sleep(5)
            driver.switch_to.window(driver.window_handles[1])
            sleep(3)
            driver.find_element(By.CLASS_NAME, "whsOnd.zHQkBf").send_keys(self.__id)
            driver.find_element(By.CLASS_NAME,
                                "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qfvgSe.qIypjc.TrZEUc.lw1w4b").click()
            sleep(3)
            driver.find_element(By.CLASS_NAME, "whsOnd.zHQkBf").send_keys(self.__password)
            sleep(1)
            driver.find_element(By.CLASS_NAME,
                                "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qfvgSe.qIypjc.TrZEUc.lw1w4b").click()
            driver.switch_to.window(driver.window_handles[0])

            # print("[System] >>> Click OK button on the device")

            confirm = input("[System] >>> Did you click 'OK' button on the device? (Y/N)")

            print("[System] >>> Login succeeded!")
            print("[System] >>> Acquring authentication information. Please wait...")

            sleep(15)
            uid_html = driver.find_elements(By.CSS_SELECTOR, "body > script")

            for i in range(len(uid_html)):
                if "constants/auth" and "user_id" in uid_html[i].get_attribute("innerText"):
                    inner_text = """%s""" % uid_html[i].get_attribute("innerText")
                    uid_filter = re.compile('(: )(.*?)(})')
                    uid_result = uid_filter.findall(inner_text)
                    uid = uid_result[0][1]

            dropbox_cookies = driver.get_cookies()
            cookie_listing = []

            for i in range(len(dropbox_cookies)):
                cookie_listing.append((dropbox_cookies[i]["name"], dropbox_cookies[i]["value"]))

            self.__cookies = {}  # 필수쿠키
            essential_cookies = ["t", "jar", "lid", "bjar", "blid"]  # 필수쿠키 선별

            for i in range(len(cookie_listing)):
                if cookie_listing[i][0] in essential_cookies:
                    self.__cookies[cookie_listing[i][0]] = cookie_listing[i][1]

            token = self.__cookies["t"]  # 획득한 쿠키 중 사용자 인증 담당하는 필수 헤더값에 필요한 값 별도 추출 후 아래에서 대입
            self.__headers = {'X-CSRF-Token': '', 'X-Dropbox-Uid': '', 'Content-Type': 'application/json'}  # 필수 헤더
            self.__headers['X-CSRF-Token'] = token
            self.__headers['X-Dropbox-Uid'] = uid

            driver.close()

        if self.__flag ==2:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.dropbox.com/login")
                with page.expect_popup() as popup_info:
                    page.locator("button:has-text(\"Apple로 로그인\")").click()
                page1 = popup_info.value
                page1.locator("input[type=\"text\"]").fill(self.__id)
                page1.locator("[aria-label=\"계속\"]").click()
                page1.locator("input[type=\"password\"]").fill(self.__password)
                page1.locator("[aria-label=\"로그인\"]").click()
                page1.locator("text=신뢰함").click()

                with page1.expect_navigation():  # 2차인증 확인 후 브라우저에 직접 입력
                    page1.locator("button:has-text(\"계속\")").click()
                page1.close()

                print("[System] >>> Login succeeded!")
                print("[System] >>> Acquring authentication information. Please wait...")

                page.goto("https://www.dropbox.com/")
                page.goto("https://www.dropbox.com/home")

                page.wait_for_timeout(10000)  # HTML 로딩 기다리기 위함
                uid_html = page.query_selector_all("body > script")  # 로그인 후 "/home" 에서 "X-Dropbox-Uid" 값 관련 태그에서 얻기 위함

                for i in range(len(uid_html)):
                    if "constants/auth" and "user_id" in uid_html[i].inner_text():
                        inner_text = """%s""" % uid_html[i].inner_text()
                        uid_filter = re.compile('(: )(.*?)(})')
                        uid_result = uid_filter.findall(inner_text)
                        uid = uid_result[0][1]

                dropbox_cookies = page.context.cookies()  # cookies 획득
                cookie_listing = []

                for i in range(len(dropbox_cookies)):
                    cookie_listing.append((dropbox_cookies[i]['name'], dropbox_cookies[i]['value']))

                self.__cookies = {}  # 필수쿠키
                essential_cookies = ["t", "jar", "lid", "bjar", "blid"]  # 필수쿠키 선별

                for i in range(len(cookie_listing)):
                    if cookie_listing[i][0] in essential_cookies:
                        self.__cookies[cookie_listing[i][0]] = cookie_listing[i][1]

                token = self.__cookies["t"]  # 획득한 쿠키 중 사용자 인증 담당하는 필수 헤더값에 필요한 값 별도 추출 후 아래에서 대입
                self.__headers = {'X-CSRF-Token': '', 'X-Dropbox-Uid': '', 'Content-Type': 'application/json'}  # 필수 헤더
                self.__headers['X-CSRF-Token'] = token
                self.__headers['X-Dropbox-Uid'] = uid

    def headers(self):
        return self.__headers

    def cookies(self):
        return self.__cookies