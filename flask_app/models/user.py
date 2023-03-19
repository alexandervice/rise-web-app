# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from datetime import date, datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# password with uppercase, lowercase, a number, and 8 characters
PASSWORD_REGEX = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
# PASSWORD_REGEX = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-:]).{8,}$"

def calculate_age(birth_date):
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        days_in_year = 365.2425
        today=date.today()
        age = int((today - birth_date).days / days_in_year )
        return age

class User:
    database = "ohana-rideshares"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birth_date = data['birth_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # all the posts a users has made
        self.posts = []
        # all the comments a user has made
        self.comments = []

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password , birth_date , created_at , updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , %(birth_date)s , NOW() , NOW() );"
        result = connectToMySQL(cls.database).query_db( query, data )
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.database).query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            "id": user_id
        }
        results = connectToMySQL(cls.database).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_user_age(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            "id": user_id
        }
        results = connectToMySQL(cls.database).query_db(query, data)
        user_age = calculate_age(cls(results[0]).birth_date)
        return user_age

        # class method to update our users in the database
    # UPDATE (CRUD)
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, birth_date = %(birth_date)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    # class method to delete our users in the database
    # DELETE (CRUD)
    @classmethod
    def delete(cls, user_id):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": user_id}
        results = connectToMySQL(cls.database).query_db(query, data)
        return results
    
    # Validations
    @classmethod
    def check_duplicates(cls, new_user):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.database).query_db(query)
        # Create an empty list to append our instances of users
        users = []
        is_valid = True
        for user in results:
            users.append( cls(user) )
            # if new_user['first_name'] == user["first_name"] and new_user['last_name'] == user["last_name"]:
            #     flash("That user is already in the system!", "duplicate")
            #     is_valid = False
            if new_user['email'] == user["email"]:
                flash("That email is already registered with a user!", "register")
                is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls, login_user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.database).query_db(query, login_user)
        # if there is no result
        if len(result) < 1:
            return False
        # if there is a result
        return cls(result[0])

    # Validations
    @staticmethod
    def validate_user(user ):
        is_valid = True
        # test whether a field matches the pattern
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        elif len(user['first_name']) > 45:
            flash("First Name must be less than 46 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        elif len(user['last_name']) > 45:
            flash("Last Name must be less than 46 characters.", "register")
            is_valid = False
        if len(user['birth_date']) < 1:
            flash("You must provide your birthdate.", "register")
            is_valid = False
        elif calculate_age(user['birth_date']) < 18:
            flash("You must be 18 or older to register an account.", "register")
            is_valid = False
        if len(user['email']) < 3:
            flash("Invalid email address.", "register")
            is_valid = False
        elif len(user['email']) > 255:
            flash("Invalid email address.", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        elif len(user['password']) > 255:
            flash("Password must be less than 256 characters.", "register")
            is_valid = False
        elif not re.match(PASSWORD_REGEX, user['password']):
            flash("Invalid Password.", "register")
            flash("Passwords must have a minimum of 8 characters, have at least one UPPERCASE letter, one lowercase letter, and one number [0-9]", "register")
            is_valid = False
        elif user['password'] != user['password_confirmation']:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid
