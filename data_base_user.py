import sqlite3


def first_iter(user_idb, nickname):
    conn = sqlite3.connect("user_all.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    res = cursor.execute("""INSERT INTO user_data
                            VALUES (?, ?, 'не выбран', 'не определена', 'RUB', 
                            FALSE, FALSE, FALSE, FALSE);""",
                         (user_idb, nickname))
    conn.commit()
    conn.close()


def check_id_bd(idb_user):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    res = cursor.execute("""SELECT fav_nick FROM 
    user_data WHERE user_id = ?;""", (idb_user,)).fetchone()
    conn.close()
    if not bool(res):
        return True
    return False


def update_info(user_id, to_what, data):
    conn = sqlite3.connect("user_all.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    st = f"UPDATE user_data SET {to_what} = ? WHERE user_id = ?;"
    cursor.execute(st, (data, user_id))
    conn.commit()
    conn.close()


def get_info(user_id, to_what):
    conn = sqlite3.connect("user_all.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    st = f"SELECT {to_what} FROM user_data WHERE user_id = ?;"
    res = cursor.execute(st, (user_id,)).fetchone()
    conn.commit()
    conn.close()
    w = list(res)[0]
    return w
