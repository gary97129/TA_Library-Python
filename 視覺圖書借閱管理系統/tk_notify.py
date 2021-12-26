from tkinter import * 
import  requests, webbrowser, json, socket

'''
要取得使用者 token 需分為兩步驟實現：
1. 須先取得 code 
2. 取得 code 後，再向 line notify 請求使用者 token
'''
# 輸入 line notify client id
client_id = "VvpfgpbfsDW1mt5L0p3Ozt"
# 輸入 line notify callback URL
redirect_uri = "https://notify-token.herokuapp.com/"
# 輸入 line notify client secret
client_secret = "KsouxvSyExeupzvufUuqz4aV6c5QhtmQu3JsRKTbBdP"
code = ''

root = Tk() 
frame = Frame(root) 
frame.pack() 

# get_code 主要功能：向 server 請求 code
def get_code():
    global code
    print("123")


def notify(): 
    # STEP 1    取得 code
    code_URL = 'https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&response_mode=form_post&state=f094a459&client_id={}&redirect_uri={}'.format(client_id, redirect_uri) 

    
    webbrowser.open_new(code_URL)
    code_r = requests.get(code_URL)

    # 200 為連線成功
    # print(code_r.status_code)

    # 連線成功回傳 OK
    if code_r.status_code == requests.codes.ok:
        print('code_URL：ok')
    
    # 執行 get_code 函式
    get_code()
    # STEP 2    取得用戶端 token
    token_URL = "https://notify-bot.line.me/oauth/token?grant_type=authorization_code&redirect_uri={}&client_id={}&client_secret={}&code={}".format(redirect_uri, client_id, client_secret, code)
    token_r = requests.post(token_URL)

    # 200 為連線成功
    # print('token_URL：', token_r.status_code)

    # 若連線成功則回傳 OK
    if token_r.status_code == requests.codes.ok:
        print('token_URL：ok')

        # 透過 json.loads 函式將 token_r.text 轉為字典資料型態
        # token_r.text 原為字串資料型態
        access_token = json.loads(token_r.text)

        # 取得註冊用戶 token
        print("token：{}".format(access_token['access_token']))

    # 若發生錯誤則回傳 error code
    else:
        print('token_URL：{}'.format(token_r.status_code))


# 點擊按鈕後呼叫 notify 函式
Notify = Button(frame, text="Notify", command=notify).pack()

root.mainloop()