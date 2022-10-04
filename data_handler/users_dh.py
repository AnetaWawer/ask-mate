import os
import shutil
import time
from tempfile import NamedTemporaryFile
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_common

dir_path = os.path.dirname(os.path.realpath(__file__))

@database_common.connection_handler
def get_all_users(cursor):
    query = """ SELECT users.login,num_of_asked_questions, num_of_answers,num_of_comments,reputation, user_details.user_id
     FROM user_details
     INNER JOIN users on users.id = user_details.user_id"""
    cursor.execute(query)
    return cursor.fetchall()



@database_common.connection_handler
def get_user_name(cursor, user_id):
    query="""SELECT users.login FROM users WHERE id = %(user_id)s """
    user_id={'user_id':user_id}
    cursor.execute(query,user_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_user_details(cursor, user_id):
    query = """SELECT user_details.user_id, users.login, users.submission_time, 
    user_details.num_of_asked_questions, user_details.num_of_answers, user_details.num_of_comments, user_details.reputation
    FROM user_details INNER JOIN users ON users.id = user_details.user_id WHERE users.id = %(user_id)s 
    """
    user_id= {'user_id': user_id}
    cursor.execute(query,user_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_question_by_user_id(cursor, user_id):
    query = """SELECT question.id, question.title FROM question WHERE user_id = %(user_id)s"""
    user_id={'user_id':user_id}
    cursor.execute(query,user_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_answer_by_user_id(cursor, user_id):
    query = """SELECT answer.question_id, answer.message FROM answer WHERE user_id = %(user_id)s"""
    user_id={'user_id':user_id}
    cursor.execute(query,user_id)
    return cursor.fetchall()

@database_common.connection_handler
def get_comment_by_user_id(cursor, user_id):
    query = """SELECT comment.question_id, comment.answer_id, comment.message FROM comment WHERE user_id = %(user_id)s"""
    user_id={'user_id':user_id}
    cursor.execute(query,user_id)
    return cursor.fetchall()

@database_common.connection_handler
def update_number_of_user_questions(cursor, user_id):
    query = """UPDATE user_details 
    SET num_of_asked_questions = (SELECT COUNT(*) FROM question WHERE question.user_id = user_details.user_id) """
    user_id={'user_id':user_id}
    cursor.execute(query,user_id)

@database_common.connection_handler
def update_number_of_user_answers(cursor, user_id):
    query = """UPDATE user_details 
    SET num_of_answers = (SELECT COUNT(*) FROM answer WHERE answer.user_id = user_details.user_id) """
    user_id={'user_id':user_id}
    cursor.execute(query,user_id)

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
def reputation_for_questions_up(cursor, user_id ):
    query="""UPDATE user_details SET reputation = reputation + 5 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})


@database_common.connection_handler
def reputation_for_questions_down(cursor, user_id ):
    query="""UPDATE user_details SET reputation = reputation -2 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})

@database_common.connection_handler
def reputation_for_answers_up(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation + 10 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})

@database_common.connection_handler
def reputation_for_answers_down(cursor, user_id):
    query = """UPDATE user_details SET reputation = reputation - 2 WHERE user_id= %(user_id)s"""
    cursor.execute(query, {"user_id": user_id})

@database_common.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    query ="""SELECT user_id FROM question WHERE id= %(question_id)s"""
    cursor.execute(query, {'question_id':question_id})
    return cursor.fetchall()

@database_common.connection_handler
def get_user_id_by_answer_id(cursor, answer_id):
    query ="""SELECT user_id FROM answer WHERE id= %(answer_id)s"""
    cursor.execute(query, {'answer_id':answer_id})
    return cursor.fetchall()