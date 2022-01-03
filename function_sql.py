import sqlite3
from settings import *

con = sqlite3.connect(NAME_DB)
cur = con.cursor()


def add_new_save(account_id, player_x, player_y, enemy_x, enemy_y, file_name):  # добавление нового сохранения
    query = f"""INSERT INTO {LOG}({ACCOUNT}, {PLAYER_X}, {PLAYER_Y}, {ENEMY_X}, {ENEMY_Y}, {MAP})
    VALUES ({account_id}, {player_x}, {player_y}, {enemy_x}, {enemy_y}, {file_name})"""
    cur.execute(query)
    con.commit()


def select_map_id(file_name):  # получение id карты
    num = int(cur.execute(f"""SELECT {ID} FROM {MAPS}
                WHERE {MAP} = '{file_name}'""").fetchone()[0])
    return num


def select_map_name(account_id):  # получение названия карты
    if is_save_in_db(account_id):
        result = cur.execute(f"""SELECT {MAP} FROM {LOG}
                            WHERE {ACCOUNT} = {account_id}""").fetchall()[-1][0]
        query = f"""SELECT {MAP} FROM {MAPS}
                            WHERE {ID} = {result}"""
        return cur.execute(query).fetchone()[0]


def update_save(account_id, player_x, player_y, enemy_x, enemy_y, file_name):  # изменение сохранения
    map = select_map_id(file_name)
    query = f"""UPDATE {LOG} 
                SET {PLAYER_X} = {player_x}, {PLAYER_Y} = {player_y}, {ENEMY_X} = {enemy_x}, {ENEMY_Y} = {enemy_y}
                WHERE {ACCOUNT} = {account_id} AND {MAP} = {map}"""
    cur.execute(query)
    con.commit()


def is_save_in_db(account_id):  # проверка - в бд есть такое сохранение?
    if cur.execute(f"""SELECT * FROM {LOG} WHERE {ACCOUNT} = {account_id}""").fetchall():
        return True
    return False


def select_save(account_id):  # получение всех сохранений аккаунта
    query = f"""SELECT * FROM {LOG} WHERE {ACCOUNT} = {account_id}"""
    return cur.execute(query).fetchall()  # список кортежей


def add_file_name(file_name):  # добавление карты
    query = f"INSERT INTO {MAPS}({MAP}) VALUES ('{file_name}')"
    cur.execute(query)
    con.commit()


def add_account(login, password):  # добавление аккаунта
    query = f"INSERT INTO {ACCOUNTS}({LOGIN}, {PASSWORD}) VALUES ({login, password})"
    cur.execute(query)
    con.commit()


def select_account_id(login, password):  # получение id аккаунта
    return cur.execute(f"""SELECT {ID} FROM {ACCOUNTS}
                    WHERE {LOGIN} = '{login}' AND {PASSWORD} = '{password}'""").fetchone()[0]


def is_account_in_db(login, password):  # в бд есть такой аккаунт?
    if cur.execute(f"""SELECT {ID} FROM {ACCOUNTS}
                        WHERE {LOGIN} = '{login}' AND {PASSWORD} = '{password}'""").fetchone():
        return True
    return False


def open_map():
    data = open('data/map.txt', encoding='utf-8').read()
    file = " ".join(data.split('\n'))
    return str(file)


def reconstruct_map(acc_id):
    if select_map_name(acc_id):
        with open('data/map.txt', "a") as file:
            file.truncate(0)
            for message in select_map_name(acc_id).split():
                file.write(message)
                file.write('\n')
        return True
    else:
        return False
