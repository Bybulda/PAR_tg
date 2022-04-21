import sqlite3
import orm.db_session as db_session
from orm.root import Root
import datetime

db_session.global_init("user_all.db")


# Проверяет, находится ли пользователь в таблице root пользователей
def check_root_id(idb_user):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    res = cursor.execute("""SELECT id FROM root WHERE id = ?;""", (idb_user,)).fetchone()
    conn.close()
    return bool(res)


# Меняет значение, отвечающее за вход пользователя в режим админа
def update_root(user_id, info):
    conn = sqlite3.connect('user_all.db')
    cursor = conn.cursor()
    cursor.execute("""UPDATE root SET root_prof = ? WHERE id = ?;""", (info, user_id))
    conn.commit()
    conn.close()


# Проверка на правильность пароля пользователя root
def get_root(user_id, password='', check=0):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    if check:
        res = cursor.execute(f"""SELECT root_prof FROM root WHERE id = ?;""", (user_id,)).fetchone()
        res = list(res)[0]
    else:
        res = cursor.execute(f"""SELECT name FROM root WHERE id = ? AND password = ?;""", (user_id, password))
        res = bool(list(res))
    conn.close()
    return res


# Удаляет некоторые параметры из двух баз данных
def del_any(who, base, tab):
    conn = sqlite3.connect(f'{base}.db')
    cursor = conn.cursor()
    sl = {'favorite': "user_id",  'user_data': "user_id", 'game_data': 'name'}
    cursor.execute(f"DELETE FROM {tab} WHERE {sl[tab]} = ?;", (who,))
    conn.commit()
    conn.close()


# Выводит информацию по всем пользователям
def get_user_info():
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    res = [[str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4])] for i in
           list(cursor.execute(f"SELECT user_id, fav_nick, fav_cost, fav_curr, fav_gen FROM user_data;"))]
    return '\n'.join(' - '.join(i) for i in res)


# Выводит статистику по средней цене в рублях и по любимым жанрам пользователей
def get_stat(who):
    conn = sqlite3.connect("user_all.db")
    cursor = conn.cursor()
    exchange = {'RUB': 0.0091, 'USD': 0.7625, 'EUR': 0.8415, 'CNY': 0.1200}
    stat, avg = {}, 0
    if who == 'fav_gen':
        res = [i[0] for i in list(cursor.execute("""SELECT fav_gen FROM user_data 
        WHERE fav_gen IS NOT NULL;""").fetchall())]

        for i in set(res):
            stat[i] = '{:.2%}'.format(res.count(i) / len(res))
        res = ['\n'.join(i) for i in list(stat.items())]
    elif who == 'avg_price':
        res = list(cursor.execute("""SELECT fav_cost, fav_curr FROM user_data 
        WHERE fav_cost IS NOT NULL;""").fetchall())
        if bool(res):
            for i in res:
                avg += i[0] if i[1] == "RUB" else i[0] * exchange[i[1]] // exchange['RUB']
            res = f"{'{:.2f}'.format(avg // len(res))} RUB"
        else:
            res = "Невозможно посчитать, нет позиций"
    conn.close()
    return res


# Изменяет параметры для игры
def ch_game_info(name, cost=-1, yt='', new_name=''):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    if yt == '' and cost != -1:
        cursor.execute(f"UPDATE game_data SET RUB = {cost}, "
                       f"CNY = {cost // 46}, USD = {cost // 87}, EUR = {cost // 101} WHERE name = ?;", (name,))
    elif cost == -1 and yt != '':
        cursor.execute(f"UPDATE game_data SET youtube = ? WHERE name = ?;", (yt, name))
    elif cost == -1 and yt == '' and new_name != '':
        cursor.execute(f"UPDATE game_data SET name = ? WHERE name = ?;", (new_name, name))
    conn.commit()
    conn.close()


# Обнуляет счётчик сообщений или же прибавляет к нему единицу
def set_mess(user_id, clear=0):
    conn = sqlite3.connect('user_all.db')
    cursor = conn.cursor()
    if clear:
        cursor.execute(f"UPDATE root SET messages = 0 WHERE id = ?;", (user_id,))
    else:
        cursor.execute(f"UPDATE root SET messages = messages + 1 WHERE id = ?;", (user_id,))
    conn.commit()
    conn.close()


# Возвращает количество сообщений в режиме админа для функции очистки
def get_mess(user_id):
    db_sess = db_session.create_session()
    res = db_sess.query(Root.messages).filter_by(id=user_id).scalar()
    return res


# Возвращает время начала блокировки
def get_ban_time(user_id, hours=0):
    conn = sqlite3.connect('user_all.db',
                           detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    res = cursor.execute("""SELECT ban_time FROM user_data 
    WHERE user_id = ? AND ban_time IS NOT NULL;""", (user_id,)).fetchone()
    conn.close()
    return res[0]


# Устанавливает время начала блокировки
def set_ban_time(user_id):
    conn = sqlite3.connect('user_all.db',
                           detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    cursor.execute("""UPDATE user_data SET ban_time = ? WHERE user_id = ?;""", (datetime.datetime.now(), user_id))
    conn.commit()
    conn.close()
