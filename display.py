import os, sys
from API_GoogleCloud import GDrive
from termcolor import colored
from pyfiglet import Figlet


def start_display():
    os.system('cls')
    f = Figlet(font='big')
    print(colored(f.renderText('AF'), 'red'))
    f = Figlet(font='big')
    print(colored(f.renderText('CLOUD'), 'yellow'))
    # f = Figlet(font='banner')
    # print(colored(f.renderText('CLOUD'), 'red'))


def show_driveinfo(driveinfo):
    print("=======================INFO========================")
    print("|--ACCESS_TOKEN---->", driveinfo['access_token'])
    print("|--REFRESH_TOKEN--->", driveinfo['refresh_token'])
    print("|--REDIRECT_URI---->", driveinfo['redirect_uri'])
    print("|--CLIENT_SECRET--->", driveinfo['client_secret'])
    print("|----CLIENT_ID----->", driveinfo['client_id'])
    print("|----AUTH_CODE----->", driveinfo['auth_code'])
    print("|----AUTH_URL------>", driveinfo['auth_url'])
    print("===================================================")


def start_menu():
    print()
    print("###########################")
    print("######### M.E.N.U #########")
    print("###########################")
    print("#    0. EXIT              #")
    print("#    1. SHOW_FILE_LIST    #")
    print("#    2. SEARCH_FILE       #")
    #print("#    3. DOWNLOAD_FILE     #")
    print()


def select_menu():
    num = int(input("Select Menu: "))
    return num


def cloud_type():
    print("###########################")
    print("######## C.L.O.U.D ########")
    print("###########################")
    print("#    1. Google Drive      #")
    print("#    2. OneDrive          #")
    print("#    3. Dropbox           #")
    print("#    4. Box               #")
    print("#    5. MEGA              #")
    print()
    cloud = int(input("Select Cloud Type: "))
    if cloud > 5:
        print(" [!!] You Can input number range(1 ~ 5)")
        print(" [!!] Try Again")
        sys.exit()
    else:
        return cloud


def login_data():
    print()
    print("###########################")
    print("######## E.N.T.E.R ########")
    print("###### ID & Password ######")
    print("###########################")
    print()
    id = input("Username: ")
    pw = input("Password: ")
    print()


def show_file_list(file_list):
    """
        수정 필요함
    :param file_list:
    :return:
    """
    # columns = file_list[0][1:]
    print()
    print("======DRIVE_FILE_LIST======")
    print("FILE_COUNT:", len(file_list) - 1)
    # print("%-7s" % "Number"
    #       + "%-60s" % "| %s" % columns[0]
    #       + "%-10s" % "| %s" % columns[1]
    #       + "%-10s" % "| %s" % columns[2]
    #       + "%-10s" % "| %s" % columns[3])

    for cnt, file in enumerate(file_list):
        # if file[1] == "TRUE":
        #     file[1] = "Shared"
        # else:
        #     file[2] = "Non-Shared"
        #
        # if file[3] == "TRUE":
        #     file[3] = "Deleted"
        # else:
        #     file[3] = "Live"

        print(f"{cnt:>5} | {file[0]:<60} | {str(file[1]):^5} | {str(file[2]):^5} | {str(file[3]):^5} | {str(file[4]):^10}")


# def search_file_list(file_list):
#     word = input("Keyword: ")
#     cnt = 0
#     for i in file_list:
#         if word in i[1]:
#             cnt += 1
#             if cnt == 1:
#                 print()
#                 print('=======FIND COMPLETE=======')
#             print(i[1])
#     print()
#     print("Total:", cnt)


# def search_with_keyword():
#     print()
#     keyword = input("Input your Keyword: ")
#     return keyword

# def search_with_period():
#     period = []
#     print()
#     keyword = input("Input your Keyword: ")
#     print()
#     print("###########################")
#     print("###### E.X.A.M.P.L.E ######")
#     print("##  2021-06-04T00:00:00  ##")
#     print("###########################")
#     print()
#     period.append(input("Input the Start Time Point: "))
#     period.append(input("Input the End Time Point: "))
#     return keyword, period

# def search_type():
#     print()
#     print("###########################")
#     print("######### M.E.N.U #########")
#     print("###########################")
#     print("#    1. Period            #")
#     print("#    2. Keyword           #")
#     print()
#
#     num = int(input("Select Menu: "))
#     return num


def download_item(file_list, dl_item, dl_path):
    print()
    print("=====DOWNLOAD COMPLETE=====")
    print(dl_path + "\\" + (file_list[dl_item][1]))


def invalid_menu():
    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!     Invalid Menu    !!!")
    print("!!!     Choose Again    !!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")









