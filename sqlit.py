import sqlite3

def reg_user(id,status,x=0):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        status_active,
        finish_stat
        ) """)
    db.commit()

    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?,?)", (id, status,0))
        db.commit()


def info_members(): # Количество челов, запустивших бота
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a


def obnova_members_status(id,status):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    proverka = sql.execute(f"SELECT status_active FROM user_time WHERE id ='{id}'").fetchone() # Проверка предыдущего статуса
    if proverka[0] == 0: #Если у человека ранее не регистрировался статус
        sql.execute(f"UPDATE user_time SET status_active = {status} WHERE id = {id}")
        db.commit()

def send_status_no_rassilka(id):
    try:
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute(f"UPDATE user_time SET status_active = 9 WHERE id = {id}")
        db.commit()
    except:
        print('Произошла неудача / сообщенние из sql')
        pass


def finish_bot(id):
    try:
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute(f"UPDATE user_time SET finish_stat = 1 WHERE id = {id}")
        db.commit()
    except:
        print('Произошла неудача номер 2 / сообщенние из sql')
        pass



def count_member_in_status(status): #Возвращает количество пользователей со статутсом {status}
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    count = sql.execute(f'SELECT COUNT(*) FROM user_time WHERE status_active = {status}').fetchone()[0]
    return count

def cheack_status(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    proverka = sql.execute(f"SELECT status_active FROM user_time WHERE id ='{id}'").fetchone()  # Проверка предыдущего статуса
    return proverka

def cheack_finish(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    proverka = sql.execute(f"SELECT finish_stat FROM user_time WHERE id = '{id}'").fetchone()  # Проверка закончил ли бота или нет
    print(f'Sql {proverka} проверка')
    return proverka
