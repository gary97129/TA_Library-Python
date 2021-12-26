# -*- coding:utf-8 -*-
import time
import wx
import sqlite3
import requests,webbrowser, json, socket
import datetime
import threading
from flask import Flask, request
from bs4 import BeautifulSoup
from pubsub import pub

app = Flask(__name__)
@app.route("/",methods=['GET','POST'])

def GetData():
    if request.method == 'POST':
        client_id = "pvrWMFKs7emzk27ZXcmmI1"
        redirect_uri = "http://127.0.0.1:5000"
        client_secret = "dLHif2Wmse1yWncwlxhLTo5qUhnDwATWD6YHEjO0GYZ"
        code = request.form.get('code')
        token_URL = "https://notify-bot.line.me/oauth/token?grant_type=authorization_code&redirect_uri={}&client_id={}&client_secret={}&code={}".format(redirect_uri, client_id, client_secret, code)
        token_r = requests.post(token_URL)
        if token_r.status_code == requests.codes.ok:
            access_token = json.loads(token_r.text)
            lineToken = access_token['access_token']
            pub.sendMessage("lineNotifyToken",message=lineToken)
        return lineToken

def RunServer():
    app.run()

class Frame_Login(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='圖書借閱管理系統-登入', size=(350, 263),name='frame',style=541072384)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.AcLabel = wx.StaticText(self.qdck,size=(69, 24),pos=(52, 36),label='帳號：',name='staticText',style=2321)
        AcLabel_字体 = wx.Font(14,74,90,400,False,'微軟正黑體',30)
        self.AcLabel.SetFont(AcLabel_字体)
        self.PwLabel = wx.StaticText(self.qdck,size=(69, 24),pos=(52, 82),label='密碼：',name='staticText',style=2321)
        PwLabel_字体 = wx.Font(14,74,90,400,False,'微軟正黑體',30)
        self.PwLabel.SetFont(PwLabel_字体)
        self.AcTextBox = wx.TextCtrl(self.qdck,size=(138, 22),pos=(127, 40),value='',name='text',style=0)
        self.PwTextBox = wx.TextCtrl(self.qdck,size=(138, 22),pos=(127, 85),value='',name='text',style=2048)
        self.btn_login = wx.Button(self.qdck,size=(171, 32),pos=(80, 130),label='登入',name='button')
        btn_login_字体 = wx.Font(12,74,90,400,False,'微軟正黑體',30)
        self.btn_login.SetFont(btn_login_字体)
        self.btn_login.Bind(wx.EVT_BUTTON,self.btn_login_anbdj)
        self.btn_reg_label = wx.StaticText(self.qdck,size=(111, 24),pos=(113, 180),label='沒有會員嗎？註冊',name='staticText',style=2321)
        btn_reg_label_字体 = wx.Font(10,74,90,400,False,'微軟正黑體',30)
        self.btn_reg_label.SetFont(btn_reg_label_字体)
        self.btn_reg_label.SetForegroundColour((0, 0, 255, 255))
        self.btn_reg_label.Bind(wx.EVT_LEFT_DOWN,self.btn_reg_label_sbzjax)

    def btn_login_anbdj(self,event):
        account = self.AcTextBox.GetValue()
        password = self.PwTextBox.GetValue()
        if account != '' and password != '':
            ret = Login(account,password)
            if ret == -1:
                msg = "帳號不存在"
            elif ret == 0:
                msg = "登入失敗"
            elif ret == 1:
                msg = "登入成功"
            elif ret == 2:
                msg = "管理員登入成功"
            wx.MessageBox(msg)
            self.Close()
            frame = Frame_Main()
            frame.Show(True)
            pub.sendMessage("panelListener",message1=ret,message2=account)
        else:
            wx.MessageBox('帳號密碼不能為空')


    def btn_reg_label_sbzjax(self,event):
        frame = Frame_Register()
        frame.Show(True)

