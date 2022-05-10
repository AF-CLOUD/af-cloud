from playwright.sync_api import sync_playwright
from time import sleep
import requests

def run(playwright, account_id, account_pw):
    chromium = playwright.firefox
    browser = chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://accounts.google.com/signin/v2/identifier?service=wise&passive=true&continue=http%3A%2F%2Fdrive.google.com%2F%3Futm_source%3Den&utm_medium=button&utm_campaign=web&utm_content=gotodrive&usp=gtd&ltmpl=drive&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

    page.wait_for_selector('input[type="email"]')
    page.type('input[type="email"]', account_id)
    page.click("#identifierNext")
    # login-submit
    page.wait_for_selector('input[type="password"]')
    page.type('input[type="password"]', account_pw)
    page.click("#passwordNext")
    # #############################
    sleep(4)
    essential_cookie = dict()
    c_value = page.context.cookies()
    for c in c_value:
        # if c['name'] == "SID":
        #     essential_cookie["SID"] = c['value']
        # elif c['name'] == "SSID":
        #     essential_cookie["SSID"] = c['value']
        # elif c['name'] == "HSID":
        #     essential_cookie["HSID"] = c['value']
        if "Check" in c['name'] or "LSID" in c['name'] or "__Host" in c['name'] or "ACCOUNT" in c['name'] or "len" in c['name']:
            continue
        essential_cookie[c['name']] = c['value']
    # page.request()
    print(essential_cookie)
    cookies = essential_cookie

    headers = {
        'Host': 'drive.google.com',
        'Connection': 'keep-alive',
        'X-Json-Requested': 'true',
        'X-Drive-First-Party': 'DriveWebUi',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Accept': '*/*',
        'Sec-GPC': '1',
        'Origin': 'https://drive.google.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://drive.google.com/drive/my-drive',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'SID=Iggkjv4XguvumZfUBco7iTAEyZBAFk2RxMiOxnoixbg4XwM3eqZnfIosqnX45KL3P4SJlQ.; __Secure-1PSID=Iggkjv4XguvumZfUBco7iTAEyZBAFk2RxMiOxnoixbg4XwM3DUJkKyjw7j-bGwUJFBwc7Q.; __Secure-3PSID=Iggkjv4XguvumZfUBco7iTAEyZBAFk2RxMiOxnoixbg4XwM3c9Fo5lcIW96Htiju8YDwJw.; HSID=A1H-moXmYIjAkSx0z; SSID=AftKC8p-yLt-uItfO; APISID=guM9QKFTv95Hqa7q/AH7M39EdI_CUUZzzW; SAPISID=q3F-ZLdZJnrPi1fD/AYMqBoaRRqSMAaMoD; __Secure-1PAPISID=q3F-ZLdZJnrPi1fD/AYMqBoaRRqSMAaMoD; __Secure-3PAPISID=q3F-ZLdZJnrPi1fD/AYMqBoaRRqSMAaMoD; 1P_JAR=2022-04-01-04; SEARCH_SAMESITE=CgQIi5UB; AEC=AVQQ_LBqhhh8p6Vq5geM9TyoVWxzKNEAguLDmAwBdcAxj6j_l-K0xaB0yNU; NID=511=ZEoS_H7yEUX1lFD4vFh_dLzJmgeaXLVHRvhD-rXu47iH7GpSBmvd_59JunEwSjTOEX1XL6cuoncvA3zBCasDPtcGv_oV9-vAUk7z1QfyZALySXzYqlyIW3nyMF73XZUd2aks3H2J8om43gbw57C9mtrtljP-vSoaI1HGNGk_EhRIrFyEV4rHLX_20PEdy0GG47r_dL7W1oqbRDaOQzETya5TvbgMt1XUj_Tn-Vo; SIDCC=AJi4QfErc7ccYdyawI19EaUYNXi539wKrDzlrEstZWo2oSsVnXR0a1Iikz8nLYh3y1MhXt45BA; __Secure-3PSIDCC=AJi4QfFpSYw_Vuz__0t3d4Zq3BUNHagltLeth4E4vFFYUScAQiPA5PjAS_AzNbCBCSHZNeMs',
    }

    headers2 = {
        'Host': 'doc-00-bg-docs.googleusercontent.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'iframe',
        'Accept-Language': 'ko-KR,ko;q=0.9',
    }

    headers3 = {
        'Host': 'docs.google.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'iframe',
        'Accept-Language': 'ko-KR,ko;q=0.9',
    }

    headers4 = {
        'Host': 'doc-00-bg-docs.googleusercontent.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'cross-sit4e',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'iframe',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        # 'Cookie': 'AUTH_5snbfn7k1d0n7avissfa95gafbmpfhbl_nonce=o26hju8sjhtlu',
    }

    thumb_headers = {
        'Host': 'lh3.google.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'image',
        'Referer': 'https://drive.google.com/',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'SID=Jwgkju0A0UjPydIkQeL1lapjdHmMf-SJuOhkIyPelZuGosSjzEaK6YPvNj7wA1B6YZhQwg.; __Secure-1PSID=Jwgkju0A0UjPydIkQeL1lapjdHmMf-SJuOhkIyPelZuGosSjg53PGT1e16xB4JVs8pHpUg.; __Secure-3PSID=Jwgkju0A0UjPydIkQeL1lapjdHmMf-SJuOhkIyPelZuGosSjWZOOuSDV6EuVSKkC0XhEpQ.; HSID=A2KUvnNqgXGhh02CU; SSID=A4Vev5tyz6VVG3CLL; APISID=EO6t6YQiNjFIOD3g/AkumvP3E3IBpG3_ql; SAPISID=Oa_rTKrFlTSgmRg7/AM9-BCIQFJV-3DogZ; __Secure-1PAPISID=Oa_rTKrFlTSgmRg7/AM9-BCIQFJV-3DogZ; __Secure-3PAPISID=Oa_rTKrFlTSgmRg7/AM9-BCIQFJV-3DogZ; SEARCH_SAMESITE=CgQIpJUB; AEC=AakniGNmBaCpfcoVmpHoVXgS1bGCex9Hxrcap3pkH_kGpMZJ-LVXnbfQGEk; 1P_JAR=2022-04-27-14; NID=511=Fbm8RX3u0SVRqbJ2He_1bEmm5RNOgycBCmOR0RsgWLTs9qMvtVqc9l9lYCHPDZ8HyxUXXEzGNF-DT6X39EMFDTom6Npu3EoMgmGApET5LVhPDMw2Q86PLOfbIXPbvmqkD1Xb7nJJyd6YiDzFyRgYDAyGS-GXrLlcfKiPH0uhgXdbheU9mg27CDR1un9Z6BeybiN0j-OFza9RIIsiPgq8pWiHl-9Z8d4q2F94GwAfQqIlUeAn_HpEq7yEb60XgZvs; SIDCC=AJi4QfF7c3hP_NMsGV105HKEd-q0yqAFvcU-33yhFa24ohy6ud8h6gmM_15lot56ioN1p1T6AQ; __Secure-3PSIDCC=AJi4QfGJg2vzmj9jBsyKbXiKfV3XhafbnHpmUX2PnJV-IRTnY-Cu3KeCiOLMYZdghufwk7E6Hg',
    }

    thumb2_headers = {
        'Host': 'lh3.googleusercontent.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'image',
        'Referer': 'https://drive.google.com/',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9',
    }

    params = {
        'id': 'tmp',
        'authuser': '1',
        'export': 'download',
    }


    # Thumbnail catch
    # res = requests.get('https://lh3.google.com/u/0/d/11ovwlSFwtt7ygSfs-073zfiNCfj8nNjx=w640-h400-p-k-nu-iv1', headers=thumb_headers, cookies=cookies)
    # u = res.url
    # ress = requests.get(u, headers=thumb2_headers, cookies=cookies)
    # with open('test.png', 'wb') as f:
    #     f.write(ress.content)

    params['id'] = '1qn_XzhdbUk-Zly2XYeEAxvrPAvJkGtS5'

    res = requests.post('https://drive.google.com/uc', headers=headers, cookies=cookies, params=params, verify=False)
    content = res.text
    a = content.find("https:")
    second_url = content[a:-2]
    second_url = second_url.replace("\\/", "/")
    print("2nd URL: " + second_url)
    host_offset = second_url.find('//doc')
    host_end_offset = second_url.find('.com')
    second_host = second_url[host_offset+2:host_end_offset+4]

    headers2['Host'] = second_host
    headers4['Host'] = second_host

    res2 = requests.get(second_url, headers=headers2, cookies=cookies, verify=False)
    if len(res2.history) == 0:
        res2 = requests.get(second_url, headers=headers3, cookies=cookies, verify=False)
        third_url = res2.history[0].headers['location']
    else:
        third_url = res2.history[0].headers['location']

    # third_url = res2.url.replace("%", "%%")
    print("3rd URL: " + third_url)

    res3 = requests.get(third_url, headers=headers3, cookies=cookies, verify=False)
    fourth_url = res3.history[0].headers['location']

    print('4th URL: ' + fourth_url)
    nonce_offset = fourth_url.find('&nonce')
    end_offset = fourth_url.find('&user')
    nonce = fourth_url[nonce_offset+7:end_offset]

    download_cookie = {
        'AUTH_5snbfn7k1d0n7avissfa95gafbmpfhbl_nonce': nonce,
    }
    res4 = requests.get(fourth_url, headers=headers4, cookies=download_cookie, verify=False)
    file_content = res4.content
    with open('./filetest', 'wb') as f:
        f.write(file_content)
        
        
    sleep(100)

    browser.close()

with sync_playwright() as playwright:
    account_id = input("Google ID: ")
    account_pw = input("Google pw: ")
    run(playwright, account_id, account_pw)
