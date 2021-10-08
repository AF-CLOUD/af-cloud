from __future__ import unicode_literals

import onedrivesdk_fork as onedrivesdk
from onedrivesdk_fork.helpers import GetAuthCodeServer
from PIL import Image
import os,sys


def navigate(client, item_id):
    items = client.item(id=item_id).children.get()
    return items


def list_changes(client, item_id, token):
    collection_page = client.item(id=item_id).delta(token).get()
    print("TOKEN: {}".format(collection_page.token))
    print("=====OneDrive list=====Count:",len(collection_page))
    for item in collection_page:
        print(item.name)
    print("=======================")

input = getattr(__builtins__, 'raw_input', input)

# My code
redirect_uri = "http://localhost:8080/"
client_secret = "9-PA2Gjoq8It~4IhttDm0m_g.2.wLno0.4"
client_id = '2755a175-8423-49df-be40-c325a51a3d0d'

# Sample code
# redirect_uri = "http://localhost:8080/"
# client_secret = "BqaTYqI0XI7wDKcnJ5i3MvLwGcVsaMVM"
# client_id = '00000000481695BB'

client = onedrivesdk.get_default_client(client_id=client_id,
                                        scopes=['wl.signin',
                                                'wl.offline_access',
                                                'onedrive.readwrite'])

auth_url = client.auth_provider.get_auth_url(redirect_uri)
# Block thread until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
# Finally, authenticate!
#code = 'M.R3_BAY.-CS7uqzQL7sSaThleZruF8727Wh8UDtOCtvRXiY48XtckJnj!6WXFeI!DjrghefeYI97lc6ITPDxlLepKt06jdDojEZcFxaKesPChKEtjNuC6BfWUxAAZYwEVqteR2aV0BMJRCx3M!BqU3!mFQHyWXlYDfErj8ybp38i28baPegJlOQ93iUiZft3lUlsVDzLahGns8a0fhd514kztI5WPZQh6l29F1LQhL*5cmFv7cMmEI1tezK46lVSitQa!6KaFfttCLoA!*G0BKASkkaEpGWVPCehQHwYLx0vPKj18YC1t!yvc3AV3U4vc!VuGrPRJ4YJ2trkyIT3GCGo2BbFokoo$'
client.auth_provider.authenticate(code, redirect_uri, client_secret)

item_id = "root"
copy_item_ids = None
action = 0

# If have token
#token = 'M.R3_BAY.-CS7uqzQL7sSaThleZruF8727Wh8UDtOCtvRXiY48XtckJnj!6WXFeI!DjrghefeYI97lc6ITPDxlLepKt06jdDojEZcFxaKesPChKEtjNuC6BfWUxAAZYwEVqteR2aV0BMJRCx3M!BqU3!mFQHyWXlYDfErj8ybp38i28baPegJlOQ93iUiZft3lUlsVDzLahGns8a0fhd514kztI5WPZQh6l29F1LQhL*5cmFv7cMmEI1tezK46lVSitQa!6KaFfttCLoA!*G0BKASkkaEpGWVPCehQHwYLx0vPKj18YC1t!yvc3AV3U4vc!VuGrPRJ4YJ2trkyIT3GCGo2BbFokoo$'
token = None

items = navigate(client, item_id)
print('=========ONEDRIVE=========')
print('DisplayName: ')
print("0: UP")
count = 0
for count, item in enumerate(items):
    print("{} {}".format(count + 1, item.name if item.folder is None else "/" + item.name))

list_changes(client, item_id, token)


