# Возвращает текст для сообщения с приветствием
def greetings(user_first_name):
    return f'Добро пожаловать, <b>{user_first_name}</b>! 😃\n' \
           f'Теперь ты можешь подобрать для себя игру из <b>Steam</b>.\n\n' \
           f'Удачи! 😉'


# Возвращает текст для сообщения главного меню
def mes_main_menu():
    return f'Пользуйся предоставленными кнопками, а также не забывай \n' \
           f'про дополнительное <b>Меню</b> внизу экрана.'


# Возвращает текст для сообщения категорий игр
def mes_categories():
    return f'Выберете одну из предоставленных категорий:'


# Возвращает текст для сообщения с настройками
def mes_sett():
    return f'В данном модуле ты можешь настроить свой профиль:'


# Возвращает текст для сообщения с информацией о проекте
def mes_about():
    return f'🤵 Проект создали <b>Соловьев Степан</b> и <b>Смирнов Никита</b>.\n' \
           f'Также активное участие в расширении проекта принимали:\n' \
           f'@Saas12211221 - Пантелеев Артём\n' \
           f'@plutarkh4 - Томашевская Александра\n\n' \
           f'💸 Если вы хотите поддержать на проект, можете кинуть\n' \
           f'пару Toncoin на этот криптокошелек: \n' \
           f'<code>EQAcIQb66BlFoIoQj-e-' \
           f'gYUeCh6ZCOXmaqCFHAOeIwknVUmo</code>\n\n' \
           f'⚙ Написать в поддержку можно по этим ссылкам:\n' \
           f'@fatman_of - Соловьев Степан\n' \
           f'@Makkre - Смирнов Никита\n'


# Возвращает текст для сообщения о никнейме пользователя
def mes_open_nick(nick, new=''):
    return f'👤 Ваш{new} никнейм - <b>{nick}</b>\n'


# Возвращает текст для сообщения о любимом жанре пользователя
def mes_open_gen(genre):
    return f'🤍 Ваш любимый жанр игр - <b>{genre}</b>.\n' \
           f'Вы хотите изменить предпочитаемый жанр?'


# Возвращает текст для сообщения о макс. цене пользователя
def mes_open_cost(cost, my_curr):
    show_c = ' ' + my_curr if cost is not None else ''
    if cost is None:
        cost = 'не определена'
    return f'💰 Максимальная цена игр - {cost}{show_c}\n' \
           f'Вы хотите изменить максимальную цену?'


# Возвращает текст для сообщения о новой валюте маркета
def mes_new_cost(new_cost, my_curr):
    return f'💰 Новая максимальная цена - <b>{new_cost} {my_curr}</b>.'


# Возвращает текст для сообщения о валюте маркета
def mes_open_curr(curr):
    return f'💸 Валюта маркета - {curr}\n' \
           f'Вы хотите изменить валюту маркета?'


# Возвращает правила для сообщения о смене никнейма
def mes_change_nick():
    return f'<b>Отлично!</b> Для изменения своего никнейма\n' \
           f'Напишите в чат свою версию, соблюдая два условия:\n' \
           f'1) Длина нового ника должна быть от <b>2</b> ' \
           f'до <b>16</b> символов\n' \
           f'2) Новый ник может состоять <b>только</b> из символов \n' \
           f'кириллицы или <b>только</b> из символов латиницы.\n\n' \
           f'📍 Если вы передумали изменять свой никнейм,\n' \
           f'воспользуйтесь кнопкой "Назад".'


# Возвращает правила для сообщения о смене любимого жанра
def mes_change_gen():
    return f'🤍 Для изменения любимого жанра выберите один\n' \
           f'из предоставленных ниже вариантов.\n\n' \
           f'📍 Если вы передумали менять любимый жанр,\n' \
           f'воспользуйтесь кнопкой "Назад".'


# Возвращает правила для сообщения о смене максимальной цены
def mes_change_cost():
    return f'💰 Для изменения максимальной цены показываемых игр\n' \
           f'введите в чат целое не отрицательной число.\n\n' \
           f'<b>Помните</b>: вы указываете сумму в выбранной валюте маркета!\n\n' \
           f'📍 Если вы передумали изменять данный параметр,\n' \
           f'воспользуйтесь кнопкой "Назад".'


# Возвращает текст для сообщения об ошибке смены параметра профиля
def mes_change_mist():
    return f'<b>Ошибка</b> ❗\n' \
           f'Параметр не был изменен.\n' \
           f'Внимательно прочитайте условия для ' \
           f'смены\n' \
           f'этого параметра и попробуйте ещё раз. 👌'


# Возвращает текст для сообщения об включении ограниченного доступа
def mes_ban_on(time):
    return f'<b>Вам запрещен доступ к командам бота</b> ❗\n\n' \
           f'Возможные причины ограничений:\n' \
           f'1) Большое количество сообщений, отправленных боту\n' \
           f'2) Вами был выбран оскорбительный никнейм\n\n' \
           f'После отмены ограничений не нарушайте эти правила !\n' \
           f'До снятия ограничений осталось <b>{time} минут.</b>'


# Возвращает текст для сообщения об выключении ограниченного доступа
def mes_ban_off():
    return f'<b>Вам разрешен доступ к командам бота</b> ❗\n\n' \
           f'Чтобы продолжить, повторно нажмите кнопку\n' \
           f'или заново вызовите последнюю команду.\n\n' \
           f'Больше не нарушайте правила бота ❗\n'


