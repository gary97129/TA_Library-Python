'''
驅動程式網址：https://cdn.sparkfun.com/assets/learn_tutorials/8/4/4/CH341SER.EXE
參考網址 ：https://pyserial.readthedocs.io/en/latest/pyserial_api.html
匯入 serial 模組的 tools.list_ports 套件
此套件主要功能為列出可用連接埠
'''
from serial.tools import list_ports
# import serial.tools.list_ports
import serial

def get_card():
    '''
    comport()：回傳一個本地端連接埠的串列
    '''
    plist = serial.tools.list_ports.comports()

    print("------------------------------\n")
    print('1 為串列類別')
    print("plist：", plist)
    print("plist type：", type(plist), "\n")

    print('2 為連接埠基本資訊 (也是一個串列)')
    print("plist[0]：", plist[0])
    print("plist[0]：", type(plist[0]), "\n")

    print('3 將連接埠轉為串列類別')
    print("plist[0]：", list(plist[0]))
    print("plist[0]：", type(list(plist[0])), "\n")

    print('4 為字串類別')
    print("plist[0][0]：", plist[0][0])
    print("plist[0][0]：", type(plist[0][0]), "\n")

    print("------------------------------\n")

    '''
    參數一：連接埠名稱 (需為字串資料型態)
    參數二：為傳輸速率/鮑率 (需為數值資料型態)
    參數三：以秒為單位設置讀取時間，也可以設置為 None 或 0
            None：收到資料後才進行後續讀取動作
            0   ：持續執行讀取動作
    '''

    ser = serial.Serial('COM3', 9600, timeout=None)
    # 當設定好參數後，連接埠會顯示以開啟

    print("是否開啟連接埠：", ser.isOpen(), "\n")


    # 開啟連接埠
    # ser.open()

    
        # 讀取 ser 是否有資料
    line = ser.readline() 

    

    print("1 未以 utf-8 方式解碼時為 bytes 類別，後面會以 \\n 做為結尾")
    print(line)
    # line 為位元資料類型
    print(type(line), "\n")


    print("2 取得資料後，使用 utf-8 方式解碼")
    line = line.decode('utf-8')
    print(line)
    print(type(line))


    # 關閉連接埠
    ser.close()
    print("是否開啟連接埠：", ser.isOpen())

    return line