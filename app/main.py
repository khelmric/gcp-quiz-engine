import random
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__)

# init vars
main_categories = []
sub_categories = []
groups = []
questions = []
header_path = ""
edit_mode = False

# use the application default credentials to access Cloud Firestore
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

# init quiz-db
db = firestore.client()
db_ref = db.collection(u'quiz-db')

@app.route('/', methods = ['GET', 'POST'])

@app.route('/index', methods = ['GET', 'POST'])
def index():
    # get global vars
    global edit_mode
    # clear variables
    main_categories.clear()
    sub_categories.clear()
    groups.clear()
    questions.clear()
    header_path=""

    # query main categories
    firestore_main_categories = db_ref.where('type', '==', 'main-category')
    for main_category in firestore_main_categories.stream():
        main_categories.append((main_category.to_dict()))
    # get cookies
#    cookies = request.cookies
    # get cookies for the main category
#    selected_main_category_id = ""
#    selected_main_category_name = ""
#    selected_sub_category_id = ""
#    selected_sub_category_name = ""
#    selected_group_id = ""
#    selected_group_name = ""  

    # render index  
    res = make_response(render_template('index.html', 
        main_categories=main_categories,
        header_path=header_path,
        edit_mode=edit_mode
        ))
    # delete all cookies
    res.set_cookie('selected_main_category_id', '', expires=0)
    res.set_cookie('selected_main_category_name', '', expires=0)
    res.set_cookie('selected_sub_category_id', '', expires=0)
    res.set_cookie('selected_sub_category_name', '', expires=0)
    res.set_cookie('selected_group_id', '', expires=0)
    res.set_cookie('selected_group_name', '', expires=0)
    res.set_cookie('question_counter', '', expires=0)  
    res.set_cookie('action', '', expires=0)

    return res

@app.route('/editmode', methods = ['GET', 'POST'])
def editmode():
    global edit_mode
    if edit_mode == True:
        edit_mode = False
    else:
        edit_mode = True
    res = make_response(redirect('/'))  
    #res = make_response(render_template('index.html', 
    #    main_categories=main_categories,
    #    header_path=header_path,
    #    edit_mode=edit_mode
    #    ))     
    return res

@app.route('/main_category', methods = ['GET', 'POST'])
def main_category():
    # get global vars
    global edit_mode
    # get cookies
    cookies = request.cookies
    if request.method == 'GET':
        selected_main_category_id = cookies.get("selected_main_category_id")
        selected_main_category_name = cookies.get("selected_main_category_name")
    # get form output    
    if request.method == 'POST': 
        selected_main_category_id = request.form['selected_main_category_id']
        selected_main_category_name = request.form['selected_main_category_name']
    # check if required vars are there, otherwise back to previous page 
    if selected_main_category_name == None or selected_main_category_id == None:
        res = make_response(redirect('/home'))
    else: 
        header_path=selected_main_category_name
        # query sub categories
        sub_categories.clear()
        firestore_sub_categories = db_ref.where('type', '==', 'sub-category')
        firestore_sub_categories = firestore_sub_categories.where('main_category_id', '==', selected_main_category_id)
        for sub_category in firestore_sub_categories.stream():
            sub_categories.append((sub_category.to_dict()))    
        # render main_category    
        res = make_response(render_template('main_category.html', 
            main_categories=main_categories,
            selected_main_category_id=selected_main_category_id,
            sub_categories=sub_categories,
            header_path=header_path,
            edit_mode=edit_mode
            ))
        # delete cookies
        res.set_cookie('selected_sub_category_id', '', expires=0)
        res.set_cookie('selected_sub_category_name', '', expires=0)
        res.set_cookie('selected_group_id', '', expires=0)
        res.set_cookie('selected_group_name', '', expires=0)
        res.set_cookie('question_counter', '', expires=0)
        res.set_cookie('action', '', expires=0)     
        # set main category cookies
        res.set_cookie(
        'selected_main_category_id',
        value = selected_main_category_id,
        #secure = True
        )
        res.set_cookie(
        'selected_main_category_name',
        value = selected_main_category_name,
        #secure = True
        )      
    return res

