from onedrive_collector.collector import *
import module.Cloud_Display as cd

class OneDrive_connector:
    def __init__(self):
        pass

    def excute(self, credential):
        PRINTI("Start OneDrive Module")

        a, a_result = self.__call_auth(credential)
        if a_result == FC_ERROR:
            PRINTI("OneDrive Authentication ERROR")
            return FC_ERROR

        e, e_result = self.__call_explorer(a)
        if e_result == FC_ERROR:
            PRINTI("OneDrive Exploration ERROR")
            return FC_ERROR

        c_result = self.__call_collector(e, a)
        if c_result == FC_ERROR:
            PRINTI("OneDrive Collector ERROR")
            return FC_ERROR

        PRINTI("End OneDrive Module")

    @staticmethod
    def __call_auth(credential):
        PRINTI("OneDrive Authentication .... Start")
        auth_data = Authentication(credential=credential)
        a_result = auth_data.run()
        PRINTI("OneDrive Authentication .... End")
        return auth_data, a_result

    @staticmethod
    def __call_explorer(auth_data):
        PRINTI("OneDrive Exploration .... Start")
        e = Exploration(auth_data)
        e_result = e.run()
        PRINTI("OneDrive Exploration .... End")
        return e, e_result

    @staticmethod
    def __call_collector(onedrive_data, auth_data):
        c = Collector(onedrive_data, auth_data)
        file_len = c.get_num_of_file_list()
        c.set_file_list()
        while True:
            menu = cd.select_menu()
            if menu == 0:  # exit
                break
            elif menu == 1:  # all of file
                c.show_file_list()
            elif menu == 2:  # select file
                c.show_file_list()
                file_len = c.get_num_of_file_list()
                while True:
                    download_number = int(input("Put file numbers (exit:0): "))
                    if download_number == 0:
                        break

                    if download_number < 0:
                        print("\n Please put correct number.")
                        continue
                    elif download_number > file_len:
                        print("Please put correct number.")
                        continue
                    c.download_file(download_number)
            elif menu == 3:  # search thumbnail
                q = input("What do you want to search for? >> ")
                c.search_file(q)
            else:
                print(" [!] Invalid Menu. Choose Again.")
                continue