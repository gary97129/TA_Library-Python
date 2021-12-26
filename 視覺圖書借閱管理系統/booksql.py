def bookadd():
    import sqlite3

    conn = sqlite3.connect('My SQL.db')
    db = conn.cursor()


    with open('book.txt', 'r',encoding="utf-8") as f:
        for i in f:
            s = i.split(" ISBN:	")
            db.execute(f"INSERT INTO book( name, isbn) values('{s[0]}', '{s[1][:-1]}');")


    conn.commit()

    conn.close()

def bookout():
    import sqlite3

    conn = sqlite3.connect('My SQL.db')
    db = conn.cursor()


    with open('book.txt', 'r',encoding="utf-8") as f:
        for i in f:
            s = i.split(" ISBN:	")
            db.execute(f"INSERT INTO book( name, isbn) values('{s[0]}', '{s[1][:-1]}');")


    conn.commit()

    conn.close()

def bookin():
    import sqlite3

    conn = sqlite3.connect('My SQL.db')
    db = conn.cursor()


    with open('book.txt', 'r',encoding="utf-8") as f:
        for i in f:
            s = i.split(" ISBN:	")
            db.execute(f"INSERT INTO book( name, isbn) values('{s[0]}', '{s[1][:-1]}');")


    conn.commit()

    conn.close()