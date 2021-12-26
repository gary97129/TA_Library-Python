from tkinter import * 
import  requests, webbrowser, json, socket
from time import *

'''
要取得使用者 token 需分為兩步驟實現：
1. 須先取得 code 
2. 取得 code 後，再向 line notify 請求使用者 token
'''
def get_token():
    a = notify("VvpfgpbfsDW1mt5L0p3Ozt","http://140.130.36.75:8000","KsouxvSyExeupzvufUuqz4aV6c5QhtmQu3JsRKTbBdP","")
    if a == 0:
        return 0
    else:
        return a

# get_code 主要功能：向 server 請求 code
def get_code(code):
    try:
        HOST = '140.130.36.75'
        PORT = 7000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while True:
            indata = s.recv(1024)
            print('code：' + indata.decode())
            code = indata.decode()
            s.close()
            break
        return code
    except:
        return 0


def notify(client_id,redirect_uri,client_secret,code): 
    global a
    # STEP 1    取得 code
    code_URL = 'https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&response_mode=form_post&state=f094a459&client_id={}&redirect_uri={}'.format(client_id, redirect_uri) 

    
    webbrowser.open_new(code_URL)
    code_r = requests.get(code_URL)
    
    print(code_r)
    print("------------------------------")
    # 200 為連線成功
    # print(code_r.status_code)

    # 連線成功回傳 OK
    if code_r.status_code == requests.codes.ok:
        print('code_URL：ok')
    
    # 執行 get_code 函式
    a = get_code(code)
    # STEP 2    取得用戶端 token
    token_URL = "https://notify-bot.line.me/oauth/token?grant_type=authorization_code&redirect_uri={}&client_id={}&client_secret={}&code={}".format(redirect_uri, client_id, client_secret, code)
    token_r = requests.post(token_URL)

    # 200 為連線成功
    # print('token_URL：', token_r.status_code)

    

    # 若連線成功則回傳 OK
    if token_r.status_code == requests.codes.ok and a != 0:
        print('token_URL：ok')

        # 透過 json.loads 函式將 token_r.text 轉為字典資料型態
        # token_r.text 原為字串資料型態
        access_token = json.loads(token_r.text)

        # 取得註冊用戶 token
        print("token：{}".format(access_token['access_token']))
        return access_token['access_token']

    # 若發生錯誤則回傳 error code
    else:
        print('token_URL：{}'.format(token_r.status_code))
        return 0



get_token()