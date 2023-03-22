from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

    user_logged_in = User.validate_login(request.form)

    if not user_logged_in:
        return redirect('/')

    session["user_id"] = user_logged_in.id
    session["user_name"] = user_logged_in.first_name
    
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():

    if "user_id" not in session:
        flash("Please login")
        return redirect('/')

    return render_template("dashboard.html", all_recipes = Recipe.get_all_recipes())


@app.route('/register',methods=['POST'])
def register():

    if not User.validate(request.form):
        return redirect('/')

    User.create(request.form)

    user_logged_in = User.validate_login(request.form)
    session["user_id"] = user_logged_in.id
    session["user_name"] = user_logged_in.first_name

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
