from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
from flask_app import DATABASE, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_by_email(cls, email):
        data={
            "email" : email,
        }
        query = " SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            user= cls(results[0])
            return user
        else:
            return False

    @classmethod
    def create(cls, form):
        hashed_pw = bcrypt.generate_password_hash(form['password'])
        data= {
            **form,
            "password" : hashed_pw,
        }
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)
            """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def validate_login(cls, form):
        found_user = cls.get_one_by_email(form['email'])
        if found_user:
            if bcrypt.check_password_hash(found_user.password, form['password']):
                return found_user
            else:
                flash("Invalid login", 'invalid')
                return False
        else:
            flash("Invalid login", 'invalid')
            return False
            


    @classmethod
    def validate(cls, form):
        is_valid = True

        if len(form['first_name']) < 3:
            is_valid= False
            flash("First name must be at least 3 characters", 'error')
        if len(form['last_name']) < 3:
            is_valid= False
            flash("Last name must be at least 3 characters", 'error')
        if not EMAIL_REGEX.match(form['email']):
            is_valid=False
            flash("Invalid Email.", 'error')
        if cls.get_one_by_email(form['email']):
            is_valid=False
            flash("Email already registered.", 'error')
        if len(form['password']) < 8:
            is_valid= False
            flash("Password must be at least 8 characters", 'error')
        if form['password'] != form['confirmpass']:
            flash("Passwords do not match", 'error')
        return is_valid


    @classmethod
    def get_one_by_id(cls, id):
        data={
            "id" : id,
        }
        query = " SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            user= cls(results[0])
            return user
        else:
            return False

    
