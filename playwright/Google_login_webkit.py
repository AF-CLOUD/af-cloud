from playwright.sync_api import Playwright, sync_playwright, expect

###작동 오류###
def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.dropbox.com/login
    page.goto("https://www.dropbox.com/login")

    # Click button:has-text("Google로 로그인") or ("Google 계정으로 로그인")
    # with page.expect_navigation(url="https://accounts.google.com/o/oauth2/auth/identifier?access_type=offline&client_id=801668726815.apps.googleusercontent.com&include_granted_scopes=true&prompt=select_account&redirect_uri=https%3A%2F%2Fwww.dropbox.com%2Fgoogle%2Fauthcallback&response_type=code&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&state=AEIkadM49cfezOsBF2ZTbKmn6a4YyiSd3HmOTurM6AwkyosPoTS1Fp40cTpMk292w7IW6eSIhqHv3_Q9igY-MuPK9bOMBLa-i1MD7BsyNc1CsMPmFCuef8rzcgS3zR2dY7zak6sedAgZVer3oa9lKeVESk2WdCp6U1zQ-28sTFF3enMEvr4ZSc4bJDIjn71akEPsT7Nh5zXZ-k47ncg6L-yShAlj71pzMPPyg3Ar2I1ICKgY_eKUiXLIxboBmp58Q7Rt5e6U5cOsvRiWFdMyXuBq3MAdo5vdV5sywRRS3c4xjvG8jQpRiDz6bnKm21D20RgOfuJwX2EHRJ79Cv0W0utAE8ZAKVthZQZJyKOoIhj84g8GadnNt5-2dqh-N1IWTtg&flowName=GeneralOAuthFlow"):
    with page.expect_navigation():
        with page.expect_popup() as popup_info:
            page.locator("button:has-text(\"Google로 로그인\"), button:has-text(\"Google 계정으로 로그인\")").click()
        page1 = popup_info.value
        page1.set_default_timeout(0)

    page1.wait_for_selector('input[type="email"]')

    # Click [aria-label="이메일 또는 휴대전화"]
    page1.locator("[aria-label=\"이메일 또는 휴대전화\"]").click()

    # Fill [aria-label="이메일 또는 휴대전화"]
    #page1.locator("[aria-label=\"이메일 또는 휴대전화\"]").fill("AF.Cloud.2021@gmail.com")
    page1.type('input[type="email"]', "AF.Cloud.2021@gmail.com")

    # Click button:has-text("다음")
    # with page1.expect_navigation(url="https://accounts.google.com/signin/v2/challenge/pwd?access_type=offline&client_id=801668726815.apps.googleusercontent.com&include_granted_scopes=true&prompt=select_account&redirect_uri=https%3A%2F%2Fwww.dropbox.com%2Fgoogle%2Fauthcallback&response_type=code&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&state=AEIkadM49cfezOsBF2ZTbKmn6a4YyiSd3HmOTurM6AwkyosPoTS1Fp40cTpMk292w7IW6eSIhqHv3_Q9igY-MuPK9bOMBLa-i1MD7BsyNc1CsMPmFCuef8rzcgS3zR2dY7zak6sedAgZVer3oa9lKeVESk2WdCp6U1zQ-28sTFF3enMEvr4ZSc4bJDIjn71akEPsT7Nh5zXZ-k47ncg6L-yShAlj71pzMPPyg3Ar2I1ICKgY_eKUiXLIxboBmp58Q7Rt5e6U5cOsvRiWFdMyXuBq3MAdo5vdV5sywRRS3c4xjvG8jQpRiDz6bnKm21D20RgOfuJwX2EHRJ79Cv0W0utAE8ZAKVthZQZJyKOoIhj84g8GadnNt5-2dqh-N1IWTtg&flowName=GeneralOAuthFlow&cid=1&navigationDirection=forward&TL=AM3QAYZ6bhyarHq9n4b3_Ppz29Gg4jXxwZDYrUTk7nJULrS9UB88vIZQJQMAUQyw"):
    with page1.expect_navigation():
        page1.locator("button:has-text(\"다음\")").click()

    # Click [aria-label="비밀번호 입력"]
    page1.locator("[aria-label=\"비밀번호 입력\"]").click()

    # Fill [aria-label="비밀번호 입력"]
    page1.locator("[aria-label=\"비밀번호 입력\"]").fill("dfrc4738!@#")


    # Click button:has-text("다음")
    # with page1.expect_navigation(url="https://www.dropbox.com/google/authcallback?state=AEIkadM49cfezOsBF2ZTbKmn6a4YyiSd3HmOTurM6AwkyosPoTS1Fp40cTpMk292w7IW6eSIhqHv3_Q9igY-MuPK9bOMBLa-i1MD7BsyNc1CsMPmFCuef8rzcgS3zR2dY7zak6sedAgZVer3oa9lKeVESk2WdCp6U1zQ-28sTFF3enMEvr4ZSc4bJDIjn71akEPsT7Nh5zXZ-k47ncg6L-yShAlj71pzMPPyg3Ar2I1ICKgY_eKUiXLIxboBmp58Q7Rt5e6U5cOsvRiWFdMyXuBq3MAdo5vdV5sywRRS3c4xjvG8jQpRiDz6bnKm21D20RgOfuJwX2EHRJ79Cv0W0utAE8ZAKVthZQZJyKOoIhj84g8GadnNt5-2dqh-N1IWTtg&code=4%2F0AX4XfWisbAF1w7IZ_hb0PEk5MYfCcPNHIpdzFKrE844oza4cpf7_1gpnoCucEj8iQRaE7A&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.other.readonly&authuser=0&prompt=none#"):
    with page1.expect_navigation():
        page1.locator("button:has-text(\"다음\")").click()

    # Close page
    page1.close()

    # Go to https://www.dropbox.com/home
    page.goto("https://www.dropbox.com/home")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
