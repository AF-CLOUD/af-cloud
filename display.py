import os
import sys
from termcolor import colored
from pyfiglet import Figlet
import tabulate

tabulate.WIDE_CHARS_MODE = True


def start_display():
    os.system('cls')
    f = Figlet(font='big')
    print(colored(f.renderText('< FACT >\n                        - CLOUD'), 'blue'))
    print(colored("[Police-Lab 2.0] Research on Data Acquisition and Analysis for Counter Anti-Forensics\n\n", 'blue'))




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
    num = input("Select Menu: ")
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
    new_list = list()
    for f in file_list:
        if len(f[0]) >= 20:
            tmp = f[0]
            f[0] = f[0][:20] + '....'
            new_list.append((f[:6]))
            f[0] = tmp
        else:
            new_list.append((f[:6]))

    file_count = len(file_list)
    print()
    print("======DRIVE_FILE_LIST======")
    print("FILE_COUNT:", file_count - 1)
    print(tabulate.tabulate(new_list, headers="firstrow", tablefmt='github', showindex=range(1, file_count)))


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









