from os import environ
from threading import Thread
from tkinter import *
from time import *
from tkinter.font import Font
from cardsql import *
from booksql import *


def sign_up(text):
    global wup
    wup = Toplevel(master=window1) 
    wup.grab_set()
    wup.title("Line綁定")
    wup.geometry('300x150')
    line = Label(wup,text=text)
    line.pack(padx=30, pady=55)
    if text != "Line綁定中":
        wup.geometry('300x250')
        done = Button(wup,text="完成",command= wup.destroy)
        done.pack(pady=0)


def aaa(ww,name):
    import get_card
    card = get_card.get_card()
    ww.destroy()
    if name == "登入":
        sign_in()
    elif name == "註冊":
        import get_token 
        sign_up("Line綁定中")
        token = get_token.get_token()
        print("-----------")
        print(token)
        wup.destroy()
        if token == 0:
            sign_up("綁定失敗")
        else:
            sign_up("綁定成功")
            peoplein(card,token)
        


def tap(name):
    ww = Toplevel(master=window1) 
    ww.grab_set()
    ww.title(name)
    ww.geometry('200x100')
    text = Label(ww,text="請感應卡片")
    text.pack(padx=30, pady=30)
    
    t = Thread(target=lambda:aaa(ww,name))
    t.start()


def adra(name):
    global window4

    window4 = Toplevel(master=window2) 
    window4.grab_set()
    window4.title(name)
    window4.state("zoomed")
    window4.resizable(0,0)

    sc = Scrollbar(window4)
    sc.pack(side=RIGHT, fill=Y)

    text = Label(window4,text="請掃瞄書本條碼")
    text.pack(pady=50)

    listbox = Listbox(window4, relief='raised',height=15,width=30,yscrollcommand=sc.set)
    listbox.pack()

    done = Button(window4,text="完成",command= lambda:upload(name))
    done.pack(pady=50)

    sc.config(command=listbox.yview)


def upload(data):
    if data == "註冊":
        #peoplein()
        print(1)
    elif data == "新增書籍":
        #bookadd()
        print(2)
    elif data == "借書":
        #bookin()
        print(3)
    elif data == "還書":
        #bookout()
        print(4)




def sign_in():
    global window2

    window2 = Toplevel(master=window1) 
    window2.grab_set()
    window2.title("圖書自助借還系統"+"a")
    window2.state("zoomed")
    window2.resizable(0,0)

    check_out = Button(window2,text="借書",command= lambda:adra('借書'))
    check_out.pack( pady=50)

    check_in = Button(window2,text="還書",command= lambda:adra('還書'))
    check_in.pack()

    new = Button(window2,text="新增書籍",command= lambda:adra('新增書籍'))
    new.pack(pady=50)



def home():
    global window1
    
    window1 = Tk() 
    window1.title("圖書自助借還系統")
    window1.state("zoomed")
    window1.resizable(0,0)

    
    window1.option_add("*Font", ("courier 20"))

    go = Button(window1,text="進入系統",command = lambda:tap("登入"))
    go.pack(pady=50)

    sign_up = Button(window1,text="註冊",command = lambda:tap("註冊"))
    sign_up.pack()

    window1.mainloop()







home()

