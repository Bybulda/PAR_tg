import configure  # Файл, содержащий уникальную информацию о боте
import data_base_user as db
import func_db as f_db
import os  # Библиотека для правильной под-грузки файлов
import telebot  # Библиотека для работы с системой бота
from telebot import types  # Импортируем для работы с кнопками
import texts

client = telebot.TeleBot(configure.config['token'])
print('Бот работает!')

# Функция выводит пользователю предупреждение о неправильном формате сообщения
def problem_mes(message, text):
    client.send_message(message.chat.id, text, parse_mode='html')
    print_const_buttons(message, texts.sett_buttons,
                        texts.mess_sett(), ['◀ Назад', 'back_to_main'])


def ans_change_sett(call, mes_text):
    print_change_buttons(call, texts.profile_sett_buttons, mes_text)


def made_inline_keyboard(but_list, dop, row=2):
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


def print_keyboard_w_pages(call, but_list, text, back, gen, page, from_rek=0,
                           back_from=0):
    markup_inline, pages = types.InlineKeyboardMarkup(row_width=4), []
    if len(but_list) > 0:
        for but_type in but_list[page]:
            item = types.InlineKeyboardButton(text=but_type[0],
                                              callback_data=but_type[1] + f'_{gen}')
            markup_inline.add(item)
    for i in range(len(but_list)):
        page_t = f'·{i + 1}·' if i == page else f'{i + 1}'
        but_callback = f'{gen}_kp{i}' if from_rek else f'{gen}_p{i}'
        item_p = types.InlineKeyboardButton(text=page_t,
                                            callback_data=but_callback)
        pages.append(item_p)
    markup_inline.add(*pages)
    item_dop = types.InlineKeyboardButton(text='◀ Назад', callback_data=back)
    markup_inline.add(item_dop)
    if back_from:
        client.send_message(chat_id=call.message.chat.id,
                            text=text,
                            reply_markup=markup_inline,
                            parse_mode='html')
    else:
        client.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text=text,
                                 reply_markup=markup_inline,
                                 parse_mode='html')


def print_game_prof(call, name, but_list, text, back):
    markup_url = types.InlineKeyboardMarkup(row_width=2)
    for but_type in but_list:
        item_1 = types.InlineKeyboardButton(text=but_type[0],
                                            url=but_type[1])
        item_2 = types.InlineKeyboardButton(text=but_type[2],
                                            url=but_type[3])
        markup_url.add(item_1, item_2)
    item_dop = types.InlineKeyboardButton(text='◀ Назад', callback_data=back)
    markup_url.add(item_dop)
    photo = open(os.path.join('games_img', f'{name}.png'), 'rb')
    client.send_photo(call.message.chat.id, photo, caption=text,
                      reply_markup=markup_url, parse_mode='html')


def print_const_buttons(message, but_list, text, dop=None, row=2):
    markup_inline = made_inline_keyboard(but_list, dop, row)
    client.send_message(message.chat.id, text,
                        parse_mode='html', reply_markup=markup_inline)


def print_change_buttons(call, but_list, text, dop=None, row=2):
    markup_inline = made_inline_keyboard(but_list, dop, row)
    client.edit_message_text(chat_id=call.message.chat.id,
                             message_id=call.message.message_id,
                             text=text,
                             reply_markup=markup_inline,
                             parse_mode='html')


def delete_mess(call):
    client.delete_message(chat_id=call.message.chat.id,
                          message_id=call.message.message_id)


def welcome(message):
    db.first_iter(message.from_user.id, message.from_user.first_name)
    stick = open(os.path.join('stickers', 'start_user.webp'), 'rb')
    client.send_sticker(message.chat.id, stick)
    client.send_message(message.chat.id,
                        texts.greetings(message.from_user.first_name),
                        parse_mode='html')
    main_menu(message)


def main_menu(message):
    print_const_buttons(message, texts.menu_buttons,
                        texts.mess_main_menu(), ['⚙ Настройки', 'sett'])


def categories(call):
    print_change_buttons(call, texts.main_genre_buttons,
                         texts.mess_categories(), ['◀ Назад', 'back_to_main'])


def recommend(call):
    print_keyboard_w_pages(*f_db.show_rek_games(call))


def favorite(call):
    pass


def settings(call):
    for i in ['nick_prog', 'gen_prog', 'cost_prog', 'curr_prog']:
        db.update_info(call.message.chat.id, i, False)
    print_change_buttons(call, texts.sett_buttons,
                         texts.mess_sett(), ['◀ Назад', 'back_to_main'])


def about_project(call):
    print_change_buttons(call, [], texts.mess_about(),
                         ['◀ Назад', 'back_to_main'])


