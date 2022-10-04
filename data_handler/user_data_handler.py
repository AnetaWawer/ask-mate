import bcrypt
import time

import database_common



def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def add_logged_users(cursor, mail, password):
    sub_time = time.strftime("%Y-%m-%d %H:%M")
    query = f"""  
      INSERT INTO users (password, login, submission_time)
      VALUES  ('{password}','{mail}', '{sub_time}') """
    cursor.execute(query)


@database_common.connection_handler
def check_mail(logins):
    mails = get_mails()
    for mail in mails:
        if mail['login'] == logins:
            return False
    return True


@database_common.connection_handler
def get_mails(cursor):
    query = """ 
        SELECT * FROM users """
    cursor.execute(query)
    return cursor.fetchall()