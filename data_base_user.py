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


def add_favour(user_id, game, delete=False):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    user_id = f"id_{user_id}"
    try:
        cursor.execute(f'ALTER TABLE favourite ADD {user_id} VARCHAR (50);')
        conn.commit()
    except sqlite3.OperationalError:
        res = cursor.execute(f"SELECT {user_id} FROM favourite WHERE {user_id} = ?;", (game,)).fetchall()
        if len(res) == 0:
            cursor.execute(f'INSERT INTO favourite ({user_id}) VALUES (?);', (game,))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return False
    else:
        cursor.execute(f'INSERT INTO favourite ({user_id}) VALUES (?);', (game,))
        conn.commit()
        conn.close()


def get_favourite(user_id, check=False):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    user_id = f"id_{user_id}"
    if check is False:
        try:
            res = list(cursor.execute(f"SELECT {user_id} FROM favourite WHERE {user_id} IS NOT NULL;").fetchall())
        except sqlite3.OperationalError:
            res = []
        if bool(res):
            return [[[j[0], j[0] + '_favgame'] for j in res[i:i+5]] for i in range(0, len(res), 5)]
        return res
    else:
        return bool(list(cursor.execute(f"SELECT {user_id} FROM favourite WHERE {user_id} = ?;", (check,))))


def del_fav(user_id, game):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    user_id = f"id_{user_id}"
    cursor.execute(f"UPDATE favourite SET {user_id} = NULL WHERE {user_id} = ?;", (game,))
    conn.commit()
    conn.close()
