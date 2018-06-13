# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:35:04 2018

@author: hamuda
"""

import time
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
else:
    # 認証処理
    f = "client.json"
    scope = "https://www.googleapis.com/auth/youtube.readonly"
    flow = client.flow_from_clientsecrets(f, scope)
    flow.user_agent = "hoge"
    credentials = tools.run_flow(flow, Storage(credentials_path))
    
http = credentials.authorize(httplib2.Http())


url = "https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id="
url += "Vy1RbiSvHoU"
res, data = http.request(url)
data = json.loads(data.decode())
chat_id = data["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
print(chat_id)

pageToken = None
url = "https://www.googleapis.com/youtube/v3/liveChat/messages?part=snippet,authorDetails"
url += "&liveChatId=" + chat_id

url2 = url
chat_no = 0
while True:
    if pageToken:
        url2 = url + "&pageToken=" + pageToken

    res, data = http.request(url2)
    data = json.loads(data.decode())

    for datum in data["items"]:
        try:
            if datum["authorDetails"]["isChatModerator"] == True:
                print("==========================================================")
                
            print(str(chat_no) + str(" | ") +\
                  datum["authorDetails"]["displayName"] + str(" | ") +\
                  datum["snippet"]["textMessageDetails"]["messageText"])
                  #datum["authorDetails"]["profileImageUrl"])
                  
            if datum["authorDetails"]["isChatModerator"] == True:
                print("==========================================================")
        except KeyError:
            print(str(chat_no) + str(" | ") +\
                  #datum["authorDetails"]["displayName"] + str(" | ") +\
                  datum["snippet"]["displayMessage"])
                  #datum["authorDetails"]["profileImageUrl"])
        chat_no += 1
    pageToken = data["nextPageToken"]
    time.sleep(3)