# Возвращает правила для сообщения о смене валюты маркета
def mes_change_curr():
    return f'💸 Для изменения валюты маркета выберите один\n' \
           f'из предоставленных ниже вариантов мировой валюты.\n\n' \
           f'📍 Если вы передумали изменять валюту маркета,\n' \
           f'воспользуйтесь кнопкой "Назад".'


# Возвращает текст для сообщения о рекомендованных играх
def mes_show_rek(nick):
    return f'📕 {nick}, в этой категории мы подготовили для вас\n' \
           f'список игр на основе ваших предпочтений:'


# Возвращает текст для сообщения об избранных играх
def mes_show_fav():
    return f'<b>Избранные игры:</b>'


# Возвращает текст для сообщения о пустом списке рекомендованных игр
def mes_show_rek_mist():
    return 'Пока мы не можем порекомендовать вам ни одну игру. 😔\n\n' \
           'Скорее всего, у вас не выбран <b>любимый жанр</b> или\n' \
           'не определена <b>максимальная цена</b>.\n\n' \
           'Проверьте эти параметры ещё раз, и список рекомендаций обновится! 😃'


# Возвращает текст для сообщения о пустом списке избранных игр
def mes_show_fav_mist():
    return 'Ваш список избранных игр пуст. 😔\n'


# Возвращает текст для сообщения с играми определенно жанра
def mes_show_gen(gen):
    return f'Выберите игру из жанра <b>{genres_types[gen][0]}</b>'


# Возвращает текст для сообщения профиля игры
def mes_game_prof(game_info, curr):
    return f'<b>{game_info[0]}</b>\n' \
           f'<b>Жанр: {genres_types[game_info[-1]][0]}\n</b>' \
           f'<b>Цена: {game_info[-2]} {curr}</b>'


# Возвращает список кнопок для профиля игры
def game_prof_buttons(game_inf, name, in_fav, gen, backed):
    if in_fav:
        return [['Steam 🖥', f'{game_inf[1]}', '❤', f's_f_{name}_{gen}_{backed}'],
                ['Gameplay 🎮', f'{game_inf[3]}', 'Metacritic 📕', f'{game_inf[2]}']]
    return [['Steam 🖥', f'{game_inf[1]}', '🤍', f's_f_{name}_{gen}_{backed}'],
            ['Gameplay 🎮', f'{game_inf[3]}', 'Metacritic 📕', f'{game_inf[2]}']]


# Возвращает нужную строку по ключу - жанру
genres_types = {'soul': ['Souls-like', 'rog'],
                'shoot': ['Shooters', 'strategy'],
                'rog': ['Roguelike', 'soul'], 'sur': ['Survival', 'horr'],
                'strategy': ['Strategy', 'shoot'], 'hor': ['Horror', 'sur']}

# Возвращает нужную строку по ключу - названию жанра
for_rek = {'Souls-like': 'soul', 'Shooters': 'shoot',
           'Roguelike': 'rog', 'Survival': 'sur',
           'Strategy': 'strategy', 'Horror': 'hor'}

# Список кнопок для сообщения о категориях игр
main_genre_buttons = [['⚔ Souls-like', 'm_soul', '🔫 Shooters', 'm_shoot'],
                      ['🛡 Roguelike', 'm_rog', '🏹 Survival', 'm_sur'],
                      ['🤔 Strategy', 'm_strategy', '👻 Horror', 'm_hor']]

# Список кнопок для сообщения о смене любимого жанра
ch_genre_buttons = [['⚔ Souls-like', 'soul', '🔫 Shooters', 'shoot'],
                    ['🛡 Roguelike', 'rog', '🏹 Survival', 'sur'],
                    ['🤔 Strategy', 'strategy', '👻 Horror', 'hor']]


# Содержит информацию о курсе разных валют (нужен для смены основной валюты)
curr_exchange_rate = {'RUB': 0.0091, 'USD': 0.7625,
                      'EUR': 0.8415, 'CNY': 0.1200}

# Список кнопок для сообщения основного меню
menu_buttons = [['👍 Рекомендации', 'rek', '📘 Категории', 'kat'],
                ['💫 Избранное', 'fav', 'ℹ О проекте', 'about']]

# Список кнопок для сообщения настроек профиля пользователя
sett_buttons = [['Мой nickname 👤', 'fav_nick', 'Любимый жанр ❤', 'fav_gen'],
                ['Максимальная цена 💰', 'fav_cost',
                 'Основная валюта 💳', 'fav_curr']]

# Список кнопок для сообщения о смене валюты маркета
change_curr_buttons = [['₽ RUB 🇷🇺', 'set_rub', '$ USD 🇺🇸', 'set_usd'],
                       ['€ EUR 🇪🇺', 'set_eur', '¥ CNY 🇨🇳', 'set_cny']]

# Список кнопок для сообщения о смене параметра профиля
prof_set_ed_but = [['◀ Назад', 'back_to_sett', 'Изменить ✏', '']]

# Список кнопок для сообщения о смене параметра профиля
agree_nk_buttons = [['Изменить ✏', 'change_nick', 'Сохранить ✅', 'back_to_sett']]

# Список кнопок для сообщения о смене параметра профиля
agree_cr_buttons = [['Изменить ✏', 'change_cost', 'Сохранить ✅', 'back_to_sett']]
