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
def add_logged_users(cursor, email, password):
    sub_time = time.strftime("%Y-%m-%d %H:%M")
    query = f"""
      INSERT INTO users (password, login, submission_time)
      VALUES  ('{password}','{email}', '{sub_time}') """
    return cursor.execute(query)


@database_common.connection_handler
def add_user_details(cursor,new_user):
    query = """ INSERT INTO user_details(user_id, num_of_asked_questions, num_of_answers, num_of_comments, reputation) 
    VALUES (%(user_id)s,%(num_of_asked_questions)s,%(num_of_answers)s,%(num_of_comments)s,%(reputation)s)"""
    new_users = {'user_id': new_user['user_id'], 'num_of_asked_questions': new_user['num_of_asked_questions'],
                   'num_of_answers': new_user['num_of_answers'], 'num_of_comments': new_user['num_of_comments'],
                   'reputation': new_user['reputation'], }
    cursor.execute(query, new_users)

def check_email(emails, logins):
    for email in emails:
        if email['login'] == logins:
            return False
    return True


@database_common.connection_handler
def get_emails(cursor):
    query = """
        SELECT login FROM users """
    cursor.execute(query)
    return cursor.fetchall()
