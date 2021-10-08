from mega import Mega
import pprint
import base64

# Mega.py의 인스턴스 생성
mega = Mega()

# Mega 로그인
m = mega.login("kim_3738@korea.ac.kr", "dfrc4738!@#")

# 사용자 세부 정보 가져오기
details = m.get_user()

# 계정 잔액 가져오기(Pro 계정만 해당)
# balance = m.get_balance()

# 계정 디스크 할당량 가져오기
quota = m.get_quota()

# 계정 저장소 공간 가져오기
space = m.get_storage_space(kilo=True)

# 계정 파일 가져오기
files = m.get_files()


# 파일 업로드 및 공개 링크 가져오기
# file = m.upload('myfile.doc')
# m.get_upload_link(file)
# see mega.py for destination and filename options


# 파일 또는 폴더 내보내기
# public_exported_web_link = m.export('myfile.doc')
# public_exported_web_link = m.export('my_mega_folder/my_sub_folder_to_share')
# e.g. https://mega.nz/#F!WlVl1CbZ!M3wmhwZDENMNUJoBsdzFng


# 파일 또는 폴더 찾기
# folder = m.find('my_mega_folder')
# Excludes results which are in the Trash folder (i.e. deleted)
# folder = m.find('my_mega_folder', exclude_deleted=True)


# 대상 폴더에 파일 업로드
# folder = m.find('my_mega_folder')
# m.upload('myfile.doc', folder[0])


# URL 또는 파일 obj에서 파일 다운로드, 선택적으로 대상 폴더 지정
# file = m.find('myfile.doc')
# m.download(file)
# m.download_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')
# m.download(file, '/home/john-smith/Desktop')
# specify optional download filename (download_url() supports this also)
# m.download(file, '/home/john-smith/Desktop', 'myfile.zip')


# URL에서 파일 가져오기, 선택적으로 대상 폴더 지정
# m.import_public_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')
# folder_node = m.find('Documents')[1]
# m.import_public_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc', dest_node=folder_node)


# 폴더 만들기
# m.create_folder('new_folder')
# m.create_folder('new_folder/sub_folder/subsub_folder')

# Returns a dict of folder node name and node_id, e.g. (폴더 노드 이름 및 node_id(예: node_id)의 받아쓰기를 반환)
# {
#   'new_folder': 'qpFhAYwA',
#   'sub_folder': '2pdlmY4Z',
#   'subsub_folder': 'GgMFCKLZ'
# }


# 파일 또는 폴더 이름 바꾸기
# file = m.find('myfile.doc')
# m.rename(file, 'my_file.doc')


# print(details)
# print(quota)
# print(space)
print(files)

# for key1, value1 in files.items():
#     print(key1)
#     print(value1)
#     print('____________')

pprint.pprint(files)

for key1, value1 in files.items():
    for key2, value2 in value1.items():
        if key2 == 'a':
            for key3, value3 in value2.items():
                if key3 == 'n':
                    print(value3.encode().decode('utf-8').encode('latin1').decode('utf-8'))
                    # print(value3.encode().decode('utf-8').encode('latin1').decode('utf-8'))

                    # fixed = bytes.fromhex(value3)
                    # print(value3.decode('utf-8').encode('latin1').decode('utf-8'))
