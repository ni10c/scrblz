# import queue
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

UN_REGEX = re.compile(r'^[a-zA-Z0-9._-]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^[a-zA-Z0-9]')

class user:
    @staticmethod
    def validate_user_reg(user):
        is_valid = True
        if len(user['username']) == 0:
            flash("Userame Required.", 'reg_messages')
            is_valid = False
        elif len(user['username']) < 3:
            flash("Userame Must Be at Least 3 Characters.", 'reg_messages')
            is_valid = False
        if not UN_REGEX.match(user['username']): 
            flash("Valid Username Required.", 'reg_messages')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Valid Email Address Required.", 'reg_messages')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match.","reg_messages")
            is_valid = False
        if len(user['password']) == 0: 
            flash("Valid Password Required.", 'reg_messages')
            is_valid = False
        elif len(user['password']) < 8: 
            flash("Valid Password Required. Must Be at Least 8 Characters.", 'reg_messages')
            is_valid = False
        return is_valid
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.last_login = data['last_login']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s,%(email)s,%(password)s);"
        return connectToMySQL("producerSection").query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("producerSection").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def check_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("producerSection").query_db(query,data)
        is_available = True
        if len(result) > 0:
            return False
        return is_available

    @classmethod
    def login_success(cls, data):
        query = "UPDATE users SET last_login=CURRENT_TIMESTAMP() WHERE id = %(id)s;"
        return connectToMySQL('producerSection').query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('producerSection').query_db(query,data)