from turtle import down
from httplib2 import Credentials
from box_collector import authenticator
from box_collector import collector
from box_collector import explorer
import module.Cloud_Display as cd
from module import FACT_Cloud_Define
class Box_connector:
    def __init__(self):
        self.e_result=None
    
    def __call_auth(self, credential):
        print("Box authentication Start")
        auth_data = authenticator.Authentication(credential=credential)
        a_result = auth_data.run()
        print("Box authentication End")
        return a_result
    
    def __call_explorer(self, auth_data):
        print("Box Exploration .... Start")
        e = explorer.Exploration(auth_data)
        self.e_result = e.run()
        print("Box Exploration .... End")
        return self.e_result

    def __call_collector(self, e_result, auth_data):
        print("Box Collector Start...")
        c = collector.Collector(auth_data, e_result)
        file_len = c.get_num_of_file_list()
        while True:
            menu = cd.select_menu()
            if menu == 0:
                break
            elif menu ==1: #view all file list
                c.show_file_list()
            elif menu ==2: #view all file list & select file and download
                c.show_file_list()
                while True:
                    download_number = int(input("PUT File numbers : (exit:0)  :"))
                    if download_number==0:
                        break
                    if download_number <0:
                        print("\n please put correct number. ")
                        continue
                    elif download_number > file_len:
                        ("\n please put correct number. ")
                        continue
                    c.download_file(download_number)

            elif menu ==3:
                sm = cd.search_menu()
                s_input = FACT_Cloud_Define.CInput()
                if sm==0:
                    continue
                elif sm ==1:
                    q= input("What do you want to search for? >>")
                    c.search_file(q)





    def excute(self, credential):
        print("Start Box Module")
        # if self.__flag==0:
        a_result = self.__call_auth(credential) #return authentication data
        self.e_result = self.__call_explorer(a_result) #return metadata list for box file
        c_result = self.__call_collector(self.e_result, a_result)



if __name__=="__main__":
    # login with open api and parsing Box data!
    credential = ["kyn0503121@korea.ac.kr","forensic4738"]
    playBox = Box_connector()
    oauth = playBox.excute(credential)

    
    
    