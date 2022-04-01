from playwright.sync_api import Playwright, sync_playwright, expect

###정상작동###
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.dropbox.com/login
    page.goto("https://www.dropbox.com/login")

    # Click button:has-text("Apple로 로그인")
    with page.expect_popup() as popup_info:
        page.locator("button:has-text(\"Apple로 로그인\")").click()
    page1 = popup_info.value

    # Fill input[type="text"]
    page1.locator("input[type=\"text\"]").fill("ymaul2@korea.ac.kr")

    # Click [aria-label="계속"]
    page1.locator("[aria-label=\"계속\"]").click()

    # Fill input[type="password"]
    page1.locator("input[type=\"password\"]").fill("Alswldbsgh220@")

    # Click [aria-label="로그인"]
    page1.locator("[aria-label=\"로그인\"]").click()

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

    page.context.cookies()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
