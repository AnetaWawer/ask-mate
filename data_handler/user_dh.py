import database_common
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


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
    FROM user_details INNER JOIN users ON users.id = user_details.user_id
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





