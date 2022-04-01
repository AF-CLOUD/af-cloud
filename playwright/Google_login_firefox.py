from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.dropbox.com/login
    page.goto("https://www.dropbox.com/login")

    # Click button:has-text("Log in with Google")
    # with page.expect_navigation(url="https://accounts.google.com/o/oauth2/auth/identifier?access_type=offline&client_id=801668726815.apps.googleusercontent.com&include_granted_scopes=true&prompt=select_account&redirect_uri=https%3A%2F%2Fwww.dropbox.com%2Fgoogle%2Fauthcallback&response_type=code&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&state=AEI08x3931ahW8YixXmkon-wGxsg_yAaqJBiNN5nm1xo4glMma18NbvJ8s2UKkVVF9LZeoit38R9nZVZEiTkBbnnMI59E7XLTY0PwQIbd-tbwRCMQI_VIvpBPofgANNjZUC6PBYU-lywdCYq_xZivLwVa7p8zDFnk18C2bgc7nrCMRZdYqDRK9IHWNBFezzbDO6isJiyF1Qlr4ukiRf2SN2jMKVBMWuLE-Gn7vAaffl2AZ3bUXT7vsbJVksr3n9ptA_RDX2FOfBJhT_OizWE3r-r8o5NHeLsQTiyQRsA9OevWT-sriqlWq09dDxZIkU04aOyX-TZA8YBNEhQgFSvWxsmoomosbiNeyDwH_wcMa_HMm9NzZFT6V70ESKIHb8ZgwE&flowName=GeneralOAuthFlow"):
    with page.expect_navigation():
        with page.expect_popup() as popup_info:
            page.locator("button:has-text(\"Log in with Google\")").click()
        page1 = popup_info.value

    # Click [aria-label="이메일 또는 휴대전화"]
    page1.locator("[aria-label=\"이메일 또는 휴대전화\"]").click()

    # Fill [aria-label="이메일 또는 휴대전화"]
    #page1.locator("[aria-label=\"이메일 또는 휴대전화\"]").fill("AF.Cloud.2021@gmail.com")
    page1.type('input[type="email"]', "AF.Cloud.2021@gmail.com")

    # Click button:has-text("다음")
    # with page1.expect_navigation(url="https://accounts.google.com/signin/v2/challenge/pwd?access_type=offline&client_id=801668726815.apps.googleusercontent.com&include_granted_scopes=true&prompt=select_account&redirect_uri=https%3A%2F%2Fwww.dropbox.com%2Fgoogle%2Fauthcallback&response_type=code&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&state=AEI08x3931ahW8YixXmkon-wGxsg_yAaqJBiNN5nm1xo4glMma18NbvJ8s2UKkVVF9LZeoit38R9nZVZEiTkBbnnMI59E7XLTY0PwQIbd-tbwRCMQI_VIvpBPofgANNjZUC6PBYU-lywdCYq_xZivLwVa7p8zDFnk18C2bgc7nrCMRZdYqDRK9IHWNBFezzbDO6isJiyF1Qlr4ukiRf2SN2jMKVBMWuLE-Gn7vAaffl2AZ3bUXT7vsbJVksr3n9ptA_RDX2FOfBJhT_OizWE3r-r8o5NHeLsQTiyQRsA9OevWT-sriqlWq09dDxZIkU04aOyX-TZA8YBNEhQgFSvWxsmoomosbiNeyDwH_wcMa_HMm9NzZFT6V70ESKIHb8ZgwE&flowName=GeneralOAuthFlow&cid=1&navigationDirection=forward&TL=AM3QAYZ2DnSeW7FbzCuykKH1Tz-s8HMgC3gtFYKbaN0VKt3DBb1tmJUaCccXVh0A"):
    with page1.expect_navigation():
        page1.locator("button:has-text(\"다음\")").click()

    # Click [aria-label="비밀번호 입력"]
    page1.locator("[aria-label=\"비밀번호 입력\"]").click()

    # Fill [aria-label="비밀번호 입력"]
    page1.locator("[aria-label=\"비밀번호 입력\"]").fill("dfrc4738!@#")

    # Click button:has-text("다음")
    # with page1.expect_navigation(url="https://www.dropbox.com/google/authcallback?state=AEI08x3931ahW8YixXmkon-wGxsg_yAaqJBiNN5nm1xo4glMma18NbvJ8s2UKkVVF9LZeoit38R9nZVZEiTkBbnnMI59E7XLTY0PwQIbd-tbwRCMQI_VIvpBPofgANNjZUC6PBYU-lywdCYq_xZivLwVa7p8zDFnk18C2bgc7nrCMRZdYqDRK9IHWNBFezzbDO6isJiyF1Qlr4ukiRf2SN2jMKVBMWuLE-Gn7vAaffl2AZ3bUXT7vsbJVksr3n9ptA_RDX2FOfBJhT_OizWE3r-r8o5NHeLsQTiyQRsA9OevWT-sriqlWq09dDxZIkU04aOyX-TZA8YBNEhQgFSvWxsmoomosbiNeyDwH_wcMa_HMm9NzZFT6V70ESKIHb8ZgwE&code=4%2F0AX4XfWiHEq078NQSZARb69Z20bGOrhBV6-2SOIas4FIIeYqAwI45bdg-5ok0LREOcngk_Q&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&authuser=0&prompt=none"):
    with page1.expect_navigation():
        page1.locator("button:has-text(\"다음\")").click()
    # expect(page1).to_have_url("https://accounts.google.com/signin/v2/challenge/pwd?access_type=offline&client_id=801668726815.apps.googleusercontent.com&include_granted_scopes=true&prompt=select_account&redirect_uri=https%3A%2F%2Fwww.dropbox.com%2Fgoogle%2Fauthcallback&response_type=code&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&state=AEI08x3931ahW8YixXmkon-wGxsg_yAaqJBiNN5nm1xo4glMma18NbvJ8s2UKkVVF9LZeoit38R9nZVZEiTkBbnnMI59E7XLTY0PwQIbd-tbwRCMQI_VIvpBPofgANNjZUC6PBYU-lywdCYq_xZivLwVa7p8zDFnk18C2bgc7nrCMRZdYqDRK9IHWNBFezzbDO6isJiyF1Qlr4ukiRf2SN2jMKVBMWuLE-Gn7vAaffl2AZ3bUXT7vsbJVksr3n9ptA_RDX2FOfBJhT_OizWE3r-r8o5NHeLsQTiyQRsA9OevWT-sriqlWq09dDxZIkU04aOyX-TZA8YBNEhQgFSvWxsmoomosbiNeyDwH_wcMa_HMm9NzZFT6V70ESKIHb8ZgwE&flowName=GeneralOAuthFlow&cid=1&navigationDirection=forward&TL=AM3QAYZ2DnSeW7FbzCuykKH1Tz-s8HMgC3gtFYKbaN0VKt3DBb1tmJUaCccXVh0A")

    # Close page
    page1.close()

    # Go to https://www.dropbox.com/home
    page.goto("https://www.dropbox.com/home")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
