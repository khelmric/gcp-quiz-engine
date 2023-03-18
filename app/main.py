import secrets
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__)

# vars
main_categories = []
sub_categories = []
groups = []
questions = []

# Use the application default credentials.
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

db_ref = db.collection(u'quiz-db')

@app.route('/', methods = ['GET', 'POST'])

@app.route('/index', methods = ['GET', 'POST'])
def index():
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
    cookies = request.cookies
    # get cookies for the main category
    selected_main_category_id = ""
    selected_main_category_name = ""
    main_category_visibility = "show_main_categories"
    selected_sub_category_id = ""
    selected_sub_category_name = ""
    sub_category_visibility = "hide_sub_categories"
    selected_group_id = ""
    selected_group_name = ""
    group_visibility = "hide_groups"    

    return render_template('index.html', 
        main_categories=main_categories,
        header_path=header_path
        )

@app.route('/home', methods = ['GET', 'POST'])
def home():
    # clear variables
    main_categories.clear()
    sub_categories.clear()
    groups.clear()
    # redirect to index  
    res = make_response(redirect('/'))
    # delete all cookies
    res.set_cookie('selected_main_category_id', '', expires=0)
    res.set_cookie('selected_main_category_name', '', expires=0)
    res.set_cookie('selected_sub_category_id', '', expires=0)
    res.set_cookie('selected_sub_category_name', '', expires=0)
    res.set_cookie('selected_group_id', '', expires=0)
    res.set_cookie('selected_group_name', '', expires=0)
    return res

@app.route('/main_category', methods = ['GET', 'POST'])
def main_category():
    # get cookies
    cookies = request.cookies
    # get form output    
    selected_main_category_id = request.form['selected_main_category_id']
    selected_main_category_name = request.form['selected_main_category_name']
    header_path=selected_main_category_name
    # query sub categories
    firestore_sub_categories = db_ref.where('type', '==', 'sub-category')
    firestore_sub_categories = firestore_sub_categories.where('main_category_id', '==', selected_main_category_id)
    for sub_category in firestore_sub_categories.stream():
        sub_categories.append((sub_category.to_dict()))    
    # render main_category    
    res = make_response(render_template('main_category.html', 
        main_categories=main_categories,
        selected_main_category_id=selected_main_category_id,
        sub_categories=sub_categories,
        header_path=header_path
        ))
    # delete cookies
    res.set_cookie('selected_sub_category_id', '', expires=0)
    res.set_cookie('selected_sub_category_name', '', expires=0)
    res.set_cookie('selected_group_id', '', expires=0)
    res.set_cookie('selected_group_name', '', expires=0)    
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
    # get cookies
    cookies = request.cookies
    selected_main_category_name = cookies.get("selected_main_category_name")
    # get form output    
    selected_sub_category_id = request.form['selected_sub_category_id']
    selected_sub_category_name = request.form['selected_sub_category_name']
    header_path=selected_main_category_name + "  ►  " + selected_sub_category_name
    # query groups
    firestore_groups = db_ref.where('type', '==', 'group')
    firestore_groups = firestore_groups.where('sub_category_id', '==', selected_sub_category_id)
    for group in firestore_groups.stream():
        groups.append((group.to_dict()))    
    # render sub_category    
    res = make_response(render_template('sub_category.html', 
        selected_sub_category_id=selected_sub_category_id,
        groups=groups,
        header_path=header_path
        ))
    # delete cookies
    res.set_cookie('selected_group_id', '', expires=0)
    res.set_cookie('selected_group_name', '', expires=0)    
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
    # get cookies
    cookies = request.cookies
    selected_main_category_name = cookies.get("selected_main_category_name")
    selected_sub_category_name = cookies.get("selected_sub_category_name")
    # get form output    
    selected_group_id = request.form['selected_group_id']
    selected_group_name = request.form['selected_group_name']
    header_path=selected_main_category_name + "  ►  " + selected_sub_category_name + "  ►  " + selected_group_name
    # query questions
    firestore_questions = db_ref.where('type', '==', 'question')
    firestore_questions = firestore_questions.where('group_id', '==', selected_group_id)
    question_count = 0
    for question in firestore_questions.stream():
        questions.append((question.to_dict()))
        question_count = question_count + 1
        print(question_count)
    # render group    
    res = make_response(render_template('group.html', 
        questions=questions,
        selected_main_category_name=selected_main_category_name,
        selected_sub_category_name=selected_sub_category_name,
        selected_group_name=selected_group_name,
        question_count=question_count,
        header_path=header_path
        )) 
    # set sub category cookies
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
    return res

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