@client.message_handler(commands=['start'])
def starting(message):
    if db.check_id_bd(message.from_user.id):
        welcome(message)
    else:
        main_menu(message)


@client.callback_query_handler(func=lambda call: True)
def platform(call):
    print(call.data)
    if call.data == 'kat':
        categories(call)
    elif call.data == 'rek':
        recommend(call)
    elif call.data == 'fav':
        pass
    elif call.data == 'sett':
        settings(call)
    elif call.data == 'about':
        about_project(call)
    elif call.data == 'fav_nick':
        print_change_buttons(*f_db.open_nick(call, call.message.chat.id))
    elif call.data == 'fav_gen':
        print_change_buttons(*f_db.open_gen(call, call.message.chat.id))
    elif call.data == 'fav_cost':
        print_change_buttons(*f_db.open_cost(call, call.message.chat.id))
    elif call.data == 'fav_curr':
        print_change_buttons(*f_db.open_curr(call, call.message.chat.id))
    elif call.data == 'change_nick':
        print_change_buttons(*f_db.change_nick(call, call.message.chat.id))
    elif call.data == 'change_gen':
        print_change_buttons(*f_db.change_gen(call, call.message.chat.id))
    elif call.data == 'change_cost':
        print_change_buttons(*f_db.change_cost(call, call.message.chat.id))
    elif call.data == 'change_curr':
        print_change_buttons(*f_db.change_curr(call, call.message.chat.id))
    elif call.data in texts.genres_types.keys():
        f_db.set_gen(call.message.chat.id, call.data)
        ans_change_sett(call,
                        texts.mess_open_gen(
                            db.get_info(call.message.chat.id, 'fav_gen')))
    elif call.data in ['set_rub', 'set_usd', 'set_eur', 'set_cny']:
        f_db.set_curr(call.message.chat.id, call.data)
        ans_change_sett(call,
                        texts.mess_open_curr(
                            db.get_info(call.message.chat.id, 'fav_curr')))
    elif call.data[2:] in texts.genres_types.keys():
        print_keyboard_w_pages(*f_db.show_gen_games(call, call.data[2:], 0))
    elif call.data.split('_')[1][0] == 'p':
        print_keyboard_w_pages(
            *f_db.show_gen_games(call, call.data.split('_')[0],
                                 int(call.data.split('_')[1][1:])))
    elif call.data.split('_')[1][:2] == 'kp':
        print_keyboard_w_pages(*f_db.show_rek_games(call,
                               int(call.data.split('_')[1][2:])))
    elif call.data.split('_')[1] == 'game':
        print_game_prof(
            *f_db.show_game_prof(call, call.data.split('_')[0],
                                 call.data.split('_')[2]))
        delete_mess(call)
    elif call.data.split('_')[1] == 'rekgame':
        print_game_prof(
            *f_db.show_game_prof(call, call.data.split('_')[0],
                                 call.data.split('_')[2], 1))
        delete_mess(call)
    elif call.data[:9] == 'back_rek':
        print_keyboard_w_pages(*f_db.show_rek_games(call, 0, 1))
        delete_mess(call)
    elif call.data[:9] == 'back_form':
        print_keyboard_w_pages(
            *f_db.show_gen_games(call, call.data.split('_')[4], 0, 1))
        delete_mess(call)
    elif call.data == 'back_to_sett':
        settings(call)
    elif call.data == 'back_to_main':
        print_change_buttons(call, texts.menu_buttons,
                             texts.mess_main_menu(), ['⚙ Настройки', 'sett'])


@client.message_handler(content_types=['text'])
def get_text(message):
    if db.get_info(message.from_user.id, 'nick_prog') and \
            f_db.set_nick(message.from_user.id, message.text):
        print_const_buttons(message, texts.agree_nk_buttons,
                            texts.mes_new_nick(db.get_info(message.from_user.id,
                                                           'fav_nick')))
    elif db.get_info(message.from_user.id, 'cost_prog') and \
            f_db.set_cost(message.from_user.id, message.text):
        print_const_buttons(message, texts.agree_cr_buttons,
                            texts.mes_new_cost(db.get_info(message.from_user.id,
                                                           'fav_cost'),
                                               db.get_info(message.from_user.id,
                                                           'fav_curr')))
    elif db.get_info(message.from_user.id, 'nick_prog') or \
            db.get_info(message.from_user.id, 'cost_prog'):
        db.update_info(message.from_user.id, 'nick_prog', False)
        db.update_info(message.from_user.id, 'curr_prog', False)
        problem_mes(message, texts.mess_change_mist())


client.polling(none_stop=True, interval=0)
