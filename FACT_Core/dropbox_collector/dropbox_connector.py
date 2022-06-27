from dropbox_collector.collector import *
import module.Cloud_Display as cd

class Dropbox_connector():
    def __init__(self):
        pass

    def excute(self, credential):
        PRINTI("Start Dropbox Module")

        a, a_result = self.__call_auth(credential)
        if a_result == FC_ERROR:
            PRINTI("Dropbox Authentication ERROR")
            return FC_ERROR

        e, e_result = self.__call_explorer(a)
        if e_result == FC_ERROR:
            PRINTI("Dropbox Exploration ERROR")
            return FC_ERROR

        c_result = self.__call_collector(e, a)
        if c_result == FC_ERROR:
            PRINTI("Dropbox Collector ERROR")
            return FC_ERROR

        PRINTI("End Dropbox Module")

    @staticmethod
    def __call_auth(credential):
        PRINTI("Dropbox Authentication .... Start")
        auth_data = Authentication_dropbox(credential=credential)
        a_result = auth_data.run()
        PRINTI("Dropbox Authentication .... End")
        return auth_data, a_result

    @staticmethod
    def __call_explorer(auth_data):
        PRINTI("Dropbox Exploration .... Start")
        e = Exploration(auth_data)
        e_result = e.run()
        PRINTI("Dropbox Exploration .... End")
        return e, e_result

    @staticmethod
    def __call_collector(dropbox_data, auth_data):
        c = Collector(dropbox_data, auth_data)
        file_list = dropbox_data.get_file_list()
        cookies = auth_data.cookies()
        revisionable_file = dropbox_data.get_revisionable_file()

        while True:
            print("""

            <Select Mode>
            1.File Browser - All Files
            2.File Download
            3.File Browser - Files with revisions
            4.File Download - Files with revisions
            5.Terminate

            """)

            try:
                mode = int(input("[Type Number] >>> "))
                if mode == 1:
                    print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡList of Filesㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")

                    for i in range(len(file_list)):
                        print("[%d]" % (i + 1), file_list[i][1])  # List of All Files

                if mode == 2:
                    try:
                        while True:
                            sec_mode = input(
                                "\n[System] >>> Wish to download files? (y/n)\n")  # 파일 다운로드 - 로컬에서 저장경로 설정 필

                            if sec_mode == "y":
                                c.file_download(file_list, cookies)  # 파일 다운로드 - 로컬에서 저장경로 설정 필

                            elif sec_mode == "n":
                                break

                            else:
                                print("[System] >>> Invalid input. Please try again")

                    except Exception as e:
                        print("[System] >>> Invalid input or error occurred. Please try again")

                if mode == 3:
                    if len(revisionable_file) == 0:
                        print("[System] >>> There is no file with revisions")

                    else:
                        print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡList of Files with revisionsㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
                        for i in range(len(revisionable_file)):
                            print("[%d]" % (i + 1), revisionable_file[i][0][1])  # List of revisionable Files

                if mode == 4:
                    if len(revisionable_file) == 0:
                        print("[System] >>> There is no file with revisions")

                    else:
                        while True:
                            mode = input("\n[System] >>> Wish to download files? (y/n)\n")

                            if mode == "y" or "Y":
                                c.file_revisions_download(revisionable_file, cookies)

                            if mode == "n" or "N":
                                break

                            else:
                                print("[System] >>> Invalid input. Please try again")

                if mode == 5:
                    print("[System] >>> Terminated")
                    break

            except Exception as e:

                print("[System] >>> Error occurred or Invalid input. Please try again?")
                print("[System] >>> Error:", e)
