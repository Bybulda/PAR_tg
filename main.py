import configuration.configure as configure  # Содержит информацию о боте
import data_base_user as db  # Содержит функции для связи бд пользователей
import func_db as f_db  # Содержит функции для всех кнопок бота
import os  # Библиотека для правильной под-грузки файлов
import rt_base as r_db  # Содержит функции для связи бд root пользователей
import root_main as r_m  # Содержит функции для режима root пользователя
import telebot  # Библиотека для работы с системой бота
from telebot import types  # Импортируем для работы с кнопками
import texts as texts  # Содержит все текстовые наполнения сообщений бота

client = telebot.TeleBot(configure.config['token'])


# Выводит новое сообщение с кнопками с помощью "call"
def print_new_mess(call, text, markup_inline):
    client.send_message(chat_id=call.message.chat.id,
                        text=text,
                        reply_markup=markup_inline,
                        parse_mode='html')


# Изменяет сообщение с кнопки с помощью "call"
def edit_old_mess(call, text, markup_inline):
    client.edit_message_text(chat_id=call.message.chat.id,
                             message_id=call.message.message_id,
                             text=text,
                             reply_markup=markup_inline,
                             parse_mode='html')


# Выводит новое сообщение с кнопками с помощью "message"
def print_mess_com(message, text, markup_inline):
    client.send_message(message.chat.id,
                        text=text,
                        reply_markup=markup_inline,
                        parse_mode='html')


# Выводит сообщение об ошибке с кнопкой с помощью "message"
def problem_mes(message, text):
    client.send_message(message.chat.id, text, parse_mode='html')
    print_const_buttons(message, texts.sett_buttons,
                        texts.mes_sett(), ['◀ Назад', 'back_to_main'])


# Удаляет сообщение с помощью "message"
def delete_mess(call):
    client.delete_message(chat_id=call.message.chat.id,
                          message_id=call.message.message_id)


# Создает множество кнопок по заданному формату
def simply_inline_kb(but_list, dop, row=2):
    markup_inline = types.InlineKeyboardMarkup(row_width=row)
    for but_type in but_list:
        item1 = types.InlineKeyboardButton(text=but_type[0],
                                           callback_data=but_type[1])
        item2 = types.InlineKeyboardButton(text=but_type[2],
                                           callback_data=but_type[3])
        markup_inline.add(item1, item2)
    if dop is not None:
        item_dop = types.InlineKeyboardButton(text=dop[0], callback_data=dop[1])
        markup_inline.add(item_dop)
    return markup_inline


# Выводит сообщение бота, у которых есть "страницы"
def print_keyboard_w_pages(call, but_list, text, back, gen, page, from_place=0,
                           back_to=0, com=0):
    markup_inline, pages = types.InlineKeyboardMarkup(row_width=6), []
    if len(but_list) > 0:
        for but_type in but_list[page]:
            item = types.InlineKeyboardButton(text=but_type[0],
                                              callback_data=but_type[
                                                                1] + f'_{gen}')
            markup_inline.add(item)
    if from_place == 1:
        but_callback = f'kp'
    elif from_place == 2:
        but_callback = f'fp'
    else:
        but_callback = f'gp'
    for i in range(len(but_list)):
        if len(but_list) != 1:
            page_t = f'·{i + 1}·' if i == page else f'{i + 1}'
            item_p = types.InlineKeyboardButton(text=page_t,
                                                callback_data=f'{gen}_{but_callback}{i}')
            pages.append(item_p)
    markup_inline.add(*pages)
    item_dop = types.InlineKeyboardButton(text='◀ Назад', callback_data=back)
    markup_inline.add(item_dop)
    if back_to:
        if com:
            print_mess_com(call, text, markup_inline)
        else:
            print_new_mess(call, text, markup_inline)
    else:
        edit_old_mess(call, text, markup_inline)


# Выводит профиль заданной игры
def print_game_prof(call, name, but_list, text, back):
    markup_url = types.InlineKeyboardMarkup(row_width=2)
    for but_type in but_list:
        item_1 = types.InlineKeyboardButton(text=but_type[0], url=but_type[1])
        if but_type[2] in '🤍❤':
            item_2 = types.InlineKeyboardButton(text=but_type[2],
                                                callback_data=but_type[3])
        else:
            item_2 = types.InlineKeyboardButton(text=but_type[2],
                                                url=but_type[3])
        markup_url.add(item_1, item_2)
    item_dop = types.InlineKeyboardButton(text='◀ Назад', callback_data=back)
    markup_url.add(item_dop)
    photo = open(os.path.join('games_img', f'{name}.png'), 'rb')
    client.send_photo(call.message.chat.id, photo, caption=text,
                      reply_markup=markup_url, parse_mode='html')


