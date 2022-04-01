from playwright.sync_api import Playwright, sync_playwright, expect

###작동 오류###
def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.dropbox.com/login
    page.goto("https://www.dropbox.com/login")

    # Click button:has-text("Apple로 로그인")
    # with page.expect_navigation(url="https://appleid.apple.com/auth/authorize?client_id=com.dropbox.Backend&redirect_uri=https%3A%2F%2Fwww.dropbox.com%2Fapple%2Fauthcallback&response_mode=form_post&response_type=code&scope=name%20email&state=AEJ9lLCfIMKUXBzogQ_dTkTs4OXIPyyyZQHJybYBp3aVnIjsl1zRY8VPe_ZAatONP82qQQqYGtdtTOi38XBSe7Iurpp7sL_UPZvSNTAmQhP55NTIErI-4kxSTVpHKKOBPpoo3yJG2kBo-cAdq6wBdPTb5_j9NHrUXy05y-f3nVBfGHWzveLcwBwXP3rgD5r5s5HM-R26s6W_QkZPAofQNVwqq5uFnec_-_ytNN3SEkOr1-JdFbHWrdVDZfMeCbSyqIsseBwQk2v71JZUcm6vMkj6xmFgpt30J3hswTaxkmalT1jqA1FMbBTkc61fHApA8HducTdxhVUeUVP3masHV8AGZrtTzRr5rynuv7z2ovq0_BiYc2Xpe4MrdS9M4eK5OHpx9mtThIxTMYtkdoVd4ytQ"):
    with page.expect_navigation():
        with page.expect_popup() as popup_info:
            page.locator("button:has-text(\"Apple로 로그인\")").click()
        page1 = popup_info.value
        page1.set_default_timeout(0)

    page1.wait_for_selector('input[type="text"]')

    # Click input[type="text"]
    page1.locator("input[type=\"text\"]").click()
    
    # Fill input[type="text"]
    #page1.locator("input[type=\"text\"]").fill("ymaul2@korea.ac.kr")
    page1.type('input[type="email"]', "ymaul2@korea.ac.kr")

    # Press Enter
    page1.locator("input[type=\"text\"]").press("Enter")

    # Fill input[type="password"]
    page1.locator("input[type=\"password\"]").fill("Alswldbsgh220@")

    # Press Enter
    page1.locator("input[type=\"password\"]").press("Enter")

    # Click text=신뢰함
    page1.locator("text=신뢰함").click()

    # Click button:has-text("계속")
    # with page1.expect_navigation(url="https://www.dropbox.com/apple/authcallback"):
    with page1.expect_navigation():
        page1.locator("button:has-text(\"계속\")").click()

    # Close page
    page1.close()

    # Go to https://www.dropbox.com/
    page.goto("https://www.dropbox.com/")

    # Go to https://www.dropbox.com/home
    page.goto("https://www.dropbox.com/home")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
