from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB ="character_sheet"
    
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def register(cls,user_data):
        data = {
            "first_name" : user_data["first_name"],
            "last_name" : user_data["last_name"],
            "email" : user_data["email"],
            "password" : bcrypt.generate_password_hash(user_data["password"])
        }
        query = "INSERT INTO users (first_name, last_name,email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        id = connectToMySQL(cls.DB).query_db(query,data)
        print("\n ___REGISTERED ID___ ->",id)
        return id
    
    @classmethod
    def get_by_email(cls,email):
        print("\n ____User get by email method____ ->", email)
        data = {"email" : email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) == 0:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,id):
        print("\n ____User get by id method____ ->", id)
        data = {"id" : id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) == 0:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        
        if not user["email"] or not EMAIL_REGEX.match(user["email"]):
            print("____User email FAILED____")
            flash("email isn't valid","login")
            is_valid = False
        else:
            user_in_db = User.get_by_email(user["email"])
            if user_in_db is False:
                flash("Wrong email or password","login")
                is_valid = False
            else:
                if len(user["password"]) <= 7 or not bcrypt.check_password_hash(user_in_db.password,user["password"]):
                    print("____User password FAILED____")
                    flash("Wrong email or password","login")
                    is_valid = False
            
        if is_valid:
            return user_in_db
        else:
            return is_valid
    
    
    @staticmethod
    def validate_register(user):
        print("")
        print("____Validate Registration____")
        print(user)
        is_valid =True
        user_in_db = User.get_by_email(user["email"])
        print("")
        print("____User in DB____", user_in_db)
        if not user["first_name"] or len(user["first_name"]) < 2 or not user["first_name"].isalpha():
            print("____User first name FAILED____")
            flash("first name must be at least 2 characters and only contain alpha characters","register")
            is_valid = False
        
        if not user["last_name"] or len(user["last_name"]) < 2 or not user["last_name"].isalpha():
            print("____User last name FAILED____")
            flash("last name must be at least 2 characters and only contain alpha characters","register")
            is_valid = False
        
        if not user["email"] or not EMAIL_REGEX.match(user["email"]): 
            print("____User email FAILED____")
            flash("email isn't valid","register")
            is_valid = False
            
        if user_in_db is not False:
            print("____User in db FAILED____")
            flash("user already exists","register")
            is_valid = False
            
        # if not re.search(r'^[A-Z]', user["password"]):
        #     print("____Password 1 capital letter FAILED____")
        #     flash("Password must contain 1 Capital letter","register")
        #     is_valid = False
            
        # if not re.search(r'^[0-9]', user["password"]):
        #     print("____Password 1 number FAILED____")
        #     flash("Password must contain 1 number","register")
        #     is_valid = False
        
        upper = False
        numeric = False
        for x in user['password']:
            if x.isupper():
                upper = True
            if x.isnumeric():
                numeric = True
        
        if not upper:
            print("____Upper case FAILED____")
            flash("Password must contain 1 Capital letter","register")
            is_valid = False
            
        if not numeric:
            print("____Numeric FAILED____")
            flash("Password must contain 1 number","register")
            is_valid = False
        
        if not user["password"] or len(user["password"]) <= 7:
            print("____User password length FAILED____")
            flash("password needs to be at least 8 characters","register")
            is_valid = False
            
        if not user["confirm_password"] or user["password"] != user["confirm_password"]:
            print("____User password match FAILED____")
            flash("Passwords do not match","register")
            is_valid = False
            
        return is_valid
    
