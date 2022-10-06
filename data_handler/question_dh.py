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
def get_five_most_recent_questions(cursor, sort_value, sort_direction):
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY {sort_value} {sort_direction}
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, sort_value, sort_direction):
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY {sort_value} {sort_direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_question(cursor, title, message, image, user_id):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"""
                INSERT INTO question 
                VALUES (DEFAULT, '{submission_time}', 0, 0, '{title}', '{message}', '{image}', '{user_id}' )   
                RETURNING id;    
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image, user_id
        FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query= """  DELETE FROM comment WHERE question_id= %(question_id)s;
                DELETE FROM comment WHERE question_id IS NULL;
                DELETE FROM answer WHERE question_id= %(question_id)s;
                DELETE FROM question_tag WHERE question_id= %(question_id)s;
                DELETE FROM question WHERE id= %(question_id)s"""
    cursor.execute(query, {"question_id": question_id})


@database_common.connection_handler
def edit_question(cursor, title, message, question_id):
    query = f""" 
                UPDATE question 
                SET title = '{title}',
                    message = '{message}'
                WHERE id = {question_id}

                """
    return cursor.execute(query)


@database_common.connection_handler
def vote_on_question(cursor, question_id, vote):
    query = """
        UPDATE question
        SET vote_number = vote_number + %(vote)s
        WHERE id = %(question_id)s
            """
    return cursor.execute(query, {"question_id": question_id, 'vote': vote})


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def search_question(cursor, search):
    query = """
    SELECT *
    FROM question
    WHERE UPPER(message) LIKE UPPER(%(search)s) OR UPPER(title) LIKE UPPER(%(search)s) """
    cursor.execute(query, {'search': '%' + search + '%'})
    return cursor.fetchall()


def add_file(fileitem):
    try:
        filename = os.path.basename(fileitem.filename)
        file_name = os.path.join(dir_path[:-12], "static", "images", filename)
        open(file_name, 'wb').write(fileitem.read())
    except:
        filename='BLANK_ICON.png'
    return filename


@database_common.connection_handler
def increase_number_of_views(cursor, question_id):
    query = """
        UPDATE question
        SET view_number = view_number+ 1
        WHERE id = %(question_id)s
            """
    cursor.execute(query, {"question_id": question_id})



