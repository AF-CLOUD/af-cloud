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

        c_result = self.__call_collector(e)
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
    def __call_collector(onedrive_data):
        c = Collector(onedrive_data)
        while True:
            menu = cd.select_menu()
            if menu == 0:  # exit
                break
            elif menu == 1:  # all of file
                c.show_file_list()
            elif menu == 2:  # select file
                a = 1
            elif menu == 3:  # extract thumbnail
                a = 1
            else:
                print(" [!] Invalid Menu. Choose Again.")
                continue