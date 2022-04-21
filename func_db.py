import data_base_user as db
import game_base as gb
import texts as texts
import datetime


# Возвращает время, на протяжении которого человек был с ограниченным доступом
def check_bane_time(time):
    return (datetime.datetime.now() - time).total_seconds()


# Возвращает набор элементов для вывода сообщения по настройке никнейма
def open_nick(call, user_id):
    texts.prof_set_ed_but[0][3] = 'change_nick'
    return [call, texts.prof_set_ed_but,
            texts.mes_open_nick(db.get_info(user_id, 'fav_nick'))]


# Возвращает набор элементов для вывода сообщения по настройке любимого жанра
def open_gen(call, user_id):
    texts.prof_set_ed_but[0][3] = 'change_gen'
    return [call, texts.prof_set_ed_but,
            texts.mes_open_gen(db.get_info(user_id, 'fav_gen'))]


# Возвращает набор элементов для вывода сообщения по настройке макс. цены
def open_cost(call, user_id):
    texts.prof_set_ed_but[0][3] = 'change_cost'
    return [call, texts.prof_set_ed_but,
            texts.mes_open_cost(db.get_info(user_id, 'fav_cost'),
                                db.get_info(user_id, 'fav_curr'))]


# Возвращает набор элементов для вывода сообщения по настройке валюты маркета
def open_curr(call, user_id):
    texts.prof_set_ed_but[0][3] = 'change_curr'
    return [call, texts.prof_set_ed_but,
            texts.mes_open_curr(db.get_info(user_id, 'fav_curr'))]


# Возвращает набор элементов для вывода сообщения об изменении никнейма
def change_nick(call, user_id):
    db.update_info(user_id, 'nick_prog', True)
    return [call, '', texts.mes_change_nick(), ['◀ Назад', 'back_to_sett']]


# Возвращает набор элементов для вывода сообщения об изменении любимого жанра
def change_gen(call, user_id):
    db.update_info(user_id, 'gen_prog', True)
    return [call, texts.ch_genre_buttons,
            texts.mes_change_gen(), ['◀ Назад', 'back_to_sett']]


# Возвращает набор элементов для вывода сообщения об изменении макс. цены
def change_cost(call, user_id):
    db.update_info(user_id, 'cost_prog', True)
    return [call, '', texts.mes_change_cost(), ['◀ Назад', 'back_to_sett']]


# Возвращает набор элементов для вывода сообщения об изменении валюты маркета
def change_curr(call, user_id):
    db.update_info(user_id, 'curr_prog', True)
    return [call, texts.change_curr_buttons,
            texts.mes_change_curr(), ['◀ Назад', 'back_to_sett']]


# Проверка на правильность введенного никнейма, его изменение
def set_nick(user_id, new_nick):
    if 17 > len(new_nick) > 1:
        eng_let = all(91 > ord(let.upper()) > 64 for let in new_nick)
        rus_let = all(1072 > ord(let.upper()) > 1039 for let in new_nick)
        if eng_let or rus_let:
            db.update_info(user_id, 'nick_prog', False)
            db.update_info(user_id, 'fav_nick', new_nick)
            return True
    return False


# Изменение любимого жанра
def set_gen(user_id, new_gen):
    db.update_info(user_id, 'gen_prog', False)
    db.update_info(user_id, 'fav_gen', texts.genres_types[new_gen][0])


# Проверка на правильность введенной макс. цены, её изменение
def set_cost(user_id, new_cost):
    if int(new_cost) >= 0 and int(new_cost) % 1 == 0:
        db.update_info(user_id, 'cost_prog', False)
        db.update_info(user_id, 'fav_cost', int(new_cost))
        return True
    return False


