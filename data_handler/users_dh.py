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
    query = """ SELECT users.login,num_of_asked_questions, num_of_answers,num_of_comments,reputation
     FROM user_details
     INNER JOIN users on users.id = user_details.user_id"""
    cursor.execute(query)
    return cursor.fetchall()
