# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:35:04 2018

@author: hamuda
"""

import wx
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

pageToken, http, url, ffffff, chat_no = None, None, None, 0, 0

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

    url = "https://www.googleapis.com/youtube/v3/liveChat/messages?part=snippet,authorDetails"
    url += "&liveChatId=" + chat_id
    
    roop()
    
def roop():
    global url
    global http
    global pageToken
    global ffffff
    global chat_no

    if ffffff == 0:
        url2 = url
        ffffff = 1
    else:
        url2 = url + "&pageToken=" + pageToken

    res, data = http.request(url2)
    f = open("data.json", "w")
    json.dump(data.decode(), f)
    data = json.loads(data.decode())

    for datum in data["items"]:
        """
        if datum["snippet"]["superChatDetails"] == True:
            text1_1.insert(str(chat_no + 1) + ".0", str(chat_no) + "\n")
            text1_3.insert(str(chat_no + 1) + ".0", str(datum["snippet"]["displayMessage"]) + "\n")
            #datum["authorDetails"]["profileImageUrl"])
        """
        try:
            if datum["authorDetails"]["isChatModerator"] == True:
                print("==========================================================")
                
            text1_1.insert(str(chat_no + 1) + ".0", str(chat_no) + "\n")
            text1_2.insert(str(chat_no + 1) + ".0", str(datum["authorDetails"]["displayName"]) + "\n")
            text1_3.insert(str(chat_no + 1) + ".0", str(datum["snippet"]["textMessageDetails"]["messageText"]) + "\n")
            #datum["authorDetails"]["profileImageUrl"])
                  
        except KeyError:
            print("error")
        chat_no += 1
        text1_1.see("end")
        text1_2.see("end")
        text1_3.see("end")
    pageToken = data["nextPageToken"]
    #time.sleep(3)
    root.after(5000, roop)


#ウィンドの作成
class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)

        self.init_ui()

    def init_ui(self):
        self.SetTitle('test')
        self.SetBackgroundColour((0, 255, 0))
        #self.SetPosition((200, 100))
        self.SetSize((400, 300))
        self.Show()


app = wx.App()
MyApp(None)
app.MainLoop()


    
"""   
    
#ウィンドウの作成
root = tk.Tk()
root.title("YoutubeLiveCommentViewer")
root.minsize(600, 200)
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

frame1 = tk.Frame(root, relief = "ridge")
frame1.pack()

labe1 = tk.Label(frame1, font=("", 14), text="生放送URL")
labe1.grid(column = 0, row = 0, padx=5, pady=5, sticky = (tk.W))
URLBox = tk.Entry(frame1, font=("", 14), width = 42)
URLBox.grid(column = 1, row = 0, padx=5, pady=5, sticky = (tk.W, tk.E))
button1 = tk.Button(frame1, text="接続")
button1.grid(column = 2, row = 0, padx=5, pady=5, sticky = (tk.E))


frame2 = tk.Frame(root, relief = "groove")
frame2.pack()

text1 = tk.Text(frame2)
text1.grid(column = 0, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))
text1_1 = tk.Text(text1, width = 5)
text1_1.grid(column = 0, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))
text1_2 = tk.Text(text1, width = 20)
text1_2.grid(column = 1, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))
text1_3 = tk.Text(text1, width = 50)
text1_3.grid(column = 2, row = 1, sticky = (tk.N, tk.S, tk.E, tk.W))


scrollbar1 = tk.Scrollbar(text1)
scrollbar1.config(command=text1_1.yview)
scrollbar1.config(command=text1_2.yview)
scrollbar1.config(command=text1_3.yview)
scrollbar1.grid(column = 3, row = 1, sticky = tk.NS)


text1_1.config(yscrollcommand = scrollbar1.set)
text1_2.config(yscrollcommand = scrollbar1.set)
text1_3.config(yscrollcommand = scrollbar1.set)

text2 = tk.Text(frame2)
text2.grid(column = 1, row = 1, padx=5, pady=5, sticky = (tk.N, tk.S, tk.E, tk.W))

button1.bind("<Button-1>",pushButton) 

root.mainloop()



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