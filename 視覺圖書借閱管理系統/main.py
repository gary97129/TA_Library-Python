from serial.tools import list_ports
from datetime import datetime, timedelta
import random
import sqlite3


conn = sqlite3.connect('My SQL.db')
db = conn.cursor()

books=[]
with open('book.txt', 'r',encoding="utf-8") as f:
    for i in f:
        s = i.split(" ISBN:	")
        books.append(s[1][:-1])


isbn = random.choice(books)
book = str(db.execute(f'SELECT name FROM book WHERE isbn="{isbn}"').fetchall()[0][0])


plist = list_ports.comports()
data=["1234567890","2345678901","3456789012","4567890123","5678901234","6789012345","7890123456","8901234567","9012345678","0123456789"]
card = random.choice(data)

sdate = datetime.now().strftime('%Y-%m-%d')
edate = datetime.now()+timedelta(days=30)
edate = edate.strftime("%Y/%m/%d")
db.execute(f'UPDATE book SET user = "{card}",sdate="{sdate}",edate="{edate}" WHERE isbn="{isbn}"')

conn.commit()

user = db.execute(f'SELECT sdate,edate,name FROM book WHERE user="{card}" ORDER BY sdate').fetchall()
books=""
day=""
for i in user:
    if (books=="" or i[0] != day):
        books += f"\n借閱時間 : {i[0]} - {i[1]}\n書本名稱 :\n[ {i[2]} ]"
        day=i[0]
    else:
        books += f"[ {i[2]} ]"
    if i!=user[-1]:books += "\n"

conn.close()