class Frame_Register(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='圖書借閱管理系統-註冊', size=(358, 263),name='frame',style=541071360)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.AcLabel = wx.StaticText(self.qdck,size=(69, 24),pos=(55, 26),label='帳號：',name='staticText',style=2321)
        AcLabel_字体 = wx.Font(12,74,90,400,False,'微軟正黑體',30)
        self.AcLabel.SetFont(AcLabel_字体)
        self.PwLabel = wx.StaticText(self.qdck,size=(69, 24),pos=(55, 63),label='密碼：',name='staticText',style=2321)
        PwLabel_字体 = wx.Font(12,74,90,400,False,'微軟正黑體',30)
        self.PwLabel.SetFont(PwLabel_字体)
        self.AcTextBox = wx.TextCtrl(self.qdck,size=(132, 22),pos=(136, 26),value='',name='text',style=0)
        self.PwTextBox = wx.TextCtrl(self.qdck,size=(132, 22),pos=(136, 63),value='',name='text',style=2048)
        self.btn_reg = wx.Button(self.qdck,size=(133, 32),pos=(103, 174),label='註冊',name='button')
        btn_reg_字体 = wx.Font(10,74,90,400,False,'微軟正黑體',30)
        self.btn_reg.SetFont(btn_reg_字体)
        self.btn_reg.Bind(wx.EVT_BUTTON,self.btn_reg_anbdj)
        self.CardCodeLabel = wx.StaticText(self.qdck,size=(80, 24),pos=(48, 99),label='卡片代碼：',name='staticText',style=2321)
        CardCodeLabel_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.CardCodeLabel.SetFont(CardCodeLabel_字体)
        self.CardId = wx.TextCtrl(self.qdck,size=(132, 22),pos=(136, 99),value='',name='text',style=16)
        self.btnNotify = wx.Button(self.qdck,size=(220, 31),pos=(54, 132),label='連動Line Notify',name='button')
        btnNotify_字体 = wx.Font(10,74,90,400,False,'Microsoft JhengHei UI',30)
        self.btnNotify.SetFont(btnNotify_字体)
        self.btnNotify.Bind(wx.EVT_BUTTON,self.btnNotify_anbdj)
        self.LineToken = wx.TextCtrl(self.qdck,size=(165, 22),pos=(91, 268),value='',name='text',style=16)
        self.LineToken.Hide()
        pub.subscribe(self.myListener,"lineNotifyToken")

    def myListener(self, message):
        self.LineToken.Value = message
        self.btnNotify.LabelText = "LineNotify連動成功"
        self.btnNotify.Disable()

    def btn_reg_anbdj(self,event):
        account = self.AcTextBox.GetValue()
        password = self.PwTextBox.GetValue()
        cardid = self.CardId.GetValue()
        lineToken = self.LineToken.GetValue()
        if account == "" or password == "" :
            wx.MessageBox("註冊資料不能為空")
            return

        if lineToken == "": #or cardid == "":
            wx.MessageBox("請先連動LineNotify以及刷卡綁定")
            return

        if len(account) < 5 or len(password) < 5:
            wx.MessageBox("帳號或密碼長度不能小於5")
            return

        ret = Register(account,password,cardid,lineToken)
        if ret == -1:
            wx.MessageBox("註冊失敗，帳號已存在")
            self.AcTextBox.Value = ""
            self.PwTextBox.Value = ""
        if ret == 1:
            wx.MessageBox("註冊成功")
            self.Close()

    def GetCode(self,client_id,redirect_uri,client_secret):
        code_URL = 'https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&response_mode=form_post&state=f094a459&client_id={}&redirect_uri={}'.format(client_id, redirect_uri) 
        webbrowser.open_new(code_URL)
        return
        
    def btnNotify_anbdj(self,event):
        client_id = "pvrWMFKs7emzk27ZXcmmI1"
        redirect_uri = "http://127.0.0.1:5000"
        client_secret = "dLHif2Wmse1yWncwlxhLTo5qUhnDwATWD6YHEjO0GYZ"
        t = threading.Thread(target=self.GetCode,args=(client_id,redirect_uri,client_secret))
        t.start()
    