@app.route('/sub_category', methods = ['GET', 'POST'])
def sub_category():
    # get global vars
    global edit_mode
    # get cookies
    cookies = request.cookies
    selected_main_category_name = cookies.get("selected_main_category_name")
    selected_main_category_id = cookies.get("selected_main_category_id")
    if request.method == 'GET':
        selected_sub_category_id = cookies.get("selected_sub_category_id")
        selected_sub_category_name = cookies.get("selected_sub_category_name")
    # get form output    
    if request.method == 'POST':    
        selected_sub_category_id = request.form['selected_sub_category_id']
        selected_sub_category_name = request.form['selected_sub_category_name']
    # check if required vars are there, otherwise back to previous page    
    if selected_main_category_name == None or selected_main_category_id == None or selected_sub_category_name == None or selected_sub_category_id == None:
        res = make_response(redirect('/main_category'))
    else:      
        header_path=selected_main_category_name + "  ►  " + selected_sub_category_name
        # query groups
        firestore_groups = db_ref.where('type', '==', 'group')
        firestore_groups = firestore_groups.where('sub_category_id', '==', selected_sub_category_id)
        groups.clear()
        for group in firestore_groups.stream():
            groups.append((group.to_dict()))    
        # render sub_category    
        res = make_response(render_template('sub_category.html', 
            selected_sub_category_id=selected_sub_category_id,
            groups=groups,
            header_path=header_path,
            edit_mode=edit_mode
            ))
        # delete cookies
        res.set_cookie('selected_group_id', '', expires=0)
        res.set_cookie('selected_group_name', '', expires=0)
        res.set_cookie('question_counter', '', expires=0)
        res.set_cookie('action', '', expires=0) 
        # set sub category cookies
        res.set_cookie(
        'selected_sub_category_id',
        value = selected_sub_category_id,
        #secure = True
        )
        res.set_cookie(
        'selected_sub_category_name',
        value = selected_sub_category_name,
        #secure = True
        )      
    return res

@app.route('/group', methods = ['GET', 'POST'])
def group():
    # get global vars
    global edit_mode
    # get cookies
    cookies = request.cookies
    selected_main_category_name = cookies.get("selected_main_category_name")
    selected_main_category_id = cookies.get("selected_main_category_id")
    selected_sub_category_name = cookies.get("selected_sub_category_name")
    selected_sub_category_id = cookies.get("selected_sub_category_id")
    if request.method == 'GET':
        selected_group_name = cookies.get("selected_group_name")
        selected_group_id = cookies.get("selected_group_id")
    # get form output
    if request.method == 'POST':    
        selected_group_id = request.form['selected_group_id']
        selected_group_name = request.form['selected_group_name']
    # check if required vars are there, otherwise back to previous page
    if selected_main_category_name == None or selected_main_category_id == None or selected_sub_category_name == None or selected_sub_category_id == None or selected_group_name == None or selected_group_id == None:
        res = make_response(redirect('/sub_category'))
    else:
        global header_path
        header_path=selected_main_category_name + "  ►  " + selected_sub_category_name + "  ►  " + selected_group_name
        # query questions
        firestore_questions = db_ref.where('type', '==', 'question')
        firestore_questions = firestore_questions.where('group_id', '==', selected_group_id)
        global question_count
        question_count = 0
        questions.clear()
        for question in firestore_questions.stream():
            questions.append(question.to_dict())
            #print(json.dumps(question.to_dict(), indent = 4))
            #print(question.to_dict())
            question_count = question_count + 1
        # shuffle question list
        random.shuffle(questions)    
        # render group    
        res = make_response(render_template('group.html', 
            questions=questions,
            selected_main_category_name=selected_main_category_name,
            selected_sub_category_name=selected_sub_category_name,
            selected_group_name=selected_group_name,
            selected_group_id=selected_group_id,
            question_count=question_count,
            header_path=header_path,
            edit_mode=edit_mode
            )) 
        # delete cookies
        res.set_cookie('question_counter', '', expires=0)
        res.set_cookie('action', '', expires=0)    
        # set group category cookies
        res.set_cookie(
            'selected_group_id',
            value = selected_group_id,
            #secure = True
        )
        res.set_cookie(
            'selected_group_name',
            value = selected_group_name,
            #secure = True
        )
        res.set_cookie(
            'question_counter',
            value = "0",
            #secure = True
        )
    return res

