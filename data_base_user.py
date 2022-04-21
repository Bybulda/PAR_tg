import sqlite3


# Функция добавляет пользователя в случае, если его нет в бд
def first_iter(user_id, nickname):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    res = cursor.execute("""INSERT INTO user_data
                            VALUES (?, ?, 'не выбран', NULL, 
                            'RUB', FALSE, FALSE, FALSE, FALSE, 0, NULL, 0);""", (user_id, nickname))
    conn.commit()
    conn.close()


# Проверяет, есть ли пользователь в бд
def check_id_bd(idb_user):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    res = cursor.execute("""SELECT fav_nick FROM user_data WHERE user_id = ?;""", (idb_user,)).fetchone()
    conn.close()
    if not bool(res):
        return True
    return False


# Обновляет любую информацию по пользователю
def update_info(user_id, to_what, data):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE user_data SET {to_what} = ? WHERE user_id = ?;", (data, user_id))
    conn.commit()
    conn.close()


# Функция возвращает любую информацию по пользователю
def get_info(user_id, to_what):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    res = cursor.execute(f"SELECT {to_what} FROM user_data WHERE user_id = ?;", (user_id,)).fetchone()
    conn.commit()
    conn.close()
    return list(res)[0]


# Функция проверяет есть ли игра в списке избранного пользователя
def check_fav(user_id, game):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    res = cursor.execute("""SELECT favorite.game_id FROM favorite, game_data 
    WHERE favorite.game_id IN (SELECT game_id FROM game_data WHERE name = ?) 
    AND favorite.user_id = ?;""", (game, user_id)).fetchone()

    conn.close()
    return bool(res)


# Добавляет игру в список избранного пользователя
def add_favour(user_id, game):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO favorite (user_id, game_id) 
    VALUES (?, (SELECT game_id FROM game_data WHERE name = ?))""", (user_id, game))
    conn.commit()
    conn.close()


# Выводит список избранного пользователя,
# в случае не задавания имени выводится список случайных игр
def get_favorite(user_id):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    res = [i[0] for i in list(cursor.execute("""SELECT game_data.name FROM game_data, favorite 
    WHERE favorite.user_id = ? AND favorite.game_id = game_data.game_id;""", (user_id,)).fetchall())]
    conn.close()
    return [[[j, j + '_favgame'] for j in res[i:i+5]] for i in range(0, len(res), 5)]


# Удаляет игру из списка избранного пользователя
def del_fav(user_id, game):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM favorite WHERE user_id = ? 
    AND game_id = (SELECT game_id FROM game_data WHERE name = ?);""", (user_id, game))
    conn.commit()
    conn.close()
