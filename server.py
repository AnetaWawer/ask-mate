from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2.extras
from data_handler import question_dh as qdh
from data_handler import comment_and_tags_dh as cdh
from data_handler import answer_dh as adh
from data_handler import users_dh

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def main_page():
    users=users_dh.get_user_id()
    for id in users:
        user_id=id['user_id']
        users_dh.update_number_of_user_questions(user_id)
        users_dh.update_number_of_user_answers(user_id)
        users_dh.update_number_of_user_comments(user_id)
    is_logged_in = session.get('is_logged_in')
    sort_value = request.form.get("sort_value")
    sort_direction = request.form.get("sort_direction")
    if sort_value == None:
        question_list = qdh.get_five_most_recent_questions('submission_time', """DESC""")
    else:
        question_list = qdh.get_five_most_recent_questions(sort_value, sort_direction)
    if is_logged_in:
        user_id = users_dh.user_id()
        return render_template('main-page.html', question_list=question_list, is_logged_in=is_logged_in, user_id=user_id, message=users_dh.is_user_logged_in_message())
    return render_template('main-page.html', question_list=question_list, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message())



@app.route('/list', methods=["GET", "POST"])
def list():
    is_logged_in = session.get('is_logged_in')
    sort_value = request.form.get("sort_value")
    sort_direction = request.form.get("sort_direction")
    if sort_value == None:
        sort_value = "id"
        sort_direction = """ASC"""
    question_list = qdh.get_question(sort_value, sort_direction)
    if is_logged_in:
        user_id = users_dh.user_id()
        return render_template('list.html', question_list=question_list, is_logged_in=is_logged_in, user_id=user_id, message=users_dh.is_user_logged_in_message())
    return render_template('list.html', question_list=question_list, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message())


@app.route('/list', methods=["GET"])
def list_answers():
    answer_list = adh.get_answer()
    return render_template("list.html", answer_list=answer_list)


@app.route('/login')
def login():
    return render_template("login.html", message=users_dh.is_user_logged_in_message())

@app.route('/login', methods=['POST'])
def get_login():
    user_login = request.form.get("login")
    user_password = request.form.get("password")
    logins_and_passwords = users_dh.get_login_and_password()
    for element in logins_and_passwords:
        if user_login == format(element['login']):
            if user_password == format(element['password']):
                session["user_login"] = user_login
                session["is_logged_in"] = True
                return redirect(url_for("main_page"))
            else:
                return redirect(url_for("login"))
        else:
            continue
    return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("main_page"))


@app.route('/question/<question_id>')
def question(question_id):
    user_id = users_dh.user_id()
    is_logged_in = session.get('is_logged_in')
    questions = qdh.get_question_by_id(question_id)
    answer = adh.get_answer(question_id)
    comments_for_questions = cdh.get_comments_to_question(question_id)
    comments_for_answer = cdh.get_comments_to_answer()
    tags = cdh.get_tag_to_question_id(question_id)
    user_login = session.get("user_login")
    if user_login:
        users_id = users_dh.get_user_id_by_login(user_login)
        user_id_in_question = users_dh.get_user_id_in_questions(question_id)
        if users_id['id'] == user_id_in_question['user_id']:
            possibility_acceptance = True
        else:
            possibility_acceptance = False
        return render_template("question.html", question_id=question_id, question=questions, answer=answer,
                               comments_for_questions=comments_for_questions, comments_for_answer=comments_for_answer,
                               tags=tags, possibility_acceptance=possibility_acceptance,is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id)
    else:
        return render_template("question.html", question_id=question_id, question=questions, answer=answer,
                               comments_for_questions=comments_for_questions, comments_for_answer=comments_for_answer,
                               tags=tags, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message())


@app.route('/add_question', methods=["POST", "GET"])
def add_question():
    is_logged_in = session.get('is_logged_in')
    if is_logged_in:
        user_id = users_dh.user_id()
        if request.method == "POST":
            title = request.form.get("title")
            message = request.form.get("message")
            image = request.files.get("filename")
            filename = qdh.add_file(image)
            question_id = qdh.add_new_question(title, message, filename,user_id)
            return redirect(url_for("question", question_id=question_id['id']))
        return render_template('add-question.html',is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(),user_id=user_id)
    else:
        return redirect(url_for("main_page", is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message()))



@app.route('/question/<question_id>/new-answer')
def add_answer_form(question_id):
    is_logged_in = session.get('is_logged_in')
    if is_logged_in:
        user_id = users_dh.user_id()
        return render_template('answer.html', question_id=question_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(),user_id=user_id)
    else:
        return redirect(url_for("question", question_id=question_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message()))


