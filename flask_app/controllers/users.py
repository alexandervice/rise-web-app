from datetime import date, datetime
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.attribute import Ride
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/login_page')
def login_page():
    return render_template("login.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    data = {
    "first_name": request.form["first_name"],
    "last_name" : request.form["last_name"],
    "email" : request.form["email"],
    "password": request.form["password"],
    "password_confirmation" : request.form["password_confirmation"],
    "birth_date": request.form["birth_date"]
    }
    if not User.validate_user(data):
        print("user creation rejected: bad form entry")
        # we redirect to the template with the form.
        return redirect('/')
    if not User.check_duplicates(data):
        print("user creation rejected: duplicate")
        # we redirect to the template with the form.
        return redirect('/')
    # we will replace the password with this later
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    pw_confirm_hash = bcrypt.generate_password_hash(request.form["password_confirmation"])
    # We pass the data dictionary into the save method from the User class.
    data["password"] = pw_hash
    data["password_confirmation"] = pw_confirm_hash
    User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/login_page')
# NOTE never render_template on a POST route

@app.route('/login', methods=["POST"])
def login():
    data = {"email" : request.form["email"]}
    user_in_db = User.get_by_email(data)
    # if the user's email is not in the database
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the email is in the db, but the password does not match
    # user_in_db_password = [user_in_db.password:-user_in_db.salt]
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords match then we add the user_id in the session
    session['logged_in_user'] = {
        "user_id": user_in_db.id,
        "first_name": user_in_db.first_name,
        "is_logged_in": True
    }
    return redirect('/rides')

@app.route('/dashboard')
def dashboard_page():
    if "logged_in_user" not in session:
        return redirect('/')
    if session['logged_in_user']["is_logged_in"] == False:
        return redirect('/')
    user=User.get_one(session['logged_in_user'])
    age=User.get_user_age(session['logged_in_user'])
    return render_template("dashboard.html", user=user, age=age)

@app.route('/characters')
def all_characters():
    if "logged_in_user" not in session:
        return redirect('/')
    if session['logged_in_user']["is_logged_in"] == False:
        return redirect('/')
    user=User.get_one(session['logged_in_user'])
    characters=Character.get_all_characters()
    return render_template("characters_page.html", user=user, characters=characters)

@app.route('/logout')
def logout():
    print('logging out')
    session.pop("logged_in_user")
    return redirect('/')

# If we want to let users see each other
# @app.route('/users/<int:user_id>')
# def show(user_id):
#     # calling the get_one method and supplying it with the id of the user we want to get
#     user=User.get_one(user_id)
#     return render_template("show_user.html",user=user)

@app.route('/users/edit/<int:user_id>')
def edit(user_id):
    if "logged_in_user" not in session:
        return redirect('/')
    user=User.get_one(user_id)
    return render_template("edit_user.html",user=user)

@app.route('/users/update',methods=['POST'])
def update():
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password": request.form["password"],
        "password_confirmation" : request.form["password_confirmation"],
        "birth_date": request.form["birth_date"]
    }
    if not User.validate_user(data):
        print("user creation rejected: bad form entry")
        # we redirect to the template with the form.
        return redirect(f'/users/edit/{session["logged_in_user"]["user_id"]}')
    if not User.check_duplicates(data):
        print("user creation rejected: duplicate")
        # we redirect to the template with the form.
        return redirect(f'/users/edit/{session["logged_in_user"]["user_id"]}')
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    pw_confirm_hash = bcrypt.generate_password_hash(request.form["password_confirmation"])

    data["password"] = pw_hash
    data["password_confirmation"] = pw_confirm_hash
    User.update(data)
    return redirect('/dashboard')

# not currently working
# @app.route('/users/delete/<int:user_id>')
# def delete_user(user_id):
#     if "logged_in_user" not in session:
#         return redirect('/')
#     User.delete(user_id)
#     return redirect('/')