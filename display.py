import os
import sys
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
    columns = ["num"] + file_list[0]
    files = file_list[1:]
    print()
    print("======DRIVE_FILE_LIST======")
    print("FILE_COUNT:", len(files))
    print(f"{columns[0]:>5} | {columns[1]:<60} | {columns[2]:^10} | {columns[3]:^10} | {columns[4]:^10} | {columns[5]:^20} | {columns[6]:^20}")
    for cnt, file in enumerate(files, start = 1):
        print(f"{cnt:>5} | {file[0]:<60} | {str(file[1]):^10} | {str(file[2]):^10} | {str(file[3]):^10} | {str(file[4]):^20} | {str(file[5]):^20}")


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