# Выводит сообщение с кнопками с помощью "message"
def print_const_buttons(message, but_list, text, dop=None, row=2):
    markup_inline = simply_inline_kb(but_list, dop, row)
    client.send_message(message.chat.id, text,
                        parse_mode='html', reply_markup=markup_inline)


# Изменяет и выводит сообщение с кнопками с помощью "call"
def print_change_buttons(call, but_list, text, dop=None, row=2):
    markup_inline = simply_inline_kb(but_list, dop, row)
    edit_old_mess(call, text, markup_inline)


# Проверка на наличие ограничений у пользователя
def ch_banned(call, edit=0, prof=0):
    user_id = call.message.chat.id if edit else call.from_user.id
    time_diff = f_db.check_bane_time(r_db.get_ban_time(user_id))
    if time_diff < 120:
        time = round(((300 - time_diff) / 60), 2)
        if edit:
            if prof:
                client.delete_message(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                print_new_mess(call, texts.mes_ban_on(time), set())
            else:
                edit_old_mess(call, texts.mes_ban_on(time), set())
        else:
            print_mess_com(call, texts.mes_ban_on(time), set())
    else:
        db.update_info(user_id, 'banned', 0)
        print_mess_com(call, texts.mes_ban_off(), set())


# Выполняет функцию консольной команды "clear"
def root_clear(message, mes_amount):
    if mes_amount != 0:
        for i in range(mes_amount + 1):
            client.delete_message(message.chat.id, message.message_id - i)
    else:
        client.delete_message(message.chat.id, message.message_id)
    r_db.set_mess(message.from_user.id, 1)


# Выводит сообщение новым пользователям, добавляет пользователей в бд
def welcome(message):
    db.first_iter(message.from_user.id, message.from_user.first_name)
    stick = open(os.path.join('stickers', 'start_user.webp'), 'rb')
    client.send_sticker(message.chat.id, stick)
    client.send_message(message.chat.id,
                        texts.greetings(message.from_user.first_name),
                        parse_mode='html')
    db.add_favour(message.from_user.id, None)
    main_menu(message)


# Выводит сообщение основного меню
def main_menu(message):
    print_const_buttons(message, texts.menu_buttons,
                        texts.mes_main_menu(), ['⚙ Настройки', 'sett'])


# Выводит сообщение с категориями
def categories(call):
    print_change_buttons(call, texts.main_genre_buttons,
                         texts.mes_categories(), ['◀ Назад', 'back_to_main'])


# Выводит сообщение с рекомендациями
def recommend(call):
    print_keyboard_w_pages(*f_db.show_rek_games(call))


# Выводит сообщение с избранными играми
def favorite(call):
    print_keyboard_w_pages(*f_db.show_fav_games(call))


# Выводит сообщение с настройками
def settings(call):
    for i in ['nick_prog', 'gen_prog', 'cost_prog', 'curr_prog']:
        db.update_info(call.message.chat.id, i, False)
    print_change_buttons(call, texts.sett_buttons,
                         texts.mes_sett(), ['◀ Назад', 'back_to_main'])


# Выводит сообщение с информацией о проекте
def about_project(call):
    print_change_buttons(call, [], texts.mes_about(),
                         ['◀ Назад', 'back_to_main'])


# Обрабатывает ввод команды 'start'
@client.message_handler(commands=['start'])
def starting(message):
    if db.check_id_bd(message.from_user.id):
        welcome(message)
    else:
        if db.get_info(message.from_user.id, 'banned') != 1:
            main_menu(message)
        else:
            ch_banned(message)


# Обрабатывает ввод команды 'main_menu'
@client.message_handler(commands=['main_menu'])
def com_main_menu(message):
    if db.get_info(message.from_user.id, 'banned') != 1:
        print_const_buttons(message, texts.menu_buttons,
                            texts.mes_main_menu(), ['⚙ Настройки', 'sett'])
    else:
        ch_banned(message)


# Обрабатывает ввод команды 'recommend'
@client.message_handler(commands=['recommend'])
def com_recommend(message):
    if db.get_info(message.from_user.id, 'banned') != 1:
        print_keyboard_w_pages(*f_db.show_rek_games('', 0, 1, message))
    else:
        ch_banned(message)


# Обрабатывает ввод команды 'categories'
@client.message_handler(commands=['categories'])
def com_categories(message):
    if db.get_info(message.from_user.id, 'banned') != 1:
        print_const_buttons(message, texts.main_genre_buttons,
                            texts.mes_categories(), ['◀ Назад', 'back_to_main'])
    else:
        ch_banned(message)


# Обрабатывает ввод команды 'favorite'
@client.message_handler(commands=['favorite'])
def com_favorite(message):
    if db.get_info(message.from_user.id, 'banned') != 1:
        print_keyboard_w_pages(*f_db.show_fav_games('', 0, 1, message))
    else:
        ch_banned(message)


# Обрабатывает ввод команды 'about'
@client.message_handler(commands=['about'])
def com_about_project(message):
    if db.get_info(message.from_user.id, 'banned') != 1:
        print_const_buttons(message, [], texts.mes_about(),
                            ['◀ Назад', 'back_to_main'])
    else:
        ch_banned(message)


# Обрабатывает ввод команды 'settings'
@client.message_handler(commands=['settings'])
def com_settings(message):
    if db.get_info(message.from_user.id, 'banned') != 1:
        for i in ['nick_prog', 'gen_prog', 'cost_prog', 'curr_prog']:
            db.update_info(message.from_user.id, i, False)
        print_const_buttons(message, texts.sett_buttons,
                            texts.mes_sett(), ['◀ Назад', 'back_to_main'])
    else:
        ch_banned(message)


# Обрабатывает ввод команды 'root'
@client.message_handler(commands=['root'])
def com_root(message):
    db.update_info(message.from_user.id, 'root_proc', 1)


# Обрабатывает ввод команды 'end_root'
@client.message_handler(commands=['end_root'])
def com_end_root(message):
    r_db.set_mess(message.from_user.id, 1)
    if db.get_info(message.from_user.id, 'root_proc') == 1:
        db.update_info(message.from_user.id, 'root_proc', 0)
        r_db.update_root(message.from_user.id, 0)
        print_mess_com(message, r_m.mode_off(), set())


# Обрабатывает нажатия всех кнопок из сообщений бота
@client.callback_query_handler(func=lambda call: True)
def platform(call):
    if db.get_info(call.message.chat.id, 'banned') == 1:
        if call.data[:9] in ['back_fav', 'back_rek', 'back_form'] \
                or call.data[:3] == 's_f':
            ch_banned(call, 1, 1)
        else:
            ch_banned(call, 1)
    elif call.data == 'kat':
        categories(call)
    elif call.data == 'rek':
        recommend(call)
    elif call.data == 'fav':
        favorite(call)
    elif call.data == 'sett':
        settings(call)
    elif call.data == 'about':
        about_project(call)
    elif call.data.split('_')[0] == 'fav':
        if call.data == 'fav_nick':
            print_change_buttons(*f_db.open_nick(call, call.message.chat.id))
        elif call.data == 'fav_gen':
            print_change_buttons(*f_db.open_gen(call, call.message.chat.id))
        elif call.data == 'fav_cost':
            print_change_buttons(*f_db.open_cost(call, call.message.chat.id))
        elif call.data == 'fav_curr':
            print_change_buttons(*f_db.open_curr(call, call.message.chat.id))
    elif call.data.split('_')[0] == 'change':
        if call.data == 'change_nick':
            print_change_buttons(*f_db.change_nick(call, call.message.chat.id))
        elif call.data == 'change_gen':
            print_change_buttons(*f_db.change_gen(call, call.message.chat.id))
        elif call.data == 'change_cost':
            print_change_buttons(*f_db.change_cost(call, call.message.chat.id))
        elif call.data == 'change_curr':
            print_change_buttons(*f_db.change_curr(call, call.message.chat.id))
    elif call.data[:3] == 's_f':
        print_game_prof(*f_db.change_fav_status(call,
                                                call.data.split('_')[2],
                                                call.data.split('_')[3],
                                                '_'.join(
                                                    call.data.split('_')[4:])))
        delete_mess(call)
    elif call.data in ['set_rub', 'set_usd', 'set_eur', 'set_cny']:
        f_db.set_curr(call.message.chat.id, call.data)
        print_change_buttons(call, texts.prof_set_ed_but,
                             texts.mes_open_curr(
                                 db.get_info(call.message.chat.id,
                                             'fav_curr')))
    elif call.data in texts.genres_types.keys():
        f_db.set_gen(call.message.chat.id, call.data)
        print_change_buttons(call, texts.prof_set_ed_but,
                             texts.mes_open_gen(
                                 db.get_info(call.message.chat.id, 'fav_gen')))
    elif call.data[2:] in texts.genres_types.keys():
        print_keyboard_w_pages(*f_db.show_gen_games(call, call.data[2:], 0))
    elif call.data.split('_')[1][:2] in ['gp', 'kp', 'fp']:
        if call.data.split('_')[1][:2] == 'gp':
            print_keyboard_w_pages(
                *f_db.show_gen_games(call, call.data.split('_')[0],
                                     int(call.data.split('_')[1][2:])))
        elif call.data.split('_')[1][:2] == 'kp':
            print_keyboard_w_pages(*f_db.show_rek_games(call,
                                                        int(call.data.split(
                                                            '_')[1][
                                                            2:])))
        elif call.data.split('_')[1][:2] == 'fp':
            print_keyboard_w_pages(*f_db.show_fav_games(call,
                                                        int(call.data.split(
                                                            '_')[1][
                                                            2:])))
    elif 'game' in call.data.split('_')[1]:
        if call.data.split('_')[1] == 'game':
            print_game_prof(
                *f_db.show_game_prof(call, call.data.split('_')[0],
                                     call.data.split('_')[2], 0,
                                     db.check_fav(call.message.chat.id,
                                                  call.data.split('_')[0])))
            delete_mess(call)
        elif call.data.split('_')[1] == 'rekgame':
            print_game_prof(
                *f_db.show_game_prof(call, call.data.split('_')[0],
                                     call.data.split('_')[2], 1,
                                     db.check_fav(call.message.chat.id,
                                                  call.data.split('_')[0])))
            delete_mess(call)
        elif call.data.split('_')[1] == 'favgame':
            print_game_prof(
                *f_db.show_game_prof(call, call.data.split('_')[0],
                                     call.data.split('_')[2], 2, 1))
            delete_mess(call)
    elif call.data[:4] == 'back':
        if call.data[:9] == 'back_rek':
            print_keyboard_w_pages(*f_db.show_rek_games(call, 0, 1))
            delete_mess(call)
        elif call.data[:9] == 'back_fav':
            print_keyboard_w_pages(*f_db.show_fav_games(call, 0, 1))
            delete_mess(call)
        elif call.data[:9] == 'back_form':
            print_keyboard_w_pages(
                *f_db.show_gen_games(call, call.data.split('_')[4], 0, 1))
            delete_mess(call)
        elif call.data == 'back_to_sett':
            settings(call)
        elif call.data == 'back_to_main':
            print_change_buttons(call, texts.menu_buttons,
                                 texts.mes_main_menu(), ['⚙ Настройки', 'sett'])


# Обрабатывает ввод всех текстовых сообщений в чат
@client.message_handler(content_types=['text'])
def get_text(message):
    if db.check_id_bd(message.from_user.id):
        db.first_iter(message.from_user.id, message.from_user.first_name)
    elif db.get_info(message.from_user.id, 'banned') == 1:
        ch_banned(message)
    elif db.get_info(message.from_user.id, 'nick_prog') and \
            f_db.set_nick(message.from_user.id, message.text):
        print_const_buttons(message, texts.agree_nk_buttons,
                            texts.mes_open_nick(db.get_info(
                                message.from_user.id,
                                'fav_nick'), ' новый'))
    elif db.get_info(message.from_user.id, 'cost_prog') and \
            f_db.set_cost(message.from_user.id, message.text):
        print_const_buttons(message, texts.agree_cr_buttons,
                            texts.mes_new_cost(db.get_info(message.from_user.id,
                                                           'fav_cost'),
                                               db.get_info(message.from_user.id,
                                                           'fav_curr')))
    elif db.get_info(message.from_user.id, 'root_proc') == 1:
        r_db.set_mess(message.from_user.id)
        if message.text[0] == '@':
            if r_db.check_root_id(message.from_user.id):
                if r_db.get_root(message.from_user.id, message.text[1:]):
                    r_db.update_root(message.from_user.id, 1)
                    print_mess_com(message, r_m.mode_on(), set())
                else:
                    print_mess_com(message, 'Error!\nThe entered '
                                            'password is incorrect.', set())
            else:
                print_mess_com(message, 'Error!\nYou are not root user.', set())
        elif r_db.get_root(message.from_user.id, '', 1) and \
                message.text[0] == '-':
            if message.text == '-clear':
                root_clear(message,
                           (r_db.get_mess(message.from_user.id) - 1) * 2)
            else:
                print_mess_com(message, r_m.navi_root(message.text[1:]), set())
        else:
            print_mess_com(message, 'no such command', set())
    elif db.get_info(message.from_user.id, 'nick_prog') or \
            db.get_info(message.from_user.id, 'cost_prog'):
        db.update_info(message.from_user.id, 'nick_prog', False)
        db.update_info(message.from_user.id, 'curr_prog', False)
        problem_mes(message, texts.mes_change_mist())


client.polling(none_stop=True, interval=0)
