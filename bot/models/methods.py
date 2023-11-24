import sqlite3 as sq
from aiogram import types


async def db_start():
    global conn, cur
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    if conn:
        print('Database connect OK')
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY, username TEXT, date_enter DATETIME, request_count INTEGER)""")
    conn.commit()


async def sql_add_user(message):
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    try:
        user_id = message.chat.id
        username = message.chat.username
        date_enter = message.date
        request_count = 30
        # Проверка наличия пользователя
        cur.execute('SELECT * FROM users WHERE user_id == ?', (user_id,))
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO users VALUES (?,?,?,?)', (user_id, username, date_enter, request_count))
            conn.commit()
            print('Новый пользователь добавлен в базу')
        # else:
        #     print("Значение user_id уже существует в таблице.")

    except sq.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()


async def sql_group_add_user(message):
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        date_enter = message.date
        request_count = 30
        # Проверка наличия пользователя
        cur.execute('SELECT * FROM users WHERE user_id == ?', (user_id,))
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO users VALUES (?,?,?,?)', (user_id, username, date_enter, request_count))
            conn.commit()
            print('Новый пользователь добавлен в базу')
        # else:
        #     print("Значение user_id уже существует в таблице.")

    except sq.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()


async def remove_user_from_database(user_id: int):
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    try:
        query = "DELETE FROM users WHERE user_id = ?"
        cur.execute(query, (user_id,))
        conn.commit()
        print('Пользователь удален из базы')
    except sq.Error as error:
        print("Error:", error)
    finally:
        if conn:
            print("База данных закрыта")
            conn.close()


async def minus_request_count(message):
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    try:
        user_id = message.chat.id
        cur.execute("""UPDATE users SET request_count = request_count - 1 WHERE user_id = ?""", (user_id,))
        conn.commit()
    except sq.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()


async def check_user_request_count(message: types.Message):
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    try:
        user_id = message.from_user.id
        request_count_tuple = cur.execute("SELECT request_count FROM users WHERE user_id = ?", (user_id,)).fetchone()
        request_count = request_count_tuple[0]
        return request_count
    except sq.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()


async def get_users():
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    try:
        count_users = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        all_users = cur.execute("SELECT * FROM users").fetchall()
        return (count_users, all_users)
    except sq.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()






