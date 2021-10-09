# coding: utf-8

from __future__ import print_function, unicode_literals
import os
from boxsdk import Client
from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole
from auth import authenticate
from boxsdk import OAuth2

def login_with_accesstoken(_access_token):
    CLIENT_ID = 'fkelzqoye3hqsv4h2mr63h518aw05okz'  # Insert Box client ID here
    CLIENT_SECRET = '4dcWL6WpDYsPNEhO7YDB4qBM6C0CUkAN'  # Insert Box client secret here
    
    oauth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token =_access_token
    )
    return oauth


def run_user_example(client):
    # 'me' is a handy value to get info on the current authenticated user.
    me = client.user(user_id='me').get(fields=['login'])
    print('The email of the user is: {0}'.format(me['login']))


def run_folder_examples(client):
    root_folder = client.folder(folder_id='0').get()
    print('The root folder is owned by: {0}'.format(root_folder.owned_by['login']))

    items = root_folder.get_items()
    print('in the root folder:')
    for item in items:
        print("   " + item.name)
        #item.type == folder일 경우 깊이 내려가서 탐색 필요

def run_examples(oauth):

    client = Client(oauth)

    run_user_example(client)
    run_folder_examples(client)


def main():

    # Please notice that you need to put in your client id and client secret in demo/auth.py in order to make this work.
    loginmode = 'login'
    if loginmode is 'token':
        loginflag=0
    elif loginmode is 'login':
        loginflag=1
    if loginflag:
        oauth, _, _ = authenticate() #real login with ID/PW
    else: 
        oauth=login_with_accesstoken('Y0Mwa2nvrZjSgfWNBdFswfJBneFkPdd7') # access token 
    run_examples(oauth)
    
    os._exit(0)

if __name__ == '__main__':
    main()

