import csv
from datetime import datetime
# import operator


DATA_FILE_QUESTIONS = "/home/flori/data/Documents/projects-web/ask-mate-1-python-apetreibogdan/sample_data/question.csv"
DATA_FILE_ANSWERS = "/home/flori/data/Documents/projects-web/ask-mate-1-python-apetreibogdan/sample_data/answer.csv"
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions(filename):
    with open(DATA_FILE_QUESTIONS, newline='') as csv_file:
        list_dict = []
        reader = csv.DictReader(csv_file)

        for row in reader:
            list_dict.append(row)
        return list_dict


def get_data_header(filename):
    with open(DATA_FILE_QUESTIONS, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
        return headers


def get_time_submission(filename):
    list_of_questions = get_all_questions(DATA_FILE_QUESTIONS)

    submission_time = [int(submission['submission_time']) for submission in list_of_questions]

    return submission_time


def transform_time(list_time):
    list_of_dates = []

    for item in list_time:
        item = datetime.utcfromtimestamp(item)
        item = item.strftime("%d-%m-%Y %H:%M:%S")
        list_of_dates.append(item)
    return list_of_dates


def get_answers(filename, qs_id):
    with open(DATA_FILE_ANSWERS, newline='') as csv_file:
        list_answers = []
        reader = csv.DictReader(csv_file)

        for row in reader:
            if int(row['question_id']) == qs_id:
                list_answers.append(row['message'])

        return list_answers


def add_new_question(filename, output):
    with open(DATA_FILE_QUESTIONS, "a", newline='') as csv_file:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(output)


def add_new_answer(filename, output):
    with open(DATA_FILE_ANSWERS, "a", newline='') as csv_file:
        fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(output)


def get_all_answers(filename):
    with open(DATA_FILE_ANSWERS, newline='') as csv_file:
        list_answers = []
        reader = csv.DictReader(csv_file)

        for row in reader:
            list_answers.append(row)
        return list_answers


def delete_question(filename, question_id):
    updated_list = []
    with open(DATA_FILE_QUESTIONS, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['id']) != question_id:
                updated_list.append(row)

    question_ids = get_ids_questions(DATA_FILE_QUESTIONS)
    [data.update({'id': question_ids[index]}) for index, data in enumerate(updated_list)]

    with open(DATA_FILE_QUESTIONS, "w") as csv_file:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in updated_list:
            writer.writerow(item)


def get_ids_questions(filename):
    list_of_questions = get_all_questions(DATA_FILE_QUESTIONS)
    question_id = [int(qs_id['id']) for qs_id in list_of_questions]
    return question_id


def get_ids_answers(filename):
    list_of_answers = get_all_answers(DATA_FILE_ANSWERS)
    answer_id = [int(ans_id['id']) for ans_id in list_of_answers]
    return answer_id


def edit_question(output):
    questions = get_all_questions(DATA_FILE_QUESTIONS)
    for item in questions:
        if int(item['id']) == int(output['id']):
            item.update(output)

    with open(DATA_FILE_QUESTIONS, "w") as csv_file:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in questions:
            writer.writerow(item)


def delete_answers_question(filename, question_id):
    updated_answers = []
    with open(DATA_FILE_ANSWERS, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if int(row['question_id']) != question_id:
                updated_answers.append(row)

    answers_ids = get_ids_answers(DATA_FILE_ANSWERS)

    [data.update({'id': answers_ids[index]}) for index, data in enumerate(updated_answers)]  

    with open(DATA_FILE_ANSWERS, "w") as csv_file:
        fieldnames = DATA_HEADER_ANSWERS
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in updated_answers:
            writer.writerow(item)


def delete_answer(filename, answer_id):
    updated_answers = []

    with open(DATA_FILE_ANSWERS, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['id']) != answer_id:
                updated_answers.append(row)

    answers_ids = get_ids_answers(DATA_FILE_ANSWERS)
    [data.update({'id': answers_ids[index]}) for index, data in enumerate(updated_answers)]

    with open(DATA_FILE_ANSWERS, "w") as csv_file:
        fieldnames = DATA_HEADER_ANSWERS
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in updated_answers:
            writer.writerow(item)


def vote_up_down(filename, question_id, action):
    questions = get_all_questions(DATA_FILE_QUESTIONS)
    if action == "up":
        for item in questions:
            if int(item['id']) == question_id:
                item['vote_number'] = str(int(item['vote_number']) + 1)
    elif action == "down":
        for item in questions:
            if int(item['id']) == question_id:
                item['vote_number'] = str(int(item['vote_number']) - 1)

    with open(DATA_FILE_QUESTIONS, "w") as csv_file:
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in questions:
            writer.writerow(item)


def vote_up_down_answer(filename, answer_id, action):
    list_of_answers = get_all_answers(DATA_FILE_ANSWERS)
    if action == "up":
        for item in list_of_answers:
            if int(item['id']) == answer_id:
                item['vote_number'] = str(int(item['vote_number']) + 1)
    elif action == "down":
        for item in list_of_answers:
            if int(item['id']) == answer_id:
                item['vote_number'] = str(int(item['vote_number']) - 1)

    with open(DATA_FILE_ANSWERS, "w") as csv_file:
        fieldnames = DATA_HEADER_ANSWERS
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in list_of_answers:
            writer.writerow(item)