@app.route('/question', methods = ['GET', 'POST'])
def question():
    # get global vars
    global edit_mode
    global answers_order
    global selected_answers
    global result
    global results
    global question_count
    global submit_button_text
    global quiz_status_bar
    global result_correct_answers_percentage
    global question_correct_answers
    global answer_type
    # get cookies
    cookies = request.cookies
    question_counter = int(cookies.get("question_counter"))
    action = cookies.get("action")
    # get form inputs
    if request.method == 'POST':
        # next question or show results
        if action == 'next':
            action = 'result'
            # increase question counter by 1 
            question_counter = int(question_counter)+1
            # create list for answer indexes
            if question_counter < int(question_count):
                answers_order = list(range(0, len(questions[question_counter].get('answers'))))
                # shuffle question list
                random.shuffle(answers_order)
            # reset values
            selected_answers = []
            result = 'None'
            submit_button_text = 'Submit'
        elif action == 'result':
            action = 'next'
            # question counter will not be incresed
            question_counter = int(question_counter)
            # get selected answer
            selected_answers = []
            for answ in request.form.getlist("selected_answer"):
                selected_answers.append(int(answ))
            #result = questions[question_counter].get('answers')[int(selected_answer)]['correct']
            if sorted(selected_answers) == sorted(question_correct_answers):
                result = True
                quiz_status_bar = quiz_status_bar + '&#9989;'
            else:
                result = False
                quiz_status_bar = quiz_status_bar + '&#10060;'
            results.append(result)
            result_correct_answers = len([item for item in results if item == True])
            result_correct_answers_percentage = str(int(round(result_correct_answers / question_count * 100, 0))) + "%"
            # Submit button text to Next
            submit_button_text = 'Next'
        else:
            action = 'result'
            # question counter will not be incresed (first run, action = None)
            question_counter = int(question_counter)
            # create list for answer indexes
            answers_order = list(range(0, len(questions[question_counter].get('answers'))))
            # shuffle question list
            random.shuffle(answers_order)
            # reset values for the initial run
            selected_answers = [ -1 ]
            result = 'None'
            submit_button_text = 'Submit'
            quiz_status_bar = ''
            results = []
        if action == 'result' and question_counter < int(question_count):
            # get current questions correct answers
            question_correct_answers = []
            for index, question_correct_answer in enumerate(questions[question_counter].get('answers')):
                if question_correct_answer['correct'] == True:
                    question_correct_answers.append(index)
            if len(question_correct_answers) > 1:
                answer_type = "checkbox"
            else:
                answer_type = "radio"    
    # check if there are questions left
    if question_counter < int(question_count):
        # create temp list for answer character ids
        answers_char = [chr(value) for value in range(64, len(questions[question_counter].get('answers'))+65)]
        # render question  
        res = make_response(render_template('question.html',
            question_text = questions[question_counter].get('question'),
            question_counter = str(int(question_counter)+1),
            question_count = question_count,
            solution_comment = questions[question_counter].get('solution_comment'),
            answers_char = answers_char,
            answers_order = answers_order,
            selected_answers = selected_answers,
            answers = questions[question_counter].get('answers'),
            answer_type = answer_type,
            action = action,
            result = result,
            submit_button_text = submit_button_text,
            quiz_status_bar = quiz_status_bar,
            header_path = header_path,
            edit_mode=edit_mode
            )) 
        # set cookies    
        res.set_cookie(
                'question_counter',
                value = str(question_counter),
                #secure = True
            )
        res.set_cookie(
                'action',
                value = action,
                #secure = True
            )        
    else:
        res = make_response(redirect('/result'))      
    return res
    
