import sqlite3


# Выводит список игр по категории
def categ_lst(genre):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    sql = "SELECT name FROM game_data WHERE genre = ?;"
    res = list(cursor.execute(sql, (genre,)).fetchall())
    res = sorted([i[0] for i in res], key=lambda x: len(x))
    return [[[j, j + '_game'] for j in res[i:i+5]]
            for i in range(0, len(res), 5)]


# Выводит данные по одной игре
def game_info(name, curr):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    sql = f"SELECT name, url, meta, youtube, {curr}, genre FROM game_data WHERE name = ?;"
    res = cursor.execute(sql, (name,)).fetchone()
    res = list(res) if res is not None else []
    return res


# Возвращает список рекомендованных игр
def rec(user_id=0, genre_1='', genre_2='', price=0, curr='', flag=0):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    reso = [i[0] for i in list(cursor.execute("""SELECT game_data.name FROM game_data, favorite 
                WHERE favorite.user_id = ? AND favorite.game_id = game_data.game_id;""", (user_id,)).fetchall())]
    if flag:
        sql = f"SELECT name FROM game_data WHERE {curr} <= ? AND (genre = ? OR genre = ?);"
        res = [i[0] for i in list(cursor.execute(sql, (price, genre_1, genre_2)).fetchall())]
    else:
        sql = "SELECT name FROM game_data ORDER BY random() LIMIT 30;"
        res = [i[0] for i in list(cursor.execute(sql).fetchall())]
    res = sorted(list(set(res) ^ set(reso)), key=lambda x: len(x))
    return sorted([[[j, j + '_rekgame'] for j in res[i:i+5]] for i in range(0, len(res), 5)], key=lambda x: len(x[0]))
