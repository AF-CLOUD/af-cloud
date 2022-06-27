from mega_collector.collector import *
import module.Cloud_Display as cd

class MEGA_connector:
    def __init__(self):
        pass

    def excute(self, credential):
        PRINTI("Start MEGA Module")

        a, a_result = self.__call_auth(credential)
        if a_result == FC_ERROR:
            PRINTI("MEGA Authentication ERROR")
            return FC_ERROR

        c_result = self.__call_collector(a)
        if c_result == FC_ERROR:
            PRINTI("MEGA Collector ERROR")
            return FC_ERROR

        PRINTI("End MEGA Module")

    @staticmethod
    def __call_auth(credential):
        PRINTI("MEGA Authentication .... Start")
        auth_data = Authentication_with_Exploration(credential=credential)
        a_result = auth_data.run()
        PRINTI("MEGA Authentication .... End")
        return auth_data, a_result

    @staticmethod
    def __call_collector(mega_data):
        c = Collector(mega_data)
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
            elif menu == 3:  # search
                sm = cd.search_menu()
                s_input = CInput()
                if sm == 0:
                    continue
                elif sm == 1:
                    q = input("What do you want to search for? >> ")
                    c.search_file(q)
                elif sm == 2:
                    search_period = s_input.set_m_period()
                    if search_period[0] and search_period[1]:
                        if search_period[0] != '1970-01-01':
                            re_start_time = datetime.datetime.strptime(search_period[0],
                                                                       "%Y-%m-%d") - datetime.timedelta(days=1)
                            re_start_time = re_start_time.strftime("%Y-%m-%d")
                        else:
                            re_start_time = search_period[0]
                        s_period = re_start_time
                        e_period = search_period[1]
                        c.search_file_by_date(s_period, e_period)
            else:
                print(" [!] Invalid Menu. Choose Again.")
                continue