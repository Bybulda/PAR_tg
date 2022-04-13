def greetings(user_first_name):
    return f'Добро пожаловать, {user_first_name}! 😃\n' \
           f'Теперь ты можешь подобрать для себя игру из <b>Steam</b>.\n\n' \
           f'Удачи! 😉'


def mess_main_menu():
    return f'Пользуйся предоставленными кнопками, а также не забывай \n' \
           f'про дополнительное <b>Меню</b> внизу экрана.'


def mess_categories():
    return f'Выберете одну из предоставленных категорий:'


def mess_sett():
    return f'В данном модуле ты можешь настроить свой профиль:'


def mess_about():
    return f'🤵 Проект создали Соловьев Степан и Смирнов Никита.\n' \
           f'Также активное участие в расширении проекта принимал\n' \
           f'@Saas12211221 - Пантелеев Артём\n\n' \
           f'💸 Если вы хотите поддержать на проект, можете кинуть\n' \
           f'пару Toncoin на этот криптокошелек: \n' \
           f'<code>EQAcIQb66BlFoIoQj-e-' \
           f'gYUeCh6ZCOXmaqCFHAOeIwknVUmo</code>\n\n' \
           f'⚙ Написать в поддержку можно по этим ссылкам:\n' \
           f'@Makkre - Смирнов Никита\n' \
           f'@fatman_of - Соловьев Степан\n'


def mess_open_nick(nick):
    return f'Ваш никнейм - {nick}\n'


def mes_new_nick(nick):
    return f'Ваш новый никнейм - <b>{nick}</b>.'


def mess_open_gen(genre):
    return f'Ваш любимый жанр игр - {genre}.\n' \
           f'Вы хотите изменить предпочитаемый жанр?'


def mess_open_cost(cost, my_curr):
    show_c = ' ' + my_curr if cost != 'не определена' else ''
    return f'Максимальная цена предлагаемых игр - {cost}{show_c}\n' \
           f'Вы хотите изменить максимальную цену?'


def mes_new_cost(new_cost, my_curr):
    return f'Новая максимальная цена - <b>{new_cost} {my_curr}</b>.'


def mess_open_curr(curr):
    return f'Валюта маркета - {curr}\n' \
           f'Вы хотите изменить валюту маркета?'


def mess_change_nick():
    return f'Отлично! Для изменения своего никнейма\n' \
           f'Напишите в чат свою версию, соблюдая два условия:\n' \
           f'1) Длина нового ника должна быть от 2 до 10 символов\n' \
           f'2) Новый ник может состоять только из символов \n' \
           f'кириллицы или только из символов латиницы.\n\n' \
           f'Если вы передумали изменять свой никнейм,\n' \
           f'воспользуйтесь кнопкой "Назад".'


def mess_change_gen():
    return f'Для изменения любимого жанра выберите один\n' \
           f'из предоставленных ниже вариантов.\n\n' \
           f'Если вы передумали менять любимый жанр,\n' \
           f'воспользуйтесь кнопкой "Назад".'


def mess_change_cost():
    return f'Для изменения максимальной цены показываемых игр\n' \
           f'введите в чат целое не отрицательной число.\n\n' \
           f'Помните: вы указываете сумму в выбранной валюте маркета!\n\n' \
           f'Если вы передумали изменять данный параметр,\n' \
           f'воспользуйтесь кнопкой "Назад".'


def mess_change_mist():
    return f'<b>Ошибка</b> ❗\n' \
           f'Параметр не был изменен.\n' \
           f'Внимательно прочитайте условия для ' \
           f'смены\n' \
           f'этого параметра и попробуйте ещё раз. 👌'


def mess_change_curr():
    return f'Для изменения валюты маркета выберите один\n' \
           f'из предоставленных ниже вариантов мировой валюты.\n\n' \
           f'Если вы передумали изменять валюту маркета,\n' \
           f'воспользуйтесь кнопкой "Назад".'


def mess_show_rek():
    return f'В этой категории мы подготовили для вас\n' \
           f'список игр на основе ваших предпочтений:'


def mess_show_rek_mist():
    return 'Пока мы не можем порекомендовать вам ни одну игру. 😔\n\n' \
           'Скорее всего, у вас не выбран любимый жанр или\n' \
           'не определена максимальная цена.\n\n' \
           'Проверьте эти параметры ещё раз, и список рекомендаций обновится! 😃'


def mess_show_gen(gen):
    return f'Выберите игру из жанра <b>{genres_types[gen][0]}</b>'


def mess_game_prof(game_info, curr):
    return f'<b>{game_info[0]}</b>\n' \
           f'<b>Жанр: {genres_types[game_info[-1]][0]}\n</b>' \
           f'<b>Цена: {game_info[-2]} {curr}</b>'


def game_prof_buttons(game_info):
    return [['Steam', f'{game_info[1]}', '🤍', f'{game_info[1]}'],
            ['Gameplay', f'{game_info[3]}', 'Metacritic', f'{game_info[2]}']]


genres_types = {'soul': ['Souls-like', 'rog'],
                'shoot': ['Shooters', 'strategy'],
                'rog': ['Roguelike', 'soul'], 'sur': ['Survival', 'horr'],
                'strategy': ['Strategy', 'shoot'], 'hor': ['Horror', 'sur']}

for_rek = {'Souls-like': 'soul', 'Shooters': 'shoot',
           'Roguelike': 'rog', 'Survival': 'sur',
           'Strategy': 'strategy', 'Horror': 'hor'}

curr_exchange_rate = {'RUB': 0.0091, 'USD': 0.7625,
                      'EUR': 0.8415, 'CYN': 0.1200}

menu_buttons = [['👍 Рекомендации', 'rek', '📘 Категории', 'kat'],
                ['💫 Избранное', 'fav', 'ℹ О проекте', 'about']]

main_genre_buttons = [['⚔ Souls-like', 'm_soul', '🔫 Shooters', 'm_shoot'],
                      ['🛡 Roguelike', 'm_rog', '🏹 Survival', 'm_sur'],
                      ['🤔 Strategy', 'm_strategy', '👻 Horror', 'm_hor']]

ch_genre_buttons = [['⚔ Souls-like', 'soul', '🔫 Shooters', 'shoot'],
                    ['🛡 Roguelike', 'rog', '🏹 Survival', 'sur'],
                    ['🤔 Strategy', 'strategy', '👻 Horror', 'hor']]

sett_buttons = [['Мой nickname', 'fav_nick', 'Любимый жанр', 'fav_gen'],
                ['Максимальная цена', 'fav_cost',
                 'Основная валюта', 'fav_curr']]

change_curr_buttons = [['₽ RUB', 'set_rub', '$ USD', 'set_usd'],
                       ['€ EUR', 'set_eur', '¥ CNY', 'set_cny']]

profile_sett_buttons = [['◀ Назад', 'back_to_sett', 'Изменить', '']]

agree_nk_buttons = [['Изменить', 'change_nick', 'Сохранить', 'back_to_sett']]

agree_cr_buttons = [['Изменить', 'change_cost', 'Сохранить', 'back_to_sett']]
