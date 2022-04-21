import rt_base as r_db
import data_base_user as db
import game_base as gb


def com_mist_arg(com, arg='', good=0):
    if good:
        return 'done'
    elif len(arg) != 0:
        return f"reading error\n" \
               f"command '{com}' has no such argument: {arg}"
    return f"reading error\n" \
           f"command format '{com}' is not correct"


def help(com):
    return f'1. -help (-h)\n' \
           f'    список доступных команд\n\n' \
           f'2. -users (-u)\n' \
           f'    общая информация о пользователях\n\n' \
           f'3. -delete (-d, -del)\n' \
           f'    удаление профиля человека:\n' \
           f'    "[-u, -user]: [id пользователя] [-p, -prof, -profile]"\n' \
           f'    -----------------------------------------------------\n' \
           f'    удаление избранного человека:\n' \
           f'    "[-u, -user]: [id пользователя] [-f, -fav, -favorite]"\n' \
           f'    -----------------------------------------------------\n' \
           f'    удаление игры из базы данных:\n' \
           f'    "[-g, -game]: [название игры]"\n\n' \
           f'4. -stat (-s)\n' \
           f'    статистика любимых жанров:\n' \
           f'    "[-g, -gen, -genre]"\n' \
           f'    -----------------------------------------------------\n' \
           f'    средняя максимальная цена:\n' \
           f'    "[-c, -cost]"\n\n' \
           f'5. -game (-g)\n' \
           f'    изменение информация об игре:\n' \
           f'    "[-c, -ch, -change]: [название игры] ' \
           f'[-name, -cost, -yt]: [новое значение]"\n\n' \
           f'6. -ban (-b)\n' \
           f'    забанить/разбанить пользователя:\n' \
           f'    "[-u, -user]: [id пользователя] [-t (-true), ' \
           f'-f (-false)]"\n\n' \
           f'7. -clear\n' \
           f'    очистить все сообщения, которые выводились в режиме root'


def users(com):
    if len(com[1:]) > 0:
        return com_mist_arg(com[0], com[1])
    return r_db.get_user_info()


def delete(com):
    if not (1 < len(com) < 4):
        return com_mist_arg(" ".join(com))
    elif com[1].split(":")[0] in ['u', 'user']:
        if len(com[1].split(":")) > 1:
            if com[2] in ['p', 'prof', 'profile']:
                r_db.del_any(int(com[1].split(":")[1]), 'user_all', 'user_data')
                return com_mist_arg(com, '', 1)
            elif com[2] in ['f', 'fav', 'favorite']:
                r_db.del_any(int(com[1].split(":")[1]), 'game', 'favorite')
                return com_mist_arg(com, '', 1)
            return com_mist_arg(com[0] + ' ' + com[1], com[3])
        return com_mist_arg(com[0] + ' ' + com[1])
    elif com[1].split(":")[0] in ['g', 'game']:
        if len(com[1].split(":")) > 1:
            r_db.del_any(com[1].split(":")[1], 'game', 'game_data')
            return com_mist_arg(com, '', 1)
        return com_mist_arg(com[0] + ' ' + com[1])
    return com_mist_arg(com[0], com[1])


def stat(com):
    if not len(com) in [2, 3]:
        return com_mist_arg(" ".join(com))
    elif com[1] in ['g', 'gen', 'genre']:
        return '\n\n'. join(r_db.get_stat('fav_gen'))
    elif com[1] in ['c', 'cost']:
        return r_db.get_stat('avg_price')
    return com_mist_arg(com[0], com[1])


def game(com):
    if len(com) != 3:
        if com[2][:4] == 'cost':
            return 'Error!\nThe price of the game cannot be less than zero'
        return com_mist_arg(" ".join(com))
    elif com[1].split(":")[0] in ['c', 'ch', 'change']:
        if len(com[1].split(":")) > 1:
            name = com[1].split(":")[1]
            if len(gb.game_info(name, 'RUB')) > 0:
                if len(com[2].split(":")) > 1:
                    what = com[2].split(":")[0]
                    if what == 'yt':
                        r_db.ch_game_info(name, -1, com[2].split(":")[1])
                        return com_mist_arg(com, '', 1)
                    elif what == 'cost':
                        if com[2].split(":")[1].isdigit():
                            r_db.ch_game_info(name, int(com[2].split(":")[1]))
                            return com_mist_arg(com, '', 1)
                        return 'Error!\nThe price of the game is a ' \
                               'positive integer.\n' \
                               'Use only numbers.'
                    elif what == 'name':
                        if len(com[2].split(":")[1]) > 0:
                            r_db.ch_game_info(name, -1, '', com[2].split(":")[1])
                            return com_mist_arg(com, '', 1)
                        return com_mist_arg(com[0] + ' ' + com[1], com[2])
                    return com_mist_arg(com[0] + ' ' + com[1], com[2])
                return com_mist_arg(com[0] + ' ' + com[1] + com[2])
            return 'Error!\nThere is no such game in the database.'
        return com_mist_arg(com[0] + ' ' + com[1])
    return com_mist_arg(com[0], com[1])


def ban(com):
    if len(com) != 3:
        return com_mist_arg(" ".join(com))
    elif len(com[1].split(':')) > 1:
        if com[2] in ['true', 't', 'false', 'f']:
            user_id = int(com[1].split(':')[1])
            if (not db.check_id_bd(user_id)) and (not r_db.check_root_id(user_id)):
                if com[2] in ['t', 'true']:
                    db.update_info(user_id, 'banned', 1)
                    r_db.set_ban_time(user_id)
                else:
                    db.update_info(user_id, 'banned', 0)
                return com_mist_arg(com, '', 1)
            else:
                return 'that "user id" is not defined'
        else:
            return com_mist_arg(com[0] + ' ' + com[1], com[2])
    return com_mist_arg(com[0])


def navi_root(com):
    com = com.replace(' ', '').split('-')
    if com[0] in ['h', 'help']:
        return help(com)
    elif com[0] in ['u', 'users']:
        return users(com)
    elif com[0] in ['d', 'del', 'delete']:
        return delete(com)
    elif com[0] in ['s', 'stat']:
        return stat(com)
    elif com[0] in ['g', 'game']:
        return game(com)
    elif com[0] in ['b', 'ban']:
        return ban(com)
    else:
        return 'no such command'


def mode_on():
    return 'root mode is on'


def mode_off():
    return 'root mode turned off'
