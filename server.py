from flask import Flask, render_template, request, redirect, url_for, session

from data_handler import question_dh as qdh
from data_handler import comment_and_tags_dh as cdh
from data_handler import answer_dh as adh

app = Flask(__name__)


@app.route("/")
def to_list():
    return redirect('/list')


@app.route('/list', methods=["GET", "POST"])
def list():
    sort_value = request.form.get("sort_value")
    sort_direction = request.form.get("sort_direction")
    if sort_value == None:
        sort_value = "id"
        sort_direction = """ASC"""
    question_list = qdh.get_question(sort_value, sort_direction)
    # question_list = dh.get_five_most_recent_questions()
    return render_template("list.html", question_list=question_list)


@app.route('/list', methods=["GET"])
def list_answers():
    answer_list = adh.get_answer()
    return render_template("list.html", answer_list=answer_list)


@app.route('/question/<question_id>')
def question(question_id):
    questions = qdh.get_question_by_id(question_id)
    answer = adh.get_answer(question_id)
    comments_for_questions = cdh.get_comments_to_question(question_id)
    comments_for_answer = cdh.get_comments_to_answer()
    tags = cdh.get_tag_to_question_id(question_id)
    login = session['login']
    user_id = qdh.get_user_id_by_login(login)
    user_id_in_question = qdh.get_user_id_in_questions_by_users_id(user_id['id'])
    if user_id['id'] == user_id_in_question['user_id']:
        possibility_acceptance = True
    else:
        possibility_acceptance = False
    return render_template("question.html", question_id=question_id, question=questions, answer=answer,
                           comments_for_questions=comments_for_questions, comments_for_answer=comments_for_answer,
                           tags=tags, possibility_acceptance=possibility_acceptance)


@app.route('/add_question', methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        image = request.files.get("filename")
        filename = qdh.add_file(image)
        question_id = qdh.add_new_question(title, message, filename)
        return redirect(url_for("question", question_id=question_id['id']))
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer')
def add_answer_form(question_id):
    return render_template('answer.html', question_id=question_id)


@app.route('/post_an_answer/<question_id>/new-answer', methods=['POST'])
def post_an_answer(question_id):
    answer = {'vote_number': 0, 'question_id': question_id, 'message': request.form.get('message'), 'image': None}
    adh.add_answer(answer)
    return redirect(url_for("question", question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        answer = adh.get_answer_by_answer_id(answer_id)
        return render_template('edit-answer.html', answer=answer)
    if request.method == 'POST':
        message = request.form.get('message')
        question_id = adh.edit_answer(message, answer_id)
        return redirect(url_for('question', question_id=question_id['question_id']))


@app.route('/question/<question_id>/edit')
def edit_question_form(question_id):
    question = qdh.get_question_by_id(question_id)
    return render_template("edit-question.html", question=question)


@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    title = request.form.get('title')
    message = request.form.get('message')
    qdh.edit_question(title, message, question_id)
    shift = "/question/" + str(question_id)
    return redirect(shift)
    return redirect(url_for("edit-question.html", question_id=question_id))


@app.route('/add_question', methods=["GET"])
def add_question_form():
    return render_template("add-question.html")


@app.route('/question/<question_id>/delete')
def delete_questions(question_id):
    qdh.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer = adh.get_answer_by_answer_id(answer_id)
    cdh.delete_comment_to_answer(answer_id)
    adh.delete_answer(answer_id)
    return redirect(url_for("question", question_id=answer['question_id']))


@app.route('/question/<question_id>/vote_up')
def vote_on_question_up(question_id):
    vote = 1
    qdh.vote_on_question(question_id, vote)
    return redirect("/list")


@app.route('/question/<question_id>/vote_down')
def vote_on_question_down(question_id):
    vote = -1
    qdh.vote_on_question(question_id, vote)
    return redirect("/list")


# @app.route('/list', methods=['POST'])
# def sort_question():
#     order_by = request.form.get("sort_value")
#     order_direction = request.form.get("sort_method")
#     dh.sort_data(order_by, order_direction)
#     return redirect("/list")

@app.route('/answer/<answer_id>/vote_up')
def vote_on_answer_up(answer_id):
    vote = 1
    adh.vote_on_answer(answer_id, vote)
    question = qdh.get_question_id_by_answer_id(answer_id)
    return redirect(url_for("question", question_id=question['question_id']))


@app.route('/answer/<answer_id>/vote_down')
def vote_on_answer_down(answer_id):
    vote = -1
    adh.vote_on_answer(answer_id, vote)
    question_id = qdh.get_question_id_by_answer_id(answer_id)
    return redirect(url_for("question", question_id=question_id['question_id']))


@app.route('/question/<question_id>/new-comment')
def add_comment_to_question_form(question_id):
    return render_template('comment-to-question.html', question_id=question_id)


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def post_new_comment_to_question(question_id):
    comment = {'question_id': question_id, 'answer_id': None, 'message': request.form.get('message'), 'edited_count': 0}
    cdh.add_comments(comment)
    return redirect(url_for("question", question_id=question_id))


@app.route('/answer/<answer_id>/new-comment')
def add_comment_to_answer_form(answer_id):
    return render_template('comment-to-answer.html', answer_id=answer_id)


@app.route('/answer/<answer_id>/new-comment', methods=['POST'])
def post_new_comment_to_answer(answer_id):
    answer = adh.get_answer_by_answer_id(answer_id)
    comment = {'question_id': None, 'answer_id': answer_id, 'message': request.form.get('message'), 'edited_count': 0}
    cdh.add_comments(comment)
    return redirect(url_for("question", question_id=answer['question_id']))


@app.route('/comment/<comment_id>/edit')
def edit_comment_form(comment_id):
    comment = cdh.get_comment_by_comment_id(comment_id)
    return render_template('edit-comment.html', comment=comment)


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
    tags = cdh.get_all_tags()
    return render_template("tags.html", tags=tags, question_id=question_id)


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
    search_question = qdh.search_question(search)
    return render_template("search.html", search_question=search_question)


@app.route('/question/<question_id>/<tag_id>/delete_tag')
def delete_tag(question_id, tag_id):
    cdh.delete_tag_from_tag(tag_id)
    return redirect(url_for('question', question_id=question_id))


@app.route('/answer/<answer_id>', methods=['POST'])
def change_status_answer(answer_id):
    new_status = request.form.get('status')
    adh.update_status_accept_answer(answer_id, new_status)
    question_id = qdh.get_question_id_by_answer_id(answer_id)
    return redirect(url_for("question", question_id=question_id['question_id']))

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=9000,
        debug=True)