# Изменение валюты маркета
def set_curr(user_id, new_curr):
    new_c = new_curr[4:].upper()
    if db.get_info(user_id, 'fav_cost') is not None:
        old_c = db.get_info(user_id, 'fav_curr')
        fav_cost = db.get_info(user_id, 'fav_cost')
        new_fav_cost = int((texts.curr_exchange_rate[old_c] *
                            fav_cost) / texts.curr_exchange_rate[new_c])
        db.update_info(user_id, 'fav_cost', new_fav_cost)
    db.update_info(user_id, 'curr_prog', False)
    db.update_info(user_id, 'fav_curr', new_c)


# Возвращает набор элементов для вывода игр опереженного жанра
def show_gen_games(call, gen, page, back_from=0):
    return [call, gb.categ_lst(gen), texts.mes_show_gen(gen), 'kat', gen,
            page, 0, back_from]


# Возвращает набор элементов для вывода рекомендуемых игр
def show_rek_games(call, page=0, back_from=0, message=None):
    user_id = message.from_user.id if message else call.message.chat.id
    fav_gen = db.get_info(user_id, 'fav_gen')
    cost = db.get_info(user_id, 'fav_cost')
    nick = db.get_info(user_id, 'fav_nick')
    curr = db.get_info(user_id, 'fav_curr')
    if fav_gen == 'не выбран' or cost is None:
        if not message:
            return [call, gb.rec(), texts.mes_show_rek(nick),
                    'back_to_main', 'nogen', page, 1, back_from]
        return [message, gb.rec(),
                texts.mes_show_rek(nick),
                'back_to_main', 'nogen', page, 1, back_from, 1]
    gen_1 = texts.for_rek[fav_gen]
    gen_2 = texts.genres_types[gen_1][1]
    if not message:
        return [call, gb.rec(user_id, gen_1, gen_2, cost, curr, 1),
                texts.mes_show_rek(nick),
                'back_to_main', gen_1, page, 1, back_from]
    return [message, gb.rec(user_id, gen_1, gen_2, cost, curr, 1),
            texts.mes_show_rek(nick),
            'back_to_main', gen_1, page, 1, back_from, 1]


# Возвращает набор элементов для вывода избранных игр
def show_fav_games(call, page=0, back_from=0, message=None):
    user_id = message.from_user.id if message else call.message.chat.id
    games = db.get_favorite(user_id)
    if len(games) == 0:
        if not message:
            return [call, [], texts.mes_show_fav_mist(), 'back_to_main', '',
                    0, 1, back_from]
        return [message, [], texts.mes_show_fav_mist(), 'back_to_main', '',
                0, 1, back_from, 1]
    if not message:
        return [call, games, texts.mes_show_fav(),
                'back_to_main', 'favgen', page, 2, back_from]
    return [message, games, texts.mes_show_fav(),
            'back_to_main', 'favgen', page, 2, back_from, 1]


# Возвращает набор элементов для вывода профиля определенной игры
def show_game_prof(call, name, gen, back_to, in_fav):
    curr = db.get_info(call.message.chat.id, 'fav_curr')
    png_name = name + ''
    game_info = gb.game_info(name, curr)
    if back_to == 0:
        back_text = f'back_form_pf_to_{gen}'
    elif back_to == 1:
        back_text = 'back_rek'
    else:
        back_text = 'back_fav'
    png_name = png_name.replace(':', '')
    png_name = png_name.replace('-', '')
    png_name = png_name.replace('–', '')
    return [call, png_name, texts.game_prof_buttons(game_info, name, in_fav,
                                                    gen, back_text),
            texts.mes_game_prof(game_info, curr),
            back_text]


# Реализует удаление/добавление игры в избранное, обновление профиля игры
def change_fav_status(call, name, gen, back):
    if not db.check_fav(call.message.chat.id, name):
        db.add_favour(call.message.chat.id, name)
        in_fav = 1
    else:
        db.del_fav(call.message.chat.id, name)
        in_fav = 0
    if back == 'back_rek':
        back_to = 1
    elif back == 'back_fav':
        back_to = 2
    else:
        back_to = 0
    return show_game_prof(call, name, gen, back_to, in_fav)
