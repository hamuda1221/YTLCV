# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:35:04 2018

@author: hamuda
"""

import json
import os
import httplib2
from oauth2client import tools
from oauth2client import client
from oauth2client.file import Storage

credentials_path = "credentials.json"
if os.path.exists(credentials_path):
    # 認証済み
    store = Storage(credentials_path)
    credentials = store.get()
    print(credentials)
else:
    # 認証処理
    f = "client.json"
    scope = "https://www.googleapis.com/auth/youtube.readonly"
    flow = client.flow_from_clientsecrets(f, scope)
    flow.user_agent = "hoge"
    credentials = tools.run_flow(flow, Storage(credentials_path))
    
http = credentials.authorize(httplib2.Http())
url = "https://www.googleapis.com/youtube/v3/liveBroadcasts?part=snippet&id="
url += "6dZq7y_oLzI"
res, data = http.request(url)
data = json.loads(data.decode())

chat_id = data["items"][0]["snippet"]["liveChatId"]
print(chat_id)

pageToken = None
url = "https://www.googleapis.com/youtube/v3/liveChat/messages?part=snippet,authorDetails"
url += "&liveChatId=" + chat_id

while True:
    if pageToken:
        url += "&pageToken=" + pageToken

    res, data = http.request(url)
    data = json.loads(data.decode())

    for datum in data["items"]:
        print(datum["authorDetails"]["displayName"])
        print(datum["snippet"]["textMessageDetails"]["messageText"])
        print(datum["authorDetails"]["profileImageUrl"])

    pageToken = data["nextPageToken"]
    # time.sleep(3)