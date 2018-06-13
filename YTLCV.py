# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:35:04 2018

@author: hamuda
"""

import sys
import time
import json
import os
import httplib2
import tkinter as tk
import tkinter.ttk as ttk
from oauth2client import tools
from oauth2client import client
from oauth2client.file import Storage

http, url = None, None

def pushButton(event):
    #ボタンが押されたらコメントを読み取り始める
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
        
    global http
    http = credentials.authorize(httplib2.Http())
    
    global url
    url = URLBox.get()
    index1 = url.find('=')
    url2 = url[index1 + 1 :]
    url = "https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id="
    url += url2
    res, data = http.request(url)
    data = json.loads(data.decode())
    chat_id = data["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
    print(chat_id)

    

#ウィンドウの作成
root = tk.Tk()
root.title("YoutubeLiveCommentViewer")
root.minsize(600, 200)
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

frame1 = tk.Frame(root, pady = 10)
frame1.pack()

labe1 = tk.Label(frame1, font=("", 14), text="生放送URL")
labe1.grid(column = 0, row = 0, padx=5, pady=5, sticky = (tk.W))
URLBox = tk.Entry(frame1, font=("", 14), width = 42)
URLBox.grid(column = 1, row = 0, padx=5, pady=5, sticky = (tk.W, tk.E))
button1 = tk.Button(frame1, text="接続")
button1.grid(column = 2, row = 0, padx=5, pady=5, sticky = (tk.E))

button1.bind("<Button-1>",pushButton) 

if http != None and url != None:
    print(http, url)

root.mainloop()

"""

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

"""