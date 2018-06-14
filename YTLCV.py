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

pageToken, http, url, ffffff, chat_no, rrrr = None, None, None, 0, 0, 0

"""
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

        if datum["snippet"]["superChatDetails"] == True:
            text1_1.insert(str(chat_no + 1) + ".0", str(chat_no) + "\n")
            text1_3.insert(str(chat_no + 1) + ".0", str(datum["snippet"]["displayMessage"]) + "\n")
            #datum["authorDetails"]["profileImageUrl"])


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
    """

#ウィンドの作成
class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)

        self.init_ui()

    def init_ui(self):
        
        self.SetTitle('test')
        #self.SetBackgroundColour((21, 31, 42))
        self.SetPosition((1080, 35))
        self.SetSize((800, 1000))
        
        self.panel = wx.Panel(self, -1)
        self.panel_chat = wx.BoxSizer(wx.VERTICAL)
        self.panel_ui1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.label_URL = wx.StaticText(self.panel, -1, "動画URL")#, size = (50, 35), pos = (0, 5))
        self.box = wx.TextCtrl(self.panel, -1, size = (300, 20))#, pos = (55,5))
        

        btn_URL = wx.Button(self.panel, -1, "接続")#, size = (70, 30), pos = (305, 5))
        btn_URL.Bind(wx.EVT_BUTTON, self.clicked)
     
        #self.panel_R = wx.Panel(self, -1, size = (380, 400), pos = (10, 60))
        #self.panel_R.SetBackgroundColour((0, 255, 0))
        
        #self.label_jp = wx.StaticText(panel_ui1, -1, "", size = (355, 200))
        
        self.panel_chat.Add(self.panel_ui1)
        self.panel_ui1.Add(self.label_URL)
        self.panel_ui1.Add(self.box)
        self.panel_ui1.Add(btn_URL)
        
        self.panel.SetSizer(self.panel_chat)
        
        """
        panel_B = wx.Panel(self, -1, pos = (210, 60), size = (180, 210))
        panel_B.SetBackgroundColour((0, 0, 255))

        panel_ui2 = wx.Panel(panel_B, -1, pos = (5, 5), size=(175, 205))
        self.label_en = wx.StaticText(panel_ui2, -1, "", size = (170, 200))
        self.label_en.SetLabel("aaaaaaaaaaaaaaaaaaaaaaaaa.")
        """
        
        #コメント更新用
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.roop)
        self.timer.Start(5000)


        self.Show(True)
        
        #self.clicked()
        
    def roop(self, event):
        global url
        global http
        global pageToken
        global ffffff
        global chat_no
        global rrrr

        if rrrr != 0:
    
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

                    text = (str("    ") + str(chat_no) + str(" | ") +\
                            datum["authorDetails"]["displayName"] + str(" | ") +\
                            datum["snippet"]["textMessageDetails"]["messageText"])
                    #datum["authorDetails"]["profileImageUrl"])
                    text = wx.StaticText(self.panel, -1, text)
                    text.SetForegroundColour('#000000')
                except KeyError:
                    print("error")
                chat_no += 1
                self.panel_chat.Add(text, proportion=0)
                self.panel_chat.Layout()
                #self.label_jp.SetLabel(text)
                print(chat_no)

            pageToken = data["nextPageToken"]
    
    
    
    def clicked(self, event):
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
        
        url = self.box.GetValue()
        #url = "https://www.youtube.com/watch?v=XfE6h2xyumQ"
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
        
        global rrrr
        rrrr = 1
        #self.label_jp.SetLabel(url)           

        
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
#https://www.youtube.com/watch?v=caunmjM4ez4
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