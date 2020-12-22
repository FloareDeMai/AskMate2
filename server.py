from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file 

import data_handeler
from datetime import datetime
import operator
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/images'


@app.route("/")
@app.route("/list")
def list_questions():
    args = dict(request.args)
    # print(args)

    questions = data_handeler.get_all_questions("sample_data/questions.csv")
    data_header = data_handeler.get_data_header("sample_data/questions.csv")
    data_time = data_handeler.get_time_submission("sample_data/questions.csv")
    time_data = data_handeler.transform_time(data_time)
    [data.update({'submission_time': time_data[index]}) for index, data in enumerate(questions)]
    questions = sorted(questions, key=operator.itemgetter('submission_time'), reverse=True)

    if 'title' and 'asc' in args.values():
        questions = sorted(questions, key=operator.itemgetter('title'))
    elif 'title' and 'desc' in args.values():
        questions = sorted(questions, key=operator.itemgetter('title'), reverse=True)
    elif 'message' and 'asc' in args.values():
        questions = sorted(questions, key=operator.itemgetter('message'))
    elif 'message' and 'desc' in args.values():
        questions = sorted(questions, key=operator.itemgetter('message'), reverse=True)
    # elif 'view_number' and 'asc' in args.values():
    #     questions = sorted(questions, key=operator.itemgetter('view_number'), reverse=True)
    # elif 'view_number' and 'desc' in args.values():
    #     questions = sorted(questions, key=operator.itemgetter('view_number'))
    # elif 'vote_number' and 'asc' in args.values():
    #     questions = sorted(questions, key=operator.itemgetter('vote_number'))
    # elif 'vote_number' and 'desc' in args.values():
    #     questions = sorted(questions, key=operator.itemgetter('vote_number'), reverse=True)

    return render_template("list_questions.html", questions=questions, data_header=data_header, time_data=time_data)


@app.route("/question/static/images/<img_path>", methods=['GET'])
def get_img(img_path):
    if request.method == "GET":
        all_answers = data_handeler.get_all_answers("sample_data/answer.csv")

        for filename in all_answers:
            if img_path in filename['image']:
                file = filename['image']

        return send_file(file, mimetype='image/png')


@app.route("/question/<int:question_id>/delete", methods=['GET', 'POST'])
@app.route("/question/<int:question_id>", methods=['GET', 'POST'])
def show_question(question_id):

    if request.method == "GET":
        questions = data_handeler.get_all_questions('sample_data/questions.csv')
        # answers = data_handeler.get_answers('sample_data/answer.csv', question_id)
        all_answers = data_handeler.get_all_answers("sample_data/answer.csv")
        story = questions[question_id - 1]
        answers2 = [answer for answer in all_answers if int(answer["question_id"]) == question_id]
        return render_template("show_question.html", story=story, answers2=answers2)

    if request.method == "POST":
        questions = data_handeler.get_all_questions('sample_data/questions.csv')
        # answers = data_handeler.get_answers('sample_data/answer.csv', question_id)
        data_handeler.delete_question("sample_data/question.csv", question_id)
        data_handeler.delete_answers_question("sample_data/answer.csv", question_id)
        return redirect(url_for('list_questions'))


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    questions = data_handeler.get_all_questions("sample_data/questions.csv")
    if request.method == "POST":
        new_question = dict(request.form)

        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        file_path = app.config['UPLOAD_PATH'] + "/" + filename

        new_question = dict((k.lower(), v.capitalize()) for k, v in new_question.items())
        now = datetime.now()
        timestampp = int(datetime.timestamp(now))
        timestampp = timestampp + 7200
        story_id = len(questions) + 1
        new_question['id'] = new_question.get(id, str(story_id))
        new_question['submission_time'] = new_question.get('submission_time', str(timestampp))
        new_question['view_number'] = new_question.get('view_number', str(0))
        new_question['vote_number'] = new_question.get('vote_number', str(0))
        new_question['image'] = new_question.get('image', file_path)
        data_handeler.add_new_question("sample_data/questions.csv", new_question)
        return redirect(url_for('show_question', question_id=len(questions) + 1))
    return render_template("add_question.html")


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def post_new_answer(question_id):
    all_answers = data_handeler.get_all_answers("sample_data/answer.csv")
    if request.method == "POST":
        new_answer = dict(request.form)

        uploaded_file = request.files['file']
        print(uploaded_file)
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        file_path = app.config['UPLOAD_PATH'] + "/" + filename
        print(file_path)

        now = datetime.now()
        timestampp = int(datetime.timestamp(now))
        timestampp = timestampp + 7200
        answer_id = len(all_answers) + 1
        new_answer['id'] = new_answer.get(id, str(answer_id))
        new_answer['submission_time'] = new_answer.get('submission_time', str(timestampp))
        new_answer['vote_number'] = new_answer.get('vote_number', str(0))
        new_answer['question_id'] = new_answer.get('question_id', question_id)
        new_answer['image'] = new_answer.get('image', file_path)
        data_handeler.add_new_answer("sample_data/answer.csv", new_answer)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template("add_new_answer.html", question_id=question_id)


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "POST":
        questions = data_handeler.get_all_questions("sample_data/questions.csv")
        question = questions[question_id - 1]
        id = int(question['id'])
        updated_question = dict(request.form)
        updated_question = dict((k.lower(), v.capitalize()) for k, v in updated_question.items())
        updated_question['id'] = updated_question.get(id, str(id))
        data_handeler.edit_question(updated_question)
        print(updated_question)
        return redirect(url_for('show_question', question_id=question_id))
    else:
        questions = data_handeler.get_all_questions("sample_data/questions.csv")
        question = questions[question_id - 1]
        id = int(question['id'])
        updated_question = dict(request.form)
        updated_question['id'] = updated_question.get(id, str(id))

        return render_template("edit-question.html", question=question)


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    all_answers = data_handeler.get_all_answers("sample_data/answer.csv")

    for row in all_answers:
        if int(row['id']) == answer_id:
            question_id = int(row['question_id'])

    data_handeler.delete_answer("sample_data/answer.csv", answer_id)

    question_url = url_for('show_question', question_id=question_id)

    return redirect(question_url)


@app.route("/question/<int:question_id>/vote_up")
def vote_up(question_id):
    data_handeler.vote_up_down("sample_data/questions.csv", question_id, "up")
    return redirect('/list')


@app.route("/question/<int:question_id>/vote_down")
def vote_down(question_id):
    data_handeler.vote_up_down("sample_data/questions.csv", question_id, "down")
    return redirect("/list")


@app.route("/answer/<int:answer_id>/vote_up")
def vote_up_answer(answer_id):
    all_answers = data_handeler.get_all_answers("sample_data/answer.csv")
    for row in all_answers:
        if int(row['id']) == answer_id:
            question_id = int(row['question_id'])

    data_handeler.vote_up_down_answer("sample_data/answer.csv", answer_id, "up")

    question_url = url_for('show_question', question_id=question_id)

    return redirect(question_url)


@app.route("/answer/<int:answer_id>/vote_down")
def vote_down_answer(answer_id):
    all_answers = data_handeler.get_all_answers("sample_data/answer.csv")
    for row in all_answers:
        if int(row['id']) == answer_id:
            question_id = int(row['question_id'])

    data_handeler.vote_up_down_answer("sample_data/answer.csv", answer_id, "down")

    question_url = url_for('show_question', question_id=question_id)

    return redirect(question_url)


if __name__ == "__main__":
    app.run(debug=True)

