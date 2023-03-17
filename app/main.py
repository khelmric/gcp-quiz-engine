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
    header_path=""
    # query main categories
    firestore_main_categories = db_ref.where('type', '==', 'main-category')
    for main_category in firestore_main_categories.stream():
        main_categories.append((main_category.to_dict()))
    # get cookies
    cookies = request.cookies
    # get cookies for the main category
    if cookies.get("selected_main_category_id") == None:
        selected_main_category_id = ""
        selected_main_category_name = ""
        main_category_visibility = "show_main_categories"
        selected_sub_category_id = ""
        selected_sub_category_name = ""
        sub_category_visibility = "hide_sub_categories"
    else:  
        selected_main_category_id = cookies.get("selected_main_category_id")
        selected_main_category_name = cookies.get("selected_main_category_name")
        main_category_visibility = "hide_main_categories"
        header_path=selected_main_category_name
        # query sub categories
        firestore_sub_categories = db_ref.where('type', '==', 'sub-category')
        firestore_sub_categories = firestore_sub_categories.where('main_category_id', '==', selected_main_category_id)
        for sub_category in firestore_sub_categories.stream():
            sub_categories.append((sub_category.to_dict()))
        if cookies.get("selected_sub_category_id") == None:
            selected_sub_category_id = ""
            selected_sub_category_name = ""
            sub_category_visibility = "show_sub_categories"
        else:  
            selected_sub_category_id = cookies.get("selected_sub_category_id")
            selected_sub_category_name = cookies.get("selected_sub_category_name")
            sub_category_visibility = "hide_sub_categories"    
            header_path=header_path + "  ►  " + selected_sub_category_name
    return render_template('index.html', 
        main_categories=main_categories,
        main_category_visibility=main_category_visibility,
        selected_main_category_id=selected_main_category_id,
        sub_categories=sub_categories,
        sub_category_visibility=sub_category_visibility,
        selected_sub_category_id=selected_sub_category_id,
        header_path=header_path
        )

@app.route('/home', methods = ['GET', 'POST'])
def home():
    # clear variables
    main_categories.clear()
    sub_categories.clear()
    # redirect to index  
    res = make_response(redirect('/'))
    # delete all cookies
    res.set_cookie('selected_main_category_id', '', expires=0)
    res.set_cookie('selected_main_category_name', '', expires=0)
    res.set_cookie('selected_sub_category_id', '', expires=0)
    res.set_cookie('selected_sub_category_name', '', expires=0)
    return res

@app.route('/main_category', methods = ['POST'])
def main_category():
    selected_main_category_id = request.form['selected_main_category_id']
    selected_main_category_name = request.form['selected_main_category_name']
    # redirect to index   
    res = make_response(redirect('/'))
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

@app.route('/sub_category', methods = ['POST'])
def sub_category():
    selected_sub_category_id = request.form['selected_sub_category_id']
    selected_sub_category_name = request.form['selected_sub_category_name']
    # redirect to index   
    res = make_response(redirect('/'))
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
