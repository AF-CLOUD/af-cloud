### Dropbox openAPI 약식 Standalone 버전 ###
### 추후 통합된 "FACT_CORE" form에 맞춰서 편입 예정 ###

import dropbox
from tqdm import tqdm

def select_mode(dbx, folder_list, file_list, deleted_file_list): #현재는 파일 목록만 운용
    while True:
        print("""

        <Select Mode>
        1.Show File List
        2.File Download
        3.Show File History
        4.Search File
        5.Terminate

        """)

        try:
            mode = int(input("[System] >>> Select Mode: "))
            if mode == 1:
                print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡList of Filesㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")

                for i in range(len(file_list)):
                    print("[%d]" % (i + 1), file_list[i].name)  # List of All Files

            if mode == 2:
                path_to_download = "./download/" #임시 경로

                for x in range(len(file_list)):
                    print("[%d]" % (x + 1), file_list[x].name)  # List of All Files

                to_download = int(input("\n[System] >>> Type the number of file you wish to download: "))

                with open(path_to_download + file_list[to_download-1].name, 'wb') as f:
                    metadata, result = dbx.files_download(path=file_list[to_download-1].path_display)
                    f.write(result.content)

            if mode == 3:
                get_file_history(dbx, file_list)

            if mode == 4:
                file_search(dbx)
                print("hi")

        except Exception as e:

            print("[System] >>> Error occurred or Invalid input. Please try again?")
            print("[System] >>> Error:", e)


def get_thumbnail(dbx, file_list): #태생적 한계...? 500개까지밖에 못불러와짐
    path_to_download = "./thumbnail/" #임시 경로
    thumbnail_ext = ["jpg", "jpeg", "png", "tiff", "tif", "gif", "webp", "ppm", "bmp"] #지원되는 extensions

    for x in tqdm(range(len(file_list))):
        ext = file_list[x].name[-3:]
        exts = file_list[x].name[-4:]

        if ext in thumbnail_ext:
            with open(path_to_download+file_list[x].name, "wb") as f:
                result = dbx.files_get_thumbnail_to_file(download_path=path_to_download+file_list[x].name, path=file_list[x].path_display)

        else:
            if exts in thumbnail_ext:
                with open(path_to_download + file_list[x].name, "wb") as f:
                    result = dbx.files_get_thumbnail_to_file(download_path=path_to_download + file_list[x].name, path=file_list[x].path_display)

def get_file_metadata(dbx): #파일 개수 500개까지밖에 못불러옴...다른 방법이 있을까?
    folders, files, deleted = [], [], []
    for entry in dbx.files_list_folder('',
                                       recursive=True,
                                       include_media_info=True,
                                       include_deleted=True,
                                       include_has_explicit_shared_members=True,
                                       include_mounted_folders=True,
                                       limit=None,
                                       shared_link=None,
                                       include_property_groups=None,
                                       include_non_downloadable_files=True).entries:
        if isinstance(entry, dropbox.files.FolderMetadata): # content is folder
            folders.append(entry)
        elif isinstance(entry, dropbox.files.FileMetadata): # content is file
            files.append(entry)
        elif isinstance(entry, dropbox.files.DeletedMetadata):
            deleted.append(entry)

    return folders, files, deleted

#FolderMetadata(id='id:HUm7p2N71_cAAAAAAAAADw', name='inside_folder', parent_shared_folder_id=NOT_SET, path_display='/test_folder/inside_folder', path_lower='/test_folder/inside_folder', property_groups=NOT_SET, shared_folder_id=NOT_SET, sharing_info=NOT_SET)
#FileMetadata(client_modified=datetime.datetime(2022, 3, 29, 11, 5, 16), content_hash='954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4', export_info=NOT_SET, file_lock_info=NOT_SET, has_explicit_shared_members=False, id='id:HUm7p2N71_cAAAAAAAAABg', is_downloadable=True, media_info=NOT_SET, name='test.txt', parent_shared_folder_id=NOT_SET, path_display='/test_folder/test.txt', path_lower='/test_folder/test.txt', property_groups=NOT_SET, rev='5db5d52effcd698132cc1', server_modified=datetime.datetime(2022, 3, 29, 15, 45, 53), sharing_info=NOT_SET, size=4, symlink_info=NOT_SET)
#DeletedMetadata(name='test_deleted.hwp', parent_shared_folder_id=NOT_SET, path_display='/test_deleted.hwp', path_lower='/test_deleted.hwp')


def get_file_list(dbx): #메타데이터 조회 API로 기능 대체 가능 / 현재 안씀
    res = dbx.files_list_folder("", recursive=True,
                                include_media_info=False,
                                include_deleted=True,
                                include_has_explicit_shared_members=True,
                                include_mounted_folders=True,
                                limit=None,
                                shared_link=None,
                                include_property_groups=None,
                                include_non_downloadable_files=True)

    return res

def get_file_history(dbx, file_list): #히스토리 잘 불러와짐, 파일 버전별 수집 시 매뉴얼대로 했음에도 버전마다 수집이 잘 되는애가 있고 안되는 애가 있음... 원인 불명

    revisionable_file = []

    for i in range(len(file_list)):
        path = file_list[i].path_display
        res = dbx.files_list_revisions(path=path, limit=50) #limit = the maximum number of revision entries returned
        if len(res.entries) != 1:
            revisionable_file.append(res)

    for x in range(len(revisionable_file)):
        print("[%d] '%s' file has %d revisions " %(x+1, (revisionable_file[x].entries[0]).path_display, len(revisionable_file[x].entries)))

    mode = input("[System] >>> Wish to download? (y/n)")

    if mode == "y" or "Y":
        for x in range(len(revisionable_file)):
            print("[%d] '%s'" % (x+1, (revisionable_file[x].entries[0]).path_display))

    select_file = int(input("[System] >>> Select number: "))

    try:
        for y in range(len(revisionable_file[select_file-1].entries)):
            with open("[Ver.%d]%s" % (y, revisionable_file[select_file-1].entries[0].name), "wb") as f:
                print("rev:%s" % (revisionable_file[select_file - 1].entries[y]).rev)
                metadata, result = dbx.files_download("rev:%s" % (revisionable_file[select_file - 1].entries[y]).rev)
                f.write(result.content)

    except:
        pass

def file_search(dbx): #String Matching 방식만 지원
    q = input("[System] >>> Input keyword: ") #ex)keyword(변수 "q")="rev" 이라면 "revision.test"같은 파일이 Match
    res = dbx.files_search_v2(q)
    #res.matches = SearchMatchV2(highlight_spans=NOT_SET, match_type=SearchMatchTypeV2('filename', None), metadata=MetadataV2('metadata', FolderMetadata(id='id:U4ar6Q4tWtgAAAAAAAAAkQ', name='revision_test', parent_shared_folder_id=NOT_SET, path_display='/revision_test', path_lower='/revision_test', property_groups=NOT_SET, shared_folder_id=NOT_SET, sharing_info=NOT_SET)))

def main():
    token = input("[System] >>> Input token: ")
    dbx = dropbox.Dropbox(token)
    #res = get_file_list(dbx) #파일 목록 조회는 아래 "메타데이터 조회 API"로 대체(사유: 삭제된 애들의 메타데이터까지 한번에 불러올 수 있음)
    folders, files, deleted = get_file_metadata(dbx)
    get_thumbnail(dbx, files)
    select_mode(dbx, folders, files, deleted)

if __name__ == '__main__':
    main()
