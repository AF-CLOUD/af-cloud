from playwright.sync_api import Playwright, sync_playwright, expect
import requests

def run(playwright: Playwright) -> None:  #2단계 앱 인증(이미 등록된 신뢰하는 앱), 구글, 기본 인증 가능
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://account.box.com/login
    page.goto("https://account.box.com/login")

    # Click [placeholder="이메일 입력"]
    page.locator("[placeholder=\"이메일 입력\"]").click()

    # Fill [placeholder="이메일 입력"]
    page.locator("[placeholder=\"이메일 입력\"]").fill("kyn0503121@korea.ac.kr")

    # Press Enter
    page.locator("[placeholder=\"이메일 입력\"]").press("Enter")
    # expect(page).to_have_url("https://account.box.com/login?redirect_url=%2F")

    # Click [placeholder="암호 입력"]
    page.locator("[placeholder=\"암호 입력\"]").click()

    # Fill [placeholder="암호 입력"]
    page.locator("[placeholder=\"암호 입력\"]").fill("forensic4738")

    # Press Enter
    page.locator("[placeholder=\"암호 입력\"]").press("Enter")

    if(page.url=="https://account.box.com/login/mfa?redirectUrl=%2Ffolder%2F0"):
        # expect(page).to_have_url("https://account.box.com/login/mfa?redirectUrl=%2Ffolder%2F0")
        factor_auth = input("2단계 인증 코드 : ")
        # Fill [placeholder="\36 자리 코드 입력"]
        page.locator("[placeholder=\"\\36 자리 코드 입력\"]").fill(str(factor_auth))

        # Press Enter
        # with page.expect_navigation(url="https://app.box.com/folder/0"):
        with page.expect_navigation():
            page.locator("[placeholder=\"\\36 자리 코드 입력\"]").press("Enter")

    box_cookie= context.cookies()

    cookie_z = next((item for item in box_cookie if item['name']=='z'),None) #z의 value only
    cookies = {'z':str(cookie_z['value'])}
    res = requests.get(page.url, cookies=cookies) #자바스크립트 내부에 <script></script>파일,폴더 리스트 등 나옴 (res.text)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright: #구글 로그인
    run(playwright)