@app.route('/result', methods = ['GET', 'POST'])
def result():
    # get global vars
    global edit_mode
    if request.method == 'POST':
        res = make_response(redirect('/group'))
    else:    
        res = make_response(render_template('result.html',
                correct_answers_percentage = result_correct_answers_percentage,
                edit_mode=edit_mode
            ))
    return res

@app.route('/data_maintenance', methods = ['GET', 'POST'])
def data_maintenance():
    # global vars
    global selected_answers
    # set lists
    selected_answers_answer = []
    selected_answers_comment = []
    selected_answers_correct = []
    # get form data
    if request.method == 'POST':
        selected_type = request.form['selected_type']
        selected_id = request.form['selected_id']
        action = request.form['action']
        try:
            selected_name = request.form['selected_name']
        except:
            selected_name = ""    
        try:
            selected_parent_id = request.form['selected_parent_id']
        except:
            selected_parent_id = ""    
        try:
            prev_action = request.form['prev_action']
        except:
            prev_action = ""
        try:
            selected_question = request.form['selected_question']
        except:
            selected_question = ""
        try:
            selected_documentation = request.form['selected_documentation']
        except:
            selected_documentation = ""
        try:
            selected_solution_comment = request.form['selected_solution_comment']
        except:
            selected_solution_comment = ""        
        # get answers
        try:
            for answ in request.form.getlist("selected_answer_answer"):
                selected_answers_answer.append(answ)
        except:
            selected_answers_answer = []
        try:    
            for answ in request.form.getlist("selected_answer_comment"):
                selected_answers_comment.append(answ)
        except:
            selected_answers_comment = []
        selected_answers_checkboxes = [ "selected_answer_correct0", "selected_answer_correct1", "selected_answer_correct2", "selected_answer_correct3", "selected_answer_correct4", "selected_answer_correct5", "selected_answer_correct6", "selected_answer_correct7"]
        for checkbox_name in selected_answers_checkboxes:
            try:
                answ = request.form.get(checkbox_name)
                if answ == 'on':
                    selected_answers_correct.append(True)
                else:
                    selected_answers_correct.append(False)
            except:
                selected_answers_correct.append(False)
        if selected_answers_answer:   
            selected_answers.clear()
        #print(len(selected_answers_answer))
        #print(len(selected_answers_comment))
        #print(len(selected_answers_correct))
        for idx, ans in enumerate(selected_answers_answer):
            selected_answers.append({ 'comment': selected_answers_comment[idx], 'answer': ans, 'correct': selected_answers_correct[idx] })    
        #    selected_answers = []
    # check if variables exist, handle exceptions
    try: action
    except NameError: action = None
    try: prev_action
    except NameError: prev_action = None
    try: selected_id
    except NameError: selected_id = None
    try: selected_type
    except NameError: selected_type = None
    try: selected_name
    except NameError: selected_name = None
    try: selected_parent_id
    except NameError: selected_parent_id = None
    try: selected_question
    except NameError: selected_question = None
    try: selected_answers
    except NameError: selected_answers = []
    # check if required vars are there, otherwise back to previous page 
    if action == None:
        res = make_response(redirect('/index'))
    elif action == 'edit':
        # get answers if selected type is question
        if selected_type == 'question':
            firestore_documents = db_ref.where('type', '==', selected_type).where('id', '==', selected_id)
            selected_answers = []
            for selected_document in firestore_documents.stream():
                #doc_ref = db_ref.document(selected_document.id)
                #questions.append(question.to_dict())
                #print(json.dumps(selected_document.to_dict(), indent = 4))
                #print(selected_document.to_dict()['answers'])
                #print(selected_document.to_dict().get('answers'))
                #selected_answers.append(selected_document.to_dict()['answers'])
                #selected_answers.append(selected_document.to_dict().get('answers'))
                selected_answers = selected_document.to_dict().get('answers')
        res = make_response(render_template('data_maintenance.html',
                selected_type = selected_type,
                selected_id = selected_id,
                selected_name = selected_name,
                selected_parent_id = selected_parent_id,
                selected_question = selected_question,
                selected_answers = selected_answers,
                prev_action = action,
                button_text = 'Update',
                edit_mode=edit_mode))
    elif action == 'add':
        if selected_type == 'main-category':
            ts_id = 'm' + str(time.time())
        elif selected_type == 'sub-category':
            ts_id = 's' + str(time.time())
        elif selected_type == 'group':
            ts_id = 'g' + str(time.time()) 
        elif selected_type == 'question':
            ts_id = 'q' + str(time.time())
        elif selected_type == 'document':
            ts_id = 'd' + str(time.time())
        else:
            ts_id = 'o' + str(time.time()) 
        res = make_response(render_template('data_maintenance.html',
                selected_type = selected_type,
                selected_id = ts_id,
                selected_name = selected_name,
                selected_parent_id = selected_parent_id,
                selected_question = selected_question,
                prev_action = action,
                button_text = 'Add',
                edit_mode=edit_mode))                
    elif action == 'delete':
        firestore_documents = db_ref.where('type', '==', selected_type).where('id', '==', selected_id)
        for selected_document in firestore_documents.stream():
            doc_ref = db_ref.document(selected_document.id)
            doc_ref.delete()
    elif action == 'apply':
        if prev_action == 'edit':
            firestore_documents = db_ref.where('type', '==', selected_type).where('id', '==', selected_id)
            for selected_document in firestore_documents.stream():
                doc_ref = db_ref.document(selected_document.id)
            if selected_type != 'question':
                doc_ref.update({u'name': selected_name})
            else:
                if selected_type == 'question':
                    data = {
                            u'id': selected_id,
                            u'group_id': selected_parent_id,
                            u'question': selected_question,
                            u'type': selected_type,
                            u'documentation': selected_documentation,
                            u'solution_comment': selected_solution_comment,
                            u'answers': []
                    }
                    #print(selected_answers)
                    for answer in selected_answers:
                        #print(answer["correct"])
                        #data['answers'].append('{ "comment": "' + answer["comment"] + '", "answer": "' + answer["answer"] + '", "correct": ', answer["correct"], '}')
                        if answer["answer"]:
                            data['answers'].append({ 'comment': answer["comment"], 'answer': answer["answer"], 'correct': answer["correct"] })
                        #data['answers'].append({ '"comment": "' + answer["comment"] + '", "answer": "' + answer["answer"] + '", "correct": ', answer["correct"] })
                    print(json.dumps(data, indent = 4))
                    doc_ref.set(data)
        elif prev_action == 'add':
            if selected_type == 'main-category':
                data = {
                        u'id': selected_id,
                        u'name': selected_name,
                        u'type': selected_type    
                }
            if selected_type == 'sub-category':
                data = {
                        u'id': selected_id,
                        u'main_category_id': selected_parent_id,
                        u'name': selected_name,
                        u'type': selected_type    
                }
            if selected_type == 'group':
                data = {
                        u'id': selected_id,
                        u'sub_category_id': selected_parent_id,
                        u'name': selected_name,
                        u'type': selected_type    
                }
            if selected_type == 'question':
                data = {
                        u'id': selected_id,
                        u'group_id': selected_parent_id,
                        u'question': selected_question,
                        u'type': selected_type,
                        u'documentation': selected_documentation,
                        u'solution_comment': selected_solution_comment,
                        u'answers': []
                }
                for answer in selected_answers:
                    if answer["answer"]:
                        data['answers'].append({ 'comment': answer["comment"], 'answer': answer["answer"], 'correct': answer["correct"] })
            #print(data)    
            db_ref.add(data)
    if action != 'edit' and action != 'add':
        if selected_type == 'main-category':
            res = make_response(redirect('/index'))
        elif selected_type == 'sub-category':
            res = make_response(redirect('/main_category'))
        elif selected_type == 'group':
            res = make_response(redirect('/sub_category'))  
        elif selected_type == 'question':
            res = make_response(redirect('/group'))           
    return res

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