class Frame_Search(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='圖書借閱管理系統-查詢', size=(593, 394),name='frame',style=541072384)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.label = wx.StaticText(self.qdck,size=(188, 24),pos=(180, 10),label='請輸入欲查詢資料：',name='staticText',style=2321)
        label_字体 = wx.Font(14,74,90,400,False,'微軟正黑體',30)
        self.label.SetFont(label_字体)
        self.TextBox = wx.TextCtrl(self.qdck,size=(169, 21),pos=(185, 43),value='',name='text',style=0)
        TextBox_字体 = wx.Font(9,74,90,400,False,'微軟正黑體',30)
        self.TextBox.SetFont(TextBox_字体)
        self.TextBox.Bind(wx.EVT_TEXT,self.TextBox_nrbgb)
        self.notifyBtn = wx.Button(self.qdck,size=(171, 32),pos=(188, 312),label='推播關注',name='button')
        notifyBtn_字体 = wx.Font(9,74,90,400,False,'微軟正黑體',30)
        self.notifyBtn.SetFont(notifyBtn_字体)
        self.notifyBtn.Bind(wx.EVT_BUTTON,self.notifyBtn_anbdj)
        self.cjlbk4 = wx.ListCtrl(self.qdck,size=(500, 225),pos=(36, 74),name='listCtrl',style=8227)
        self.cjlbk4.AppendColumn('書名', 0,140)
        self.cjlbk4.AppendColumn('作者', 0,140)
        self.cjlbk4.AppendColumn('出版社', 0,140)
        self.cjlbk4.AppendColumn('是否可借閱', 0,80)
        cjlbk4_字体 = wx.Font(10,74,90,400,False,'微軟正黑體',30)
        self.cjlbk4.SetFont(cjlbk4_字体)
        self.cjlbk4.Bind(wx.EVT_LIST_ITEM_SELECTED,self.cjlbk4_xzbx)

    def TextBox_nrbgb(self,event):
        text = self.TextBox.Value
        self.cjlbk4.ClearAll()

        self.cjlbk4.AppendColumn('書名', 0,140)
        self.cjlbk4.AppendColumn('作者', 0,140)
        self.cjlbk4.AppendColumn('出版社', 0,140)
        self.cjlbk4.AppendColumn('是否可借閱', 0,80)

        retBook = FindBook(text)

        if len(retBook) != 0:
            for i in retBook:
                self.cjlbk4.Append(i)

    def notifyBtn_anbdj(self,event):
        focusedItem = self.cjlbk4.GetFocusedItem()
        if focusedItem != -1:
            wx.MessageBox(focusedItem)
        else:
            wx.MessageBox("請先選擇一本書")

    def cjlbk4_xzbx(self,event):
        self.cjlbk4.GetFocusedItem()

class Frame_AddBook(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='圖書借閱管理系統-新增', size=(454, 100),name='frame',style=541072384)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.ISBNTextBox = wx.TextCtrl(self.qdck,size=(266, 22),pos=(27, 19),value='',name='text',style=0)
        self.btn_addBook = wx.Button(self.qdck,size=(98, 32),pos=(316, 13),label='新增書籍',name='button')
        self.btn_addBook.Bind(wx.EVT_BUTTON,self.btn_addBook_anbdj)

    def btn_addBook_anbdj(self,event):
        isbn = self.ISBNTextBox.GetValue()
        if isbn == "":
            wx.MessageBox("請輸入ISBN或是掃描條碼")
            return
        ret = AddBook(isbn)
        if ret == 0:
            wx.MessageBox("書本已存在")
        elif ret == 1:
            wx.MessageBox("新增成功")
        elif ret == -1:
            wx.MessageBox("新增失敗")
        else:
            wx.MessageBox("未知錯誤")

class Frame_Borrow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='圖書借閱管理系統-借/還書', size=(390, 280),name='frame',style=541072384)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.MemberLabel = wx.StaticText(self.qdck,size=(287, 24),pos=(35, 30),label='會員帳號：',name='staticText',style=17)
        MemberLabel_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.MemberLabel.SetFont(MemberLabel_字体)
        self.BookNameLabel = wx.StaticText(self.qdck,size=(287, 24),pos=(35, 70),label='書本名稱：',name='staticText',style=17)
        BookNameLabel_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.BookNameLabel.SetFont(BookNameLabel_字体)
        self.bq9 = wx.StaticText(self.qdck,size=(291, 24),pos=(35, 110),label='歸還日期：',name='staticText',style=17)
        bq9_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.bq9.SetFont(bq9_字体)
        self.IsOverdue = wx.StaticText(self.qdck,size=(194, 24),pos=(35, 150),label='是否逾期：',name='staticText',style=17)
        IsOverdue_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.IsOverdue.SetFont(IsOverdue_字体)
        self.btn_scan = wx.Button(self.qdck,size=(289, 29),pos=(40, 189),label='開啟掃描',name='button')
        btn_scan_字体 = wx.Font(10,74,90,400,False,'Microsoft JhengHei UI',30)
        self.btn_scan.SetFont(btn_scan_字体)
        self.btn_scan.Bind(wx.EVT_BUTTON,self.btn_scan_anbdj)
        pub.subscribe(self.myListener,"member")

    def myListener(self, message):
        self.MemberLabel.LabelText = "會員帳號：" + message

    def btn_scan_anbdj(self,event):
        print("開啟掃描工具中...")
        #拿到ISBN後 使用BorrowBook函數
        #BorrowBook(self.MemberLabel.LabelText.replace('會員帳號：',''),lineToken,isbn)
        #開啟掃描工具

