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
def get_five_most_recent_questions(cursor):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY submission_time DESC
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
def add_new_question(cursor, title, message, image):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"""
                INSERT INTO question 
                VALUES (DEFAULT, '{submission_time}', 0, 0, '{title}', '{message}', '{image}' )   
                RETURNING id;    
            """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()



@database_common.connection_handler
def get_answer(cursor, question_id):
    query = """ SELECT * FROM answer WHERE question_id = (%(question_id)s) ORDER BY vote_number DESC"""
    answer = {'question_id':question_id}
    cursor.execute(query, answer)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id = %(answer_id)s
        """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def add_answer(cursor, new_answer):
    sub_time = time.strftime("%Y-%m-%d %H:%M")
    query= """ INSERT INTO answer(submission_time, vote_number, question_id, message, image) 
    VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s )"""
    new_answers = {'submission_time': sub_time, 'vote_number':new_answer['vote_number'],
                   'question_id': new_answer['question_id'], 'message':new_answer['message'], 'image':new_answer['image']}
    cursor.execute(query, new_answers)





@database_common.connection_handler
def delete_question(cursor, question_id):
    query= """  DELETE FROM comment WHERE question_id= %(question_id)s;
                DELETE FROM comment WHERE question_id IS NULL;
                DELETE FROM answer WHERE question_id= %(question_id)s;
                DELETE FROM question_tag WHERE question_id= %(question_id)s;
                DELETE FROM question WHERE id= %(question_id)s"""
    cursor.execute(query, {"question_id": question_id})


@database_common.connection_handler
def delete_answer_p1(cursor, answer_id):
    query = """
        UPDATE answer
        SET submission_time = NULL,
        vote_number = NULL,
        message = '',
        image = NULL
        WHERE id = %(answer_id)s
        """
    return cursor.execute(query, {"answer_id": answer_id})


@database_common.connection_handler
def delete_answer_p2(cursor):
    query="""
    DELETE FROM answer
    WHERE message = ''
        """
    return cursor.execute(query)

@database_common.connection_handler
def edit_answer(cursor,  message, question_id):
    query = f""" 
                UPDATE answer
                SET message = '{message}'
                WHERE id = {question_id}   
                RETURNING question_id         
                """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def edit_question(cursor, title, message, question_id):
    query = f""" 
                UPDATE question 
                SET title = '{title}',
                    message = '{message}'
                WHERE id = {question_id}

                """
    return cursor.execute(query)
     # cursor.fetchone()


@database_common.connection_handler
def delete_comment_to_answer(cursor,answer_id):
    query= """DELETE FROM comment WHERE answer_id= %(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


@database_common.connection_handler
def delete_answer_p1(cursor, answer_id):
    query = """
        UPDATE answer
        SET submission_time = NULL,
        vote_number = NULL,
        message = '',
        image = NULL
        WHERE id = %(answer_id)s
        """
    return cursor.execute(query, {"answer_id": answer_id})


@database_common.connection_handler
def delete_answer_p2(cursor):
    query="""
    DELETE FROM answer
    WHERE message = ''
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
def vote_on_answer(cursor, answer_id, vote):
    query = """
        UPDATE answer
        SET vote_number = vote_number + %(vote)s
        WHERE id = %(answer_id)s
            """
    return cursor.execute(query, {"answer_id": answer_id, 'vote': vote})


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


def add_file(fileitem):
    try:
        filename = os.path.basename(fileitem.filename)
        file_name = os.path.join(dir_path[:-12], 'static', 'images', filename)
        open(file_name, 'wb').write(fileitem.read())
    except IsADirectoryError:
        filename=''
    return filename

@database_common.connection_handler
def get_comments_to_question(cursor, question_id):
    query = """ SELECT * FROM comment WHERE question_id = (%(question_id)s) """
    comment = {'question_id':question_id}
    cursor.execute(query, comment)
    return cursor.fetchall()

@database_common.connection_handler
def add_comments(cursor, new_comment):
    sub_time = time.strftime("%Y-%m-%d %H:%M")
    query= """ INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count) 
    VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s )"""
    new_comments = {'question_id': new_comment['question_id'],'answer_id': new_comment['answer_id'],
                    'message':new_comment['message'], 'submission_time': sub_time, 'edited_count':new_comment['edited_count']}
    cursor.execute(query, new_comments)
@database_common.connection_handler
def get_all_tags(cursor):
    query = """
        SELECT *
        FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def save_new_tag(cursor, new_tag):
    query = f"""
            INSERT INTO tag
            VALUES (DEFAULT, '{new_tag}')
            RETURNING (id)
"""
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_tag_to_question_id(cursor, question_id):
    query = f"""SELECT  *
        FROM tag
        FULL JOIN
        question_tag
        ON      tag.id = question_tag.tag_id
        WHERE   tag.id IS NOT NULL AND question_tag.tag_id IS NOT NULL
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def save_tag_to_question_tag(cursor, question_id, tag_id):
    query = f"""
        INSERT INTO question_tag
        VALUES ('{question_id}', '{tag_id}')
    """

    return cursor.execute(query)


@database_common.connection_handler
def save_existing_tag_to_question(cursor, question_id, tag_id):
    query = f"""
        INSERT INTO question_tag
        VALUES ('{question_id}', '{tag_id}')
    """
    return cursor.execute(query)





@database_common.connection_handler
def get_comments_to_answer(cursor):
    query = """ SELECT comment.message, comment.answer_id, comment.id, comment.edited_count, comment.question_id FROM comment INNER JOIN answer ON comment.answer_id= answer.id """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_comment_id(cursor, comment_id):
    query = """ SELECT message, id FROM comment WHERE id= %(comment_id)s"""
    cursor.execute(query, {'comment_id':comment_id})
    return cursor.fetchall()

@database_common.connection_handler
def delete_comment(cursor, comment_id):
    query = f"""
        DELETE FROM comment
        WHERE id = '{comment_id}'
        """
    return cursor.execute(query)


@database_common.connection_handler
def edit_comment(cursor, message, comment_id):
    query = f""" UPDATE comment SET message = '{message}' WHERE id = {comment_id} """
    cursor.execute(query)

@database_common.connection_handler
def update_edit_counts(cursor, comment_id, count):
    query = """ UPDATE comment SET edited_count = edited_count + %(count)s WHERE id = %(comment_id)s """
    return cursor.execute(query, {'comment_id':comment_id, 'count':count })

@database_common.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    query = """
        SELECT question_id
        FROM comment
        WHERE id = %(comment_id)s AND question_id IS NOT NULL"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()

@database_common.connection_handler
def direct_to_question(cursor):
    query = """ SELECT answer.question_id  FROM answer INNER JOIN comment ON answer.id= comment.answer_id """
    cursor.execute(query)
    return cursor.fetchone()