@app.route('/post_an_answer/<question_id>/new-answer', methods=['POST'])
def post_an_answer(question_id):
    user = users_dh.get_user_id_by_login(session['user_login'])
    user_id = user['id']
    answer = {'vote_number': 0, 'question_id': question_id, 'message': request.form.get('message'), 'image': None,'user_id': user_id}
    adh.add_answer(answer)
    return redirect(url_for("question", question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    if request.method == 'GET':
        answer = adh.get_answer_by_answer_id(answer_id)
        return render_template('edit-answer.html', answer=answer, is_logged_in=is_logged_in,message=users_dh.is_user_logged_in_message(),user_id=user_id)
    if request.method == 'POST':
        message = request.form.get('message')
        question_id = adh.edit_answer(message, answer_id)
        return redirect(url_for('question', question_id=question_id['question_id'], is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id))


@app.route('/question/<question_id>/edit')
def edit_question_form(question_id):
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    question = qdh.get_question_by_id(question_id)
    return render_template("edit-question.html", question=question, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id)


@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    title = request.form.get('title')
    message = request.form.get('message')
    qdh.edit_question(title, message, question_id)
    shift = "/question/" + str(question_id)
    return redirect(shift)
    # return redirect(url_for("edit-question.html", question_id=question_id))


@app.route('/add_question', methods=["GET"])
def add_question_form():
    return render_template("add-question.html")


@app.route('/question/<question_id>/delete')
def delete_questions(question_id):
    qdh.delete_question(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer = adh.get_answer_by_answer_id(answer_id)
    cdh.delete_comment_to_answer(answer_id)
    adh.delete_answer(answer_id)
    return redirect(url_for("question", question_id=answer['question_id']))


@app.route('/question/<question_id>/vote_up', methods=['POST'])
def vote_on_question_up(question_id):
    vote = 1
    qdh.vote_on_question(question_id, vote)
    user_id = users_dh.get_user_id_by_question_id(question_id)['user_id']
    users_dh.reputation_for_questions_up(user_id)
    return redirect(request.referrer)


@app.route('/question/<question_id>/vote_down', methods=['POST'])
def vote_on_question_down(question_id):
    vote = -1
    qdh.vote_on_question(question_id, vote)
    user_id = users_dh.get_user_id_by_question_id(question_id)['user_id']
    users_dh.reputation_for_questions_down(user_id)
    return redirect(request.referrer)


# @app.route('/list', methods=['POST'])
# def sort_question():
#     order_by = request.form.get("sort_value")
#     order_direction = request.form.get("sort_method")
#     dh.sort_data(order_by, order_direction)
#     return redirect("/list")

@app.route('/answer/<answer_id>/vote_up', methods=['POST'])
def vote_on_answer_up(answer_id):
    vote = 1
    adh.vote_on_answer(answer_id, vote)
    question = qdh.get_question_id_by_answer_id(answer_id)
    user_id = users_dh.get_user_id_by_answer_id(answer_id)['user_id']
    users_dh.reputation_for_answers_up(user_id)
    return redirect(url_for("question", question_id=question['question_id']))


@app.route('/answer/<answer_id>/vote_down', methods=['POST'])
def vote_on_answer_down(answer_id):
    vote = -1
    adh.vote_on_answer(answer_id, vote)
    question_id = qdh.get_question_id_by_answer_id(answer_id)
    user_id = users_dh.get_user_id_by_answer_id(answer_id)['user_id']
    users_dh.reputation_for_answers_down(user_id)
    return redirect(url_for("question", question_id=question_id['question_id']))


@app.route('/question/<question_id>/new-comment')
def add_comment_to_question_form(question_id):
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    if is_logged_in:
        return render_template('comment-to-question.html', question_id=question_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id)
    else:
        return redirect(url_for("question", question_id=question_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id))


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def post_new_comment_to_question(question_id):
    is_logged_in = session.get('is_logged_in')
    user = users_dh.get_user_id_by_login(session['user_login'])
    user_id = user['id']
    comment = {'question_id': question_id, 'answer_id': None, 'message': request.form.get('message'), 'edited_count': 0, 'user_id':user_id}
    cdh.add_comments(comment)
    return redirect(url_for("question", question_id=question_id))


@app.route('/answer/<answer_id>/new-comment')
def add_comment_to_answer_form(answer_id):
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    if is_logged_in:
        return render_template('comment-to-answer.html', answer_id=answer_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(),user_id=user_id)
    else:
        answer = adh.get_answer_by_answer_id(answer_id)
        return redirect(url_for("question", question_id=answer['question_id'], is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id))

@app.route('/answer/<answer_id>/new-comment', methods=['POST'])
def post_new_comment_to_answer(answer_id):
    user = users_dh.get_user_id_by_login(session['user_login'])
    user_id = user['id']
    answer = adh.get_answer_by_answer_id(answer_id)
    comment = {'question_id': None, 'answer_id': answer_id, 'message': request.form.get('message'), 'edited_count': 0, 'user_id':user_id}
    cdh.add_comments(comment)
    return redirect(url_for("question", question_id=answer['question_id']))


@app.route('/comment/<comment_id>/edit')
def edit_comment_form(comment_id):
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    comment = cdh.get_comment_by_comment_id(comment_id)
    return render_template('edit-comment.html', comment=comment, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id )


@app.route('/comment/<comment_id>/edit', methods=['POST'])
def edit_comment(comment_id):
    message = request.form.get('message')
    cdh.edit_comment(message, comment_id)
    count = 1
    cdh.update_edit_counts(comment_id, count)
    question = cdh.get_question_id_by_comment_id(comment_id)
    if question != None:
        return redirect(url_for("question", question_id=question['question_id']))
    else:
        question = cdh.direct_to_question()
        return redirect(url_for("question", question_id=question['question_id']))


@app.route('/question/<question_id>/comments/<comment_id>/delete')
def delete_comment(comment_id, question_id):
    cdh.delete_comment(comment_id)
    return redirect(url_for("question", question_id=question_id))


@app.route('/question/<question_id>/new-tag')
def render_tags(question_id):
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    tags = cdh.get_all_tags()
    return render_template("tags.html", tags=tags, question_id=question_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id)


@app.route('/question/<question_id>/new-tag', methods=['POST'])
def save_new_tag(question_id):
    new_tag = request.form.get('new-tag')
    tag_id = cdh.save_new_tag(new_tag)
    cdh.save_tag_to_question_tag(question_id, tag_id['id'])
    return redirect(url_for('question', question_id=question_id))


@app.route('/question/<question_id>/<tag_id>')
def save_tag_from_existing_tags(question_id, tag_id):
    cdh.save_existing_tag_to_question(question_id, tag_id)
    return redirect(url_for('question', question_id=question_id))


@app.route('/question/<question_id>/view-up')
def increase_views(question_id):
    qdh.increase_number_of_views(question_id)
    return redirect(url_for('question', question_id=question_id))


@app.route('/search')
def search():
    search = request.args.get('search_phrase')
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    search_question = qdh.search_question(search)
    return render_template("search.html", search_question=search_question, message=users_dh.is_user_logged_in_message(), user_id=user_id, is_logged_in=is_logged_in)


@app.route('/question/<question_id>/<tag_id>/delete_tag')
def delete_tag(question_id, tag_id):
    cdh.delete_tag_from_tag(tag_id)
    return redirect(url_for('question', question_id=question_id))


@app.route('/users')
def users():
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    if is_logged_in:
        all_users = users_dh.get_all_users()
        return render_template('users.html', is_logged_in=is_logged_in,all_users=all_users, message=users_dh.is_user_logged_in_message(), user_id=user_id)
    else:
        return redirect(url_for('main_page'))


@app.route('/user/<user_id>')
def user_page(user_id):
    is_logged_in = session.get('is_logged_in')
    user_name = users_dh.get_user_name(user_id)
    user_questions = users_dh.get_question_by_user_id(user_id)
    user_answers = users_dh.get_answer_by_user_id(user_id)
    user_comments = users_dh.get_comment_by_user_id(user_id)
    user_details = users_dh.get_user_details(user_id)
    return render_template('user-page.html', user_details=user_details,user_name=user_name, user_questions=user_questions,
                           user_answers=user_answers, user_comments=user_comments, user_id=user_id, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message())

@app.route('/tag')
def all_tags():
    is_logged_in = session.get('is_logged_in')
    user_id = users_dh.user_id()
    quantity_of_tags = cdh.get_quantity_of_tags()
    return render_template('all-tags.html', quantity_of_tags=quantity_of_tags, is_logged_in=is_logged_in, message=users_dh.is_user_logged_in_message(), user_id=user_id)


@app.route('/answer/<answer_id>', methods=['POST'])
def change_status_answer(answer_id):
    new_status = request.form.get('status')
    adh.update_status_accept_answer(answer_id, new_status)
    question_id = qdh.get_question_id_by_answer_id(answer_id)
    user_id = users_dh.get_user_id_by_answer_id(answer_id)['user_id']
    if new_status == 'True':
        users_dh.reputation_for_accepted_answer_up(user_id)
    return redirect(url_for("question", question_id=question_id['question_id']))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(
        host='0.0.0.0',
        port=9000,
        debug=True)
