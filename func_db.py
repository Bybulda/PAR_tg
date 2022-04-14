import data_base_user as db
import game_base as gb
import texts


def open_nick(call, user_id):
    texts.profile_sett_buttons[0][3] = 'change_nick'
    return [call, texts.profile_sett_buttons,
            texts.mess_open_nick(db.get_info(user_id, 'fav_nick'))]


def open_gen(call, user_id):
    texts.profile_sett_buttons[0][3] = 'change_gen'
    return [call, texts.profile_sett_buttons,
            texts.mess_open_gen(db.get_info(user_id, 'fav_gen'))]


def open_cost(call, user_id):
    texts.profile_sett_buttons[0][3] = 'change_cost'
    return [call, texts.profile_sett_buttons,
            texts.mess_open_cost(db.get_info(user_id, 'fav_cost'),
                                 db.get_info(user_id, 'fav_curr'))]


def open_curr(call, user_id):
    texts.profile_sett_buttons[0][3] = 'change_curr'
    return [call, texts.profile_sett_buttons,
            texts.mess_open_curr(db.get_info(user_id, 'fav_curr'))]


def change_nick(call, user_id):
    db.update_info(user_id, 'nick_prog', True)
    return [call, '', texts.mess_change_nick(), ['◀ Назад', 'back_to_sett']]


def change_gen(call, user_id):
    db.update_info(user_id, 'gen_prog', True)
    return [call, texts.ch_genre_buttons,
            texts.mess_change_gen(), ['◀ Назад', 'back_to_sett']]


def change_cost(call, user_id):
    db.update_info(user_id, 'cost_prog', True)
    return [call, '', texts.mess_change_cost(), ['◀ Назад', 'back_to_sett']]


def change_curr(call, user_id):
    db.update_info(user_id, 'curr_prog', True)
    return [call, texts.change_curr_buttons,
            texts.mess_change_curr(), ['◀ Назад', 'back_to_sett']]


def set_nick(user_id, new_nick):
    if 11 > len(new_nick) > 1:
        eng_let = all(91 > ord(let.upper()) > 64 for let in new_nick)
        rus_let = all(1072 > ord(let.upper()) > 1039 for let in new_nick)
        if eng_let or rus_let:
            db.update_info(user_id, 'nick_prog', False)
            db.update_info(user_id, 'fav_nick', new_nick)
            return True
    return False


def set_gen(user_id, new_gen):
    db.update_info(user_id, 'gen_prog', False)
    db.update_info(user_id, 'fav_gen', texts.genres_types[new_gen][0])


def set_cost(user_id, new_cost):
    if int(new_cost) >= 0 and int(new_cost) % 1 == 0:
        db.update_info(user_id, 'cost_prog', False)
        db.update_info(user_id, 'fav_cost', int(new_cost))
        return True
    return False


def set_curr(user_id, new_curr):
    new_c = new_curr[4:].upper()
    if db.get_info(user_id, 'fav_cost') != 'не определена':
        old_c = db.get_info(user_id, 'fav_curr')
        fav_cost = db.get_info(user_id, 'fav_cost')
        new_fav_cost = int((texts.curr_exchange_rate[old_c] *
                            fav_cost) / texts.curr_exchange_rate[new_c])
        db.update_info(user_id, 'fav_cost', new_fav_cost)
    db.update_info(user_id, 'curr_prog', False)
    db.update_info(user_id, 'fav_curr', new_c)


def show_gen_games(call, gen, page, back_from=0):
    return [call, gb.categ_lst(gen), texts.mess_show_gen(gen), 'kat', gen,
            page, 0, back_from]


def show_rek_games(call, page=0, back_from=0):
    fav_gen = db.get_info(call.message.chat.id, 'fav_gen')
    cost = db.get_info(call.message.chat.id, 'fav_cost')
    if fav_gen == 'не выбран' or cost == 'не определена':
        return [call, [], texts.mess_show_rek_mist(), 'back_to_main', '',
                0, 1, back_from]
    gen_1 = texts.for_rek[fav_gen]
    gen_2 = texts.genres_types[gen_1][1]
    curr = db.get_info(call.message.chat.id, 'fav_curr')
    return [call, gb.rec(gen_1, gen_2, cost, curr), texts.mess_show_rek(),
            'back_to_main', gen_1, page, 1, back_from]


def show_fav_games(call, page=0, back_from=0):
    mist = False
    if mist:
        return [call, [], texts.mess_show_rek_mist(), 'back_to_main', '',
                0, 1, back_from]
    return [call, db.get_favourite(call.message.chat.id), texts.mess_show_fav(),
            'back_to_main', 'favgen', page, 2, back_from]


def show_game_prof(call, name, gen, back_to, in_fav):
    curr = db.get_info(call.message.chat.id, 'fav_curr')
    game_info = gb.game_info(name, curr)
    if back_to == 0:
        back_text = f'back_form_pf_to_{gen}'
    elif back_to == 1:
        back_text = 'back_rek'
    else:
        back_text = 'back_fav'
    return [call, name.replace(':', ''), texts.game_prof_buttons(game_info, name, in_fav, gen, back_text),
            texts.mess_game_prof(game_info, curr),
            back_text]


def change_fav_status(call, name, gen, back):
    if not db.get_favourite(call.message.chat.id, name):
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
