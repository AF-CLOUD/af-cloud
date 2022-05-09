from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import json
import re
import urllib3

def functions(headers, cookies):
    while True:
        print("""

        <Select Mode>
        1.File Browser & Download
        2.Terminate

        """)

        try:
            mode = int(input(">>> "))
            if mode == 1:
                global folder
                folder = ['/']
                global file
                file = []

                print("[System] >>> File Browsing Start!")
                print("[System] >>> Working on... A list of files will appear shortly")

                recursive_search_folder("", headers, cookies) #Root Directory부터 재귀적으로 모든 폴더 목록 획득
                print("[System] >>> Existing Folders:", folder)

                for i in range(len(folder)): #획득한 폴더 각각을 input으로 해당 폴더에 존재하는 파일 목록 획득
                    recursive_search_file(folder[i], headers, cookies)

                print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡList of Filesㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")

                for i in range(len(file)):
                    print("[%d]" % (i+1), file[i]) #List of All Files

                try:
                    while True:
                        sec_mode = input("\n[System] >>> Wish to download files? (y/n)\n") #파일 다운로드 - 로컬에서 저장경로 설정 필

                        if sec_mode == "y":
                            file_download(cookies) #파일 다운로드 - 로컬에서 저장경로 설정 필

                        elif sec_mode == "n":
                            break

                        else:
                            print("[System] >>> Invalid input. Please try again")

                except Exception as e:
                    print("[System] >>> Invalid input or error occurred. Please try again")
                    #print(e)

            if mode == 2:
                print("[System] >>> File Browsing & Download Terminated")
                break

        except Exception as e:

            print("[System] >>> Invalid input. Please check again?")
            #print("[System] >>> Error:", e)


def file_download(cookies):
    global file #삭제된 파일을 포함한 전체 파일 리스트, 파일별 메타데이터 정보 포함
    downloadble_file = [] #삭제된 파일(메타데이터상 파일 크기가 "-1") 제외한 다운로드 가능한 파일 리스트, 파일별 메타데이터 정보 포함

    for i in range(len(file)):
        if file[i][2] > 0: #크기가 "-1"이면 삭제된 파일
            downloadble_file.append(file[i])

    for i in range(len(downloadble_file)):
        print("[%d]" % (i + 1), downloadble_file[i][1])

    to_download = int(input("\n[System] >>> Type the number of file you wish to download: "))
    print("[System] >>> File: [%s] selected. Please wait" % downloadble_file[(to_download-1)][1])
    print("[System] >>> Downloading...")

    get_param = downloadble_file[(to_download-1)][3] #파일별 메타데이터 중 다운로드에 필요한 Param값인 "subject_uid" 및 "w" 획득

    s_filter = re.compile('(=)(.*?)(&w)')
    subject_uid = s_filter.findall(get_param)
    w_filter = re.compile('(w=)(.*?)($)')
    w = w_filter.findall(get_param)

    params = {
        '_notify_domain': 'www.dropbox.com',
        '_subject_uid': subject_uid[0][1],
        'w': w[0][1],
    }

    url = "https://www.dropbox.com/pri/get"+downloadble_file[(to_download-1)][1]+"?"
    response = requests.get(url, params=params, cookies=cookies, verify=False)

    filename = downloadble_file[(to_download-1)][1]
    finalname = filename.replace("/", "_")

    with open('Download/%s' % finalname, 'wb') as f: #파일 저장되는 경로 설정 필
        f.write(response.content)

    print("[System] >>> Download Completed")

def recursive_search_folder(fq_path, headers, cookies):
    global folder

    data = {"path": fq_path, "max_height": 1, "limit_sub_folder_count": 150}
    response = requests.post('https://www.dropbox.com/2/files/list_subfolders', headers=headers, cookies=cookies,
                             data=json.dumps(data), verify=False)

    result = json.loads(response.content)

    if len(result['subfolder_entries']) != 0:
        for i in range(len(result['subfolder_entries'])):
            folder.append(result['subfolder_entries'][i]['folder_metadata']['path_display'])
            recursive_search_folder(result['subfolder_entries'][i]['folder_metadata']['path_display'], headers, cookies)
            #해당 폴더에 하위 폴더가 존재하는 경우 재귀적으로 조회

    else:
        flag = 0

def recursive_search_file_continue(headers, cookies, cursor):
    file_folder_continue = []

    response_continue = requests.post('https://www.dropbox.com/2/files/browse_continue', headers=headers,
                                      cookies=cookies, data=json.dumps(cursor), verify=False)

    result_continue = response_continue.content
    result_continue_json = json.loads(result_continue)

    for i in range(len(result_continue_json['paginated_file_info'])):
        file_folder_continue.append([result_continue_json['paginated_file_info'][i]['file_info']['type'][".tag"],
                            result_continue_json['paginated_file_info'][i]['file_info']['fq_path'],
                            result_continue_json['paginated_file_info'][i]['file_info']['size_bytes'],
                            result_continue_json['paginated_file_info'][i]['file_info']['direct_blockserver_link'],
                            result_continue_json['paginated_file_info'][i]['file_info']['file_id'],
                            result_continue_json['paginated_file_info'][i]['file_info']['ns_id'],
                            result_continue_json['paginated_file_info'][i]['file_info']['sjid']])
                            #필요한 메타 정보만 가공한 최종 형태: [type][fq_path][size][link][file_id][ns_id][sjid] - 보완 예정

    for x in range(len(file_folder_continue)): #Type이 폴더는 제외한 파일만 가공하는 과정
        if file_folder_continue[x][0] == "file":
            global file
            file.append(file_folder_continue[x])

    if result_continue_json["has_more"] == True: #여전히 불러올 파일 목록이 있는 경우
        cursor_continue = {}
        cursor_continue["cursor"] = result_continue_json["next_request_voucher"]
        recursive_search_file_continue(headers, cookies, cursor_continue) #cursor값과 함께 재귀적으로 처리

