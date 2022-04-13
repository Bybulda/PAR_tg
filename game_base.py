import sqlite3


def categ_lst(genre):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    sql = "SELECT name FROM game_data WHERE genre = ?;"
    res = list(cursor.execute(sql, (genre,)).fetchall())
    res, games_buttons = [i[0] for i in res], []
    for games in res:
        games_buttons.append([games, games + '_game'])
    f_page = sorted(games_buttons[0:5], key=lambda x: len(x[0]))
    s_page = sorted(games_buttons[5:10], key=lambda x: len(x[0]))
    return f_page, s_page


def game_info(name, curr):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    sql = f"SELECT name, url, meta, youtube, {curr}, genre FROM game_data WHERE name = ?;"
    res = list(cursor.execute(sql, (name,)).fetchone())
    return res


def rec(genre_1, genre_2, price, curr):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    sql = f"SELECT name FROM game_data WHERE {curr} <= ? AND (genre = ? OR genre = ?);"
    res = list(cursor.execute(sql, (price, genre_1, genre_2)).fetchall())
    res, an = [i[0] for i in res], []
    for i in [[[j, j + '_rekgame'] for j in res[i:i+5]] for i in range(0, len(res), 5)]:
        an.append(sorted(i, key=lambda x: len(x[0])))
    return an