class Frame_Main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='圖書借閱管理系統', size=(362, 138),name='frame',style=541072384)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.btn_search = wx.Button(self.qdck,size=(93, 40),pos=(62, 30),label='查詢',name='button')
        btn_search_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.btn_search.SetFont(btn_search_字体)
        self.btn_search.Bind(wx.EVT_BUTTON,self.btn_search_anbdj)
        self.btn_borrow = wx.Button(self.qdck,size=(93, 40),pos=(196, 30),label='借/還書',name='button')
        btn_borrow_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.btn_borrow.SetFont(btn_borrow_字体)
        self.btn_borrow.Bind(wx.EVT_BUTTON,self.btn_borrow_anbdj)
        self.MemberLabel = wx.StaticText(self.qdck,size=(80, 24),pos=(1000,1000),label='',name='staticText',style=2321)
        MemberLabel_字体 = wx.Font(12,74,90,400,False,'Microsoft JhengHei UI',30)
        self.MemberLabel.SetFont(MemberLabel_字体)
        self.MemberLabel.Hide()
        pub.subscribe(self.myListener,"panelListener")

    def myListener(self, message1,message2):
        if message1 == 2:
            self.Title = "圖書借閱管理系統-管理員"
            self.btn_search.LabelText = '新增/查詢'
        else:
            self.MemberLabel.LabelText = message2

    def btn_search_anbdj(self,event):
        if self.Title == "圖書借閱管理系統-管理員" and self.btn_search.LabelText == '新增/查詢':
            frame = Frame_AddBook()
            frame.Show(True)
        frame = Frame_Search()
        frame.Show(True)

    def btn_borrow_anbdj(self,event):
        frame = Frame_Borrow()
        frame.Show(True)
        pub.sendMessage("member",message=self.MemberLabel.LabelText)

class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame_Login()
        self.frame.Show(True)
        return True

#-2程式出錯,-1不存在用戶,0登入失敗,1登入成功
def Login(account,password):
    conn = sqlite3.connect('library.db')
    db = conn.cursor()
    db.execute('SELECT Account FROM Users;')
    flag = 0
    ret = 0
    for i in db.fetchall():
        if account in i:
            flag=1
            break
    if not flag:
        ret = -1
    db.execute(f'SELECT Password FROM Users WHERE Account = "{account}";')
    if db.fetchone()[0] == password:
        db.execute(f'SELECT IsAdmin FROM Users WHERE Account = "{account}";')
        if db.fetchone()[0]:
            ret = 2
        else:
            ret = 1
        lineToken = GetUserNotifyToken(account)
        SendLineNotify(lineToken,f'\n登入成功\n會員帳號：{account}\n您登入的時間是：\n{GetTime()}')
    else:
        ret = 0
    conn.close()
    return ret

def GetTime():
    return time.strftime("%Y/%m/%d\n%H:%M:%S",time.localtime())

def GetUserNotifyToken(member):
    conn = sqlite3.connect('library.db')
    db = conn.cursor()
    db.execute(f'SELECT LineToken FROM Users WHERE Account = "{member}";')
    token = db.fetchone()[0]
    conn.close()
    return token

#-1帳號已存在 1註冊成功
def Register(account,password,cardid,lineToken):
    conn = sqlite3.connect('library.db')
    db = conn.cursor()
    db.execute('SELECT Account FROM Users;')
    for i in db.fetchall():
        if account in i:
            conn.close()
            return -1
    db.execute(f'INSERT INTO Users VALUES ("{account}", "{password}", 0,"{lineToken}","{cardid}");')
    conn.commit()
    conn.close()
    return 1

