import os
import time
import database_common

dir_path = os.path.dirname(os.path.realpath(__file__))


@database_common.connection_handler
def get_answer(cursor, question_id):
    query = """ SELECT * FROM answer WHERE question_id = (%(question_id)s) ORDER BY vote_number DESC"""
    answer = {'question_id': question_id}
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
    query = """ INSERT INTO answer(submission_time, vote_number, question_id, message, image, accept_answer, user_id) 
    VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s,%(accept_answer)s, %(user_id)s )"""
    new_answers = {'submission_time': sub_time, 'vote_number': new_answer['vote_number'],
                   'question_id': new_answer['question_id'], 'message': new_answer['message'],
                   'image': new_answer['image'], 'accept_answer': False, 'user_id': new_answer['user_id']}
    cursor.execute(query, new_answers)


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """DELETE FROM answer WHERE id= %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def edit_answer(cursor, message, question_id):
    query = f""" 
                UPDATE answer
                SET message = '{message}'
                WHERE id = {question_id}   
                RETURNING question_id         
                """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def vote_on_answer(cursor, answer_id, vote):
    query = """
        UPDATE answer
        SET vote_number = vote_number + %(vote)s
        WHERE id = %(answer_id)s
            """
    return cursor.execute(query, {"answer_id": answer_id, 'vote': vote})


@database_common.connection_handler
def update_status_accept_answer(cursor, answer_id, value):
    query = """
        UPDATE answer
        SET accept_answer = %(value)s
        WHERE id = %(answer_id)s
        """
    return cursor.execute(query, {"answer_id": answer_id, 'value': value})
