from playwright.sync_api import Playwright, sync_playwright, expect

###정상작동###
def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.dropbox.com/login
    page.goto("https://www.dropbox.com/login")

    # Click button:has-text("Log in with Apple")
    with page.expect_popup() as popup_info:
        page.locator("button:has-text(\"with Apple\")").click()
    page1 = popup_info.value

    # Fill input[type="text"]
    page1.locator("input[type=\"text\"]").fill("ymaul2@korea.ac.kr")

    # Click [aria-label="Continue"]
    page1.locator("[aria-label=\"Continue\"]").click()

    # Fill input[type="password"]
    page1.locator("input[type=\"password\"]").fill("Alswldbsgh220@")

    # Click [aria-label="Sign In"]
    page1.locator("[aria-label=\"Sign In\"]").click()

    # Click text=Don’t Trust
    page1.locator("text=Don’t Trust").click()

    # Click button:has-text("Continue")
    # with page1.expect_navigation(url="https://www.dropbox.com/apple/authcallback"):
    with page1.expect_navigation():
        page1.locator("button:has-text(\"Continue\")").click()

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