def recursive_search_file(fq_path, headers, cookies):
    path = {"fq_path": fq_path, "include_deleted": True, "sort_type": {".tag": "files_by_name"},
            "sort_is_ascending": True}
    response = requests.post('https://www.dropbox.com/2/files/browse', headers=headers, cookies=cookies,
                             data=json.dumps(path), verify=False)
    result = json.loads(response.content)
    file_folder = [] #input으로 주어진 경로(fq_path/folder)에 존재하는 모든 파일/폴더가 담기는 리스트

    for i in range(len(result['paginated_file_info'])):
        file_folder.append([result['paginated_file_info'][i]['file_info']['type'][".tag"],
                        result['paginated_file_info'][i]['file_info']['fq_path'],
                        result['paginated_file_info'][i]['file_info']['size_bytes'],
                        result['paginated_file_info'][i]['file_info']['direct_blockserver_link'],
                        result['paginated_file_info'][i]['file_info']['file_id'],
                        result['paginated_file_info'][i]['file_info']['ns_id'],
                        result['paginated_file_info'][i]['file_info']['sjid']])
                        #필요한 메타 정보만 가공한 최종 형태: [type][fq_path][size][link][file_id][ns_id][sjid] - 보완 예정

    for x in range(len(file_folder)): #Type이 폴더는 제외한 파일만 가공하는 과정
        if file_folder[x][0] == "file":
            global file
            file.append(file_folder[x])

    if result['has_more'] == True: #해당 경로에 파일이 30개 이상인경우 별도 처리
        cursor = {}
        path_continue = result['next_request_voucher']
        cursor["cursor"] = path_continue
        recursive_search_file_continue(headers, cookies, cursor) #커서값과 함께 담당 재귀함수로 전달

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.dropbox.com/login")
    with page.expect_popup() as popup_info:
        page.locator("button:has-text(\"Apple로 로그인\")").click()
    page1 = popup_info.value
    page1.locator("input[type=\"text\"]").fill("ymaul2@korea.ac.kr")
    page1.locator("[aria-label=\"계속\"]").click()
    page1.locator("input[type=\"password\"]").fill("Alswldbsgh220@")
    page1.locator("[aria-label=\"로그인\"]").click()
    page1.locator("text=신뢰함").click()

    with page1.expect_navigation(): #2차인증 확인 후 브라우저에 직접 입력
        page1.locator("button:has-text(\"계속\")").click()
    page1.close()

    print("[System] >>> Login succeeded!")
    print("[System] >>> Acquring authentication information. Please wait...")

    page.goto("https://www.dropbox.com/")
    page.goto("https://www.dropbox.com/home")

    page.wait_for_timeout(10000) #HTML 로딩 기다리기 위함
    uid_html = page.query_selector_all("body > script") # 로그인 후 "/home" 에서 "X-Dropbox-Uid" 값 관련 태그에서 얻기 위함

    for i in range(len(uid_html)):
        if "constants/auth" and "user_id" in uid_html[i].inner_text():
            inner_text = """%s""" % uid_html[i].inner_text()
            uid_filter = re.compile('(: )(.*?)(})')
            uid_result = uid_filter.findall(inner_text)
            uid = uid_result[0][1]

    dropbox_cookies = page.context.cookies() #cookies 획득
    cookie_listing = []

    for i in range(len(dropbox_cookies)):
        cookie_listing.append((dropbox_cookies[i]['name'], dropbox_cookies[i]['value']))

    cookies = {} #필수쿠키
    essential_cookies = ["t", "jar", "lid", "bjar", "blid"] #필수쿠키 선별

    for i in range(len(cookie_listing)):
        if cookie_listing[i][0] in essential_cookies:
            cookies[cookie_listing[i][0]] = cookie_listing[i][1]

    token = cookies["t"] #획득한 쿠키 중 사용자 인증 담당하는 필수 헤더값에 필요한 값 별도 추출 후 아래에서 대입
    headers = {'X-CSRF-Token': '', 'X-Dropbox-Uid': '', 'Content-Type': 'application/json'} #필수 헤더
    headers['X-CSRF-Token'] = token
    headers['X-Dropbox-Uid'] = uid

    functions(headers, cookies) #controller

    # ---------------------
    context.close()
    browser.close()

def main():
    global folder
    folder = ['/']
    global file
    file = []

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with sync_playwright() as playwright:
        run(playwright)

if __name__ == '__main__':
    main()