#return 0 == 存在 1 == 新增成功 -1 == 新增失敗
def AddBook(isbn,bookName = '',author = '',publisher = ''):
    isbn = int(isbn)
    conn = sqlite3.connect('library.db')
    db = conn.cursor()
    db.execute('SELECT ISBN FROM Library;')
    for i in db.fetchall():
        if isbn in i:
            conn.close()
            return 0
    url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/'
    headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    res = requests.request("GET",url,headers=headers)
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    if cookie != '':
        url = 'http://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayResults.php?&Pact=DisplayAll4Simple'
        payload ={
        'FO_SearchField0' : 'ISBN',
        'FO_SearchValue0' : isbn,
        'FB_clicked': 'FB_開始查詢',
        'FB_pageSID': 'Simple',
        'FO_Match': '2',
        'FO_每頁筆數': '10',
        'FO_目前頁數': '1',
        'FO_資料排序': 'PubMonth_Pre DESC',
        'FB_ListOri': ''
        }
        try:
            res = requests.request('POST',url,data=payload,cookies=cookie,headers=headers)
            res = requests.request('POST',url,data=payload,cookies=cookie,headers=headers)
            res.encoding='UTF-8'
            root = BeautifulSoup(res.text,"html.parser")
            data = root.find("table",class_ ="rwd-table table-searchbooks")
            tdData = data.find_all("td")
            for i in tdData:
                if bookName != '' and author != '' and publisher != '':
                    break
                if i['aria-label'] == "書名":
                    bookName = i.text
                elif i['aria-label'] == "作者":
                    author = i.text
                elif i['aria-label'] == "出版者":
                    publisher = i.text
            imgSrc=root.find("img",width='50')['src']
            db.execute(f'INSERT INTO Library VALUES ({isbn}, "{bookName}", "{author}","{publisher}","{imgSrc}",0,"","","");')
            conn.commit()
            conn.close()
            return 1
        except Exception as e:
            print(e)
            return -1

def FindBook(bookName):
    retBook = []
    bn = ''
    au = ''
    pu = ''
    ib = ''
    if bookName != '':
        conn = sqlite3.connect('library.db')
        db = conn.cursor()
        db.execute('SELECT BookName FROM Library;')
        for i in db.fetchall():
            if bookName in i[0]:
                db.execute(f'SELECT * FROM Library WHERE bookName = "{i[0]}";')
                data = db.fetchone()
                bn = data[1]
                au = data[2]
                pu = data[3]
                ib = '可' if data[5] == 0 else '不可'
                retBook.append([bn,au,pu,ib])
        conn.close()
    return retBook

def GetMemberLineToken(account):
    conn = sqlite3.connect('library.db')
    db = conn.cursor()
    db.execute(f'SELECT LineToken FROM Users WHERE Account = {account};')
    lineToken = db.fetchone()[0]
    conn.close()
    return lineToken

#發送Line通知
def SendLineNotify(lineToken,msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Authorization' : 'Bearer ' + lineToken
    }
    payload = {'message' : msg}
    r = requests.post(url,headers=headers,params=payload)
    return r.status_code #200 = 成功

#如果這本書被借走了，就會執行還書的動作；如果這本書沒被借走，就會執行借書的動作
def BorrowBook(member,lineToken,isbn):
    #連接library資料庫
    conn = sqlite3.connect('library.db')
    db = conn.cursor()
    db.execute(f'SELECT IsBorrow FROM Library WHERE ISBN = {isbn};')
    IsBorrow = db.fetchone()[0]
    db.execute(f'SELECT BookName FROM Library WHERE ISBN = {isbn};')
    BookName = db.fetchone()[0]
    #代表這本書被借走了，不能借閱，所以變成還書
    if IsBorrow:
        db.execute(f'UPDATE Library SET IsBorrow = 0 WHERE ISBN = {isbn};')
        db.execute(f'UPDATE Library SET Borrower = "" WHERE ISBN = {isbn};')
        db.execute(f'UPDATE Library SET BorrowDate = "" WHERE ISBN = {isbn};')
        db.execute(f'UPDATE Library SET ReturnDate = "" WHERE ISBN = {isbn};')
        print(f'{BookName}還書成功')
        if lineToken != '':
            SendLineNotify(lineToken,f'{BookName}還書成功')
    #這本書可以借閱
    else:
        today = int(datetime.datetime.now().strftime("%Y%m%d"))
        returnDay = DateProc(str(today))
        db.execute(f'UPDATE Library SET IsBorrow = 1 WHERE ISBN = {isbn};')
        db.execute(f'UPDATE Library SET Borrower = {member} WHERE ISBN = {isbn};')
        db.execute(f'UPDATE Library SET BorrowDate = {today} WHERE ISBN = {isbn};')
        db.execute(f'UPDATE Library SET ReturnDate = {returnDay} WHERE ISBN = {isbn};')
        print(f'{BookName}借閱成功')
        if lineToken != '':
            SendLineNotify(lineToken,f'{BookName}借閱成功')
    conn.commit()
    conn.close()

#日期計算
def DateProc(date:str):
    date = datetime.datetime.strptime(str(date),"%Y%m%d")
    returnDate = (date + datetime.timedelta(days=27)).strftime("%Y%m%d")
    print(type(returnDate))
    return returnDate

if __name__ == '__main__':
    t = threading.Thread(target=RunServer)
    t.start()
    app = myApp()
    app.MainLoop()