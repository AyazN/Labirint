# Фазульзянов Амир
# 29.12 - добавлены основные функции для базы данных и создание самой базы данных

import sqlite3

NAME_DB = 'data_base/labirint_db.db'
LOG = 'log'
MAPS = 'maps'
ACCOUNTS = 'accounts'
ID = 'id'
ACCOUNT = 'account'
PLAYER_X = 'player_x'
PLAYER_Y = 'player_y'
ENEMY_X = 'enemy_x'
ENEMY_Y = 'enemy_y'
MAP = 'map'
LOGIN = 'login'
PASSWORD = 'password'

con = sqlite3.connect(NAME_DB)
cur = con.cursor()


def add_new_save(account_id, player_x, player_y, enemy_x, enemy_y, file_name):
    map = select_map_id(file_name)
    query = f"""INSERT INTO {LOG}({ACCOUNT}, {PLAYER_X}, {PLAYER_Y}, {ENEMY_X}, {ENEMY_Y}, {MAP})
    VALUES ({account_id}, {player_x}, {player_y}, {enemy_x}, {enemy_y}, {map})"""
    cur.execute(query)
    con.commit()


def select_map_id(file_name):
    query = f"""SELECT {ID} FROM {MAPS}
                WHERE {MAP} = {file_name}"""
    return cur.execute(query).fetchone()[0]


def select_map_name(account_id):
    query = f"""SELECT {MAP} FROM {MAPS}
                    WHERE {ID} = {account_id}"""
    return cur.execute(query).fetchone()[0]


def update_save(account_id, player_x, player_y, enemy_x, enemy_y, file_name):
    map = select_map_id(file_name)
    query = f"""UPDATE {LOG} 
                SET {PLAYER_X} = {player_x}, {PLAYER_Y} = {player_y}, {ENEMY_X} = {enemy_x}, {ENEMY_Y} = {enemy_y}
                WHERE {ACCOUNT} = {account_id} AND {MAP} = {map}"""
    cur.execute(query)
    con.commit()


def is_save_in_db(account_id, file_name):
    map = select_map_id(file_name)
    query = f"""SELECT * FROM {LOG} WHERE {ACCOUNT} = {account_id} AND {MAP} = {map}"""
    if cur.execute(query).fetchone():
        return True
    return False


def select_save(account_id):
    query = f"""SELECT * FROM {LOG} WHERE {ACCOUNT} = {account_id}"""
    return cur.execute(query).fetchall()  # список кортежей


def add_file_name(file_name):
    query = f"INSERT INTO {MAPS}({MAP}) VALUES ({file_name})"
    cur.execute(query)
    con.commit()


def add_account(login, password):
    query = f"INSERT INTO {ACCOUNTS}({LOGIN}, {PASSWORD}) VALUES ({login, password})"
    cur.execute(query)
    con.commit()


def select_account_id(login, password):
    query = f"""SELECT {ID} FROM {ACCOUNTS}
                    WHERE {LOGIN} = {login} AND {PASSWORD} = {password}"""
    return cur.execute(query).fetchone()[0]


def is_account_in_db(login, password):
    query = f"""SELECT {ID} FROM {ACCOUNTS}
                        WHERE {LOGIN} = {login} AND {PASSWORD} = {password}"""
    if cur.execute(query).fetchone():
        return True
    return False
