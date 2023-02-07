from pprint import pprint
from flask_app.models.user import user
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class interestedUser:
    def __init__(self, data):
        self.req = data['req']
        self.user_id = data['user_id']

    @classmethod
    def interested(cls,data):
        query = "INSERT INTO interested_users (req,user_id) VALUES (%(req)s,%(user_id)s)"
        result = connectToMySQL('producerSection').query_db(query,data)
        return result

    @classmethod
    def get_all(cls,id):
        query = f"SELECT * FROM interested_users JOIN users ON interested_users.user_id = users.id WHERE req = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        pprint(results, sort_dicts=False)
        interested = []
        for row in results:
            list = cls(row)
            intrstd = {
                'req': row['req'],
                'user_id': row['user_id']
            }
            list.interest = interestedUser(intrstd)
            user_data = {
                'id': row['id'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'last_login': row['last_login']
            }
            list.user = user(user_data)
            interested.append(list)
        return interested

    @classmethod
    def delete(cls,id):
        query = f"DELETE FROM requests WHERE discussion_id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        return results