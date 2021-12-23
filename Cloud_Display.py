import os
import sys
from termcolor import colored
from pyfiglet import Figlet
import pytz
import dateutil.parser
import tabulate

tabulate.WIDE_CHARS_MODE = True


def start_tool():
    os.system('cls')
    f = Figlet(font='big')
    print(colored(f.renderText('< FACT >\n                        - CLOUD'), 'blue'))
    print(colored("[Police-Lab 2.0] Research on Data Acquisition and Analysis for Counter Anti-Forensics\n\n", 'blue'))


def select_cloud():
    print("###########################")
    print("######## C.L.O.U.D ########")
    print("###########################")
    print("#    1. GOOGLE DRIVE      #")
    print("#    2. ONEDRIVE          #")
    print("#    3. DROPBOX           #")
    print("#    4. BOX               #")
    print("#    5. MEGA              #")
    print()
    cloud = input("Select Cloud Type: ")
    return cloud


def select_menu():
    print()
    print("###########################")
    print("######### M.E.N.U #########")
    print("###########################")
    print("#    0. EXIT              #")
    print("#    1. SHOW_FILE_LIST    #")
    print("#    2. SEARCH_FILE       #")
    print()
    num = input("Select Menu: ")
    return num


def show_file_list(file_list):
    local_timezone = pytz.timezone('Asia/Seoul')
    new_list = list()
    cnt = 0
    for f in file_list:
        if cnt != 0:
            created_date = dateutil.parser.parse(f[4])
            modified_date = dateutil.parser.parse(f[5])
            f[4] = created_date.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%Y-%m-%d %H:%M:%S")
            f[5] = modified_date.replace(tzinfo=pytz.utc).astimezone(local_timezone).strftime("%Y-%m-%d %H:%M:%S")
        cnt += 1
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


def show_credential_info(info):
    print("=======================INFO========================")
    print("|--ACCESS_TOKEN---->", info['access_token'])
    print("|--REFRESH_TOKEN--->", info['refresh_token'])
    print("|--REDIRECT_URI---->", info['redirect_uri'])
    print("|--CLIENT_SECRET--->", info['client_secret'])
    print("|----CLIENT_ID----->", info['client_id'])
    print("|----AUTH_CODE----->", info['auth_code'])
    print("|----AUTH_URL------>", info['auth_url'])
    print("===================================================")


def login_data():
    print()
    print("###########################")
    print("######## E.N.T.E.R ########")
    print("###### ID & Password ######")
    print("###########################")
    print()
    id = input("Username: ")
    pw = input("Password: ")
    return id, pw













