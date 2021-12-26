def peoplein(cardid,token):
    import sqlite3

    conn = sqlite3.connect('My SQL.db')
    db = conn.cursor()

    db.execute(f"INSERT INTO people( cardid, linetoken) values('{cardid}', '{token}');")


    conn.commit()

    conn.close()