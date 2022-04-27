from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import json
import re

folder = ['/']
file = []

def file_download(file, cookies):
    #삭제된파일(크키-1) 안보이게끔 처리해야함
    for i in range(len(file)):
        print("[%d]" % (i + 1), file[i][1])

    to_download = int(input("Type the Number of File you wish to download: >>>"))

    get_param = file[(to_download-1)][3] #subject_uid & w

    s_filter = re.compile('(=)(.*?)(&w)')
    subject_uid = s_filter.findall(get_param)
    w_filter = re.compile('(w=)(.*?)($)')
    w = w_filter.findall(get_param)

    params = {
        '_notify_domain': 'www.dropbox.com',
        '_subject_uid': subject_uid[0][1],
        'w': w[0][1],
    }

    url = "https://www.dropbox.com/pri/get"+file[(to_download-1)][1]+"?"

    response = requests.get(url, params=params, cookies=cookies, verify=False)

    filename = file[(to_download-1)][1]
    finalname = filename.replace("/", "_")

    with open('Download/%s' % finalname, 'wb') as f:
        f.write(response.content)

    print("Download Completed")

    while True:
        try:
            continue_download = input("Download more? (y/n)")

            if continue_download == "y":
                return continue_download

            elif continue_download =="n":
                return continue_download

            else:
                print("Try again")

        except Exception as e:
            print(e)


def recursive_search_folder(fq_path, headers, cookies):
    #foldernames = 해당 경로의 fq_path들 복수니까 여기서 request받아와야함
    foldernames = subfolder(fq_path, headers, cookies) #현재 경로에 하위 폴더들이 담긴 리스트 형태로 존재
    for path in foldernames:
        if path != []:
            subfolder(path, headers, cookies)
        else:
            flag = 0

def recursive_search_file(fq_path, headers, cookies):
    path = {"fq_path": fq_path, "include_deleted": True}
    response = requests.post('https://www.dropbox.com/2/files/browse', headers=headers, cookies=cookies,
                             data=json.dumps(path), verify=False)
    result = json.loads(response.content)
    file_folder = []

    for i in range(len(result['paginated_file_info'])):
        file_folder.append([result['paginated_file_info'][i]['file_info']['type'][".tag"],
                        result['paginated_file_info'][i]['file_info']['fq_path'],
                        result['paginated_file_info'][i]['file_info']['size_bytes'],
                        result['paginated_file_info'][i]['file_info']['direct_blockserver_link'],
                        result['paginated_file_info'][i]['file_info']['file_id'],
                        result['paginated_file_info'][i]['file_info']['ns_id'],
                        result['paginated_file_info'][i]['file_info']['sjid']])
                        #[type][fq_path][size][link][file_id][ns_id][sjid]

    for i in range(len(file_folder)):
        if file_folder[i][0] == "file":
            file.append(file_folder[i])

def subfolder(fq_path, headers, cookies):

    data = {"path": fq_path, "max_height": 1, "limit_sub_folder_count": 150}
    response = requests.post('https://www.dropbox.com/2/files/list_subfolders', headers=headers, cookies=cookies,
                             data=json.dumps(data), verify=False)

    result = json.loads(response.content)
    fq_paths = []
    for i in range(len(result['subfolder_entries'])):
        fq_paths.append(result['subfolder_entries'][i]['folder_metadata']['path_display'])
        folder.append(result['subfolder_entries'][i]['folder_metadata']['path_display'])

    return fq_paths

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
    #page1.locator("input[type=\"text\"]").fill("AF.Cloud.2021@gmail.com")

    # Click [aria-label="계속"]
    page1.locator("[aria-label=\"계속\"]").click()

    # Fill input[type="password"]
    page1.locator("input[type=\"password\"]").fill("Alswldbsgh220@")
    #page1.locator("input[type=\"password\"]").fill("Dfrc4738!@#")

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

    dropbox_cookies = page.context.cookies()

    cookie_listing = []

    for i in range(len(dropbox_cookies)):
        cookie_listing.append((dropbox_cookies[i]['name'], dropbox_cookies[i]['value']))

    cookies = {}
    essential_cookies = ["t", "jar", "lid", "bjar", "blid"]

    for i in range(len(cookie_listing)):
        if cookie_listing[i][0] in essential_cookies:
            cookies[cookie_listing[i][0]] = cookie_listing[i][1]

    token = cookies["t"]
    headers = {'X-CSRF-Token': '', 'X-Dropbox-Uid': '1215469809', 'Content-Type': 'application/json'}
    headers['X-CSRF-Token'] = token

    while True:
        print("""

        <Select Mode>
        1.File Browser & Download
        2.Terminate

        """)

        try:
            mode = int(input(">>>"))
            if mode == 1:
                print("File Browsing Start")
                recursive_search_folder("", headers, cookies)

                for i in range(len(folder)):
                    recursive_search_file(folder[i], headers, cookies)

                print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡList of Filesㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

                for i in range(len(file)):
                    print(file[i])

                sec_mode = input("\nWish to download files? (y/n)\n")

                if sec_mode == "y":
                    status = file_download(file, cookies)

                    if status == "y":
                        file_download(file, cookies)

                    elif status =="n":
                        break

            if mode == 2:
                print("File Browsing Terminated")
                break

        except Exception as e:

            print("[System] >>> Invalid input. Please check again?")
            #print(e)

    # ---------------------
    context.close()
    browser.close()

def main():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == '__main__':
    main()

