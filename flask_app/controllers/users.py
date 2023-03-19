from datetime import date, datetime
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.ride import Ride
from flask_bcrypt import Bcrypt
# import bcrypt as salty
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

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
        # session["old_form"] = data
        # we redirect to the template with the form.
        return redirect('/')
    if not User.check_duplicates(data):
        print("user creation rejected: duplicate")
        # session["old_form"] = data
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
    return redirect('/')
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
def dashboard():
    if "logged_in_user" not in session:
        return redirect('/')
    if session['logged_in_user']["is_logged_in"] == False:
        return redirect('/')
    user=User.get_one(session['logged_in_user']["user_id"])
    age=User.get_user_age(session['logged_in_user']["user_id"])
    return render_template("dashboard.html", user=user, age=age)

@app.route('/rides')
def all_rides():
    if "logged_in_user" not in session:
        return redirect('/')
    if session['logged_in_user']["is_logged_in"] == False:
        return redirect('/')
    user=User.get_one(session['logged_in_user']["user_id"])
    rides=Ride.get_all_rides_with_rider_and_driver()
    return render_template("ride_page.html", user=user, rides=rides)

@app.route('/logout')
def logout():
    print('logging out')
    session.pop("logged_in_user")
    return redirect('/')

# @app.route('/add_new')
# def add():
#     return render_template("create_user.html")

# @app.route('/users/<int:user_id>')
# def show(user_id):
#     # calling the get_one method and supplying it with the id of the user we want to get
#     user=User.get_one(user_id)
#     return render_template("show_user.html",user=user)

# @app.route('/users/edit/<int:user_id>')
# def edit(user_id):
#     user=User.get_one(user_id)
#     return render_template("edit_user.html",user=user)

# @app.route('/users/update',methods=['POST'])
# def update():
#     data = {
#         "first_name": request.form["first_name"],
#         "last_name" : request.form["last_name"],
#         "email" : request.form["email"]
#     }
#     if not User.validate_user(data):
#         print("user creation rejected: bad form entry")
#         # session["old_form"] = data
#         # we redirect to the template with the form.
#         return redirect('/add_new')
#     if not User.check_duplicates(data):
#         print("user creation rejected: duplicate")
#         # session["old_form"] = data
#         # we redirect to the template with the form.
#         return redirect('/add_new')
#     User.update(request.form)
#     return redirect('/')

# @app.route('/users/delete/<int:user_id>')
# def delete_user(user_id):
#     User.delete(user_id)
#     return redirect('/')