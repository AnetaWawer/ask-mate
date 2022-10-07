import os
import database_common
from flask import session
import bcrypt
import time

dir_path = os.path.dirname(os.path.realpath(__file__))


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
def add_user_details(cursor, new_user):
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


@database_common.connection_handler
def get_login_and_password(cursor):
    query = """SELECT login, password FROM users"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_users(cursor):
    query = """ SELECT users.login,num_of_asked_questions, num_of_answers,num_of_comments,reputation, user_details.user_id
     FROM user_details
     INNER JOIN users on users.id = user_details.user_id"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_name(cursor, user_id):
    query = """SELECT users.login FROM users WHERE id = %(user_id)s """
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_details(cursor, user_id):
    query = """SELECT user_details.user_id, users.login, users.submission_time, 
    user_details.num_of_asked_questions, user_details.num_of_answers, user_details.num_of_comments, user_details.reputation
    FROM user_details INNER JOIN users ON users.id = user_details.user_id WHERE users.id = %(user_id)s 
    """
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_user_id(cursor, user_id):
    query = """SELECT question.id, question.title FROM question WHERE user_id = %(user_id)s"""
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_user_id(cursor, user_id):
    query = """SELECT answer.question_id, answer.message FROM answer WHERE user_id = %(user_id)s"""
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_user_id(cursor, user_id):
    query = """SELECT comment.question_id, comment.answer_id, comment.message FROM comment WHERE user_id = %(user_id)s"""
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)
    return cursor.fetchall()


@database_common.connection_handler
def update_number_of_user_questions(cursor, user_id):
    query = """UPDATE user_details 
    SET num_of_asked_questions = (SELECT COUNT(*) FROM question WHERE question.user_id = user_details.user_id) """
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)


@database_common.connection_handler
def update_number_of_user_answers(cursor, user_id):
    query = """UPDATE user_details 
    SET num_of_answers = (SELECT COUNT(*) FROM answer WHERE answer.user_id = user_details.user_id) """
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)


@database_common.connection_handler
def update_number_of_user_comments(cursor, user_id):
    query = """UPDATE user_details
    SET num_of_comments = (SELECT COUNT(*) FROM comment WHERE comment.user_id = user_details.user_id) """
    user_id = {'user_id': user_id}
    cursor.execute(query, user_id)


@database_common.connection_handler
def get_user_id(cursor):
    query = """SELECT user_id FROM user_details"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id_in_questions(cursor, id):
    query = f"""
    SELECT user_id
    FROM question
    WHERE id= %(question_id)s
    """
    cursor.execute(query, {'question_id': id})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_by_login(cursor, login):
    query = """
    SELECT id 
    FROM users
    WHERE login = %(login)s
    """
    cursor.execute(query, {"login": login})
    return cursor.fetchone()


@database_common.connection_handler
def reputation_for_questions_up(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation + 5 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})


@database_common.connection_handler
def reputation_for_questions_down(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation -2 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})


@database_common.connection_handler
def reputation_for_answers_up(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation + 10 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})


@database_common.connection_handler
def reputation_for_accepted_answer_up(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation + 15 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})


@database_common.connection_handler
def reputation_for_answers_down(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation - 2 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})


@database_common.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    query = """SELECT user_id FROM question WHERE id= %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_by_answer_id(cursor, answer_id):
    query = """SELECT user_id FROM answer WHERE id= %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


def is_user_logged_in_message():
    if session.get('is_logged_in'):
        message = 'Logged in as: ' + session['user_login']
    else:
        message = 'Not logged in.'
    return message


def user_id():
    if session.get('is_logged_in'):
        user = get_user_id_by_login(session['user_login'])
        user_id = user['id']
        return user_id
    else:
        pass
