from module.FACT_Cloud_Define import *

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
    print("#    2. DOWNLOAD_FILE     #")
    print("#    3. SEARCH_FILE       #")
    print()
    num = input("Select Menu: ")
    return int(num)


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
    print(tabulate.tabulate(new_list, headers="firstrow", tablefmt='github', showindex=range(1, file_count),
                            numalign="left"))


def show_file_list_onedirve(file_list):
    new_list = []
    print('======ONEDRIVE_FILE_LIST======')
    print('FILE_COUNT:', len(file_list) - 1)

    for id, file, f, created_time, modified_time, size, path in file_list:
        if created_time is None:
            created_time = '-'
        elif type(created_time) == datetime.datetime:
            created_time = created_time + datetime.timedelta(hours=9)

        if modified_time is None:
            modified_time = '-'
        elif type(modified_time) == datetime.datetime:
            modified_time = modified_time + datetime.timedelta(hours=9)

        if path is None:
            path = '-'

        new_list.append([file, f, created_time, modified_time, size, path])

    print(tabulate.tabulate(new_list, headers="firstrow", tablefmt='github', showindex=range(1, len(file_list)),
                            numalign="left"))


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
    id = input("Input User ID: ")
    pw = input("Input Password: ")
    return id, pw
