import time
import tkinter
from tkinter import *
import sqlite3
import random
con = sqlite3.connect(r'/SQL/labirint_db.db')
cur = con.cursor()
def register():
    global register_screen
    global username
    global password
    global username_entry
    global password_entry
    register_screen = Toplevel(main_screen)
    register_screen.title("Регистрация")
    register_screen.geometry("500x300")
    username = StringVar()
    password = StringVar()
    Label(register_screen, text="Придумайте логин и пароль").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Логин")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Пароль")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Регистрация", width=10, height=1, bg="white", command=register_user).pack()


def login():
    global login_screen
    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry
    username_verify = StringVar()
    password_verify = StringVar()
    login_screen = Toplevel(main_screen)

    login_screen.title("Логин")
    login_screen.geometry("300x250")
    Label(login_screen, text="Придумайте логин и пароль").pack()
    Label(login_screen, text="").pack()

    Label(login_screen, text="Логин").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Пароль").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Логин", width=10, height=1, command=login_verify).pack()
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    check_username = '''SELECT login from accounts'''
    check_pass = '''SELECT password from accounts'''
    cur.execute(check_username)
    records = cur.fetchall()
    cur.execute(check_pass)
    records_1 = cur.fetchall()
    prov_user = []
    prov_pass = []
    for row in records:
        prov_user.append(str(row[0]))
    for row_1 in records_1:
        prov_pass.append(str(row_1[0]))
    if username1 in prov_user:
        if password1 in prov_pass:
            login_sucess()
        else:
            password_not_recognised()
    else:
        user_not_found()
def register_user():
    prov_user = []
    check_username = '''SELECT login from accounts'''
    cur.execute(check_username)
    records = cur.fetchall()
    for row in records:
        prov_user.append(str(row[0]))
    username_info = username.get()
    password_info = password.get()
    if (len(password_info) == 0 or len(username_info) == 0):
        Label(register_screen, text='Пустая строчка', fg='red', font=('calibri', 11)).pack()
    elif username_info in prov_user:
        Label(register_screen, text='Пользователь с таким логином уже существует', fg='red', font=('calibri', 11)).pack()
    else:
        random_id = random.randint(1000, 9999)
        sqlite_insert = '''INSERT INTO accounts
                        (id, login, password)
                        VALUES (?, ?, ?);'''
        data_tuple = (random_id, username_info, password_info)
        cur.execute(sqlite_insert, data_tuple)
        con.commit()

        username_entry.delete(0, END)
        password_entry.delete(0, END)
        Label(register_screen, text="Регистрация прошла успешна", fg="green", font=("calibri", 11)).pack()


def check_empty_window():
    global empty_check
    empty_check = Toplevel(login_screen)
    empty_check.title("Успешно")
    empty_check.geometry("1500x100")
    Label(empty_check, text="Логин и пароль сошелся").pack()
    Button(empty_check, text="OK", command=delete_check).pack()
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Успешно")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Логин и пароль сошелся").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()


def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Успешно")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Неправильный пароль").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Успешно")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="Не найден").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

def delete_login_success():
    login_success_screen.destroy()
def delete_check():
    empty_check.destroy()
def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("500x200")
    main_screen.title("Логин аккаунта")
    Label(text="Выбрать", bg="black", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Логин", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Регистрация", height="2", width="30", command=register).pack()

    main_screen.mainloop()
main_account_screen()
