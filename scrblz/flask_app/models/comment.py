from pprint import pprint
from flask_app.models.user import user
from flask_app.models.thread import thread
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class comment:
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['content']) == 0:
            flash("Comment Required.",'comment_messages')
            is_valid = False
        elif len(comment['content']) < 3:
            flash("Valid comment Required. Must Be at Least 3 Characters.", 'comment_messages')
            is_valid = False
        return is_valid
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.user_id = data['user_id']
        self.discussion_id = data['discussion_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO comments (content,user_id,discussion_id) VALUES (%(content)s,%(user_id)s,%(discussion_id)s);"
        return connectToMySQL('producerSection').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE comments SET content=%(content)s,updated_at=CURRENT_TIMESTAMP() WHERE comments.id = %(id)s;"
        result = connectToMySQL('producerSection').query_db(query,data)
        return result

    @classmethod
    def get_all(cls,id):
        query = f"SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id WHERE discussion_id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        pprint(results, sort_dicts=False)
        comments = []
        for row in results:
            list = cls(row)
            comment_data = {
                'id': row['id'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id'],
                'discussion_id': row['discussion_id']
            }
            list.comment = comment(comment_data)
            user_data = {
                'id': row['users.id'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'last_login': row['last_login']
            }
            list.user = user(user_data)
            comments.append(list)
        return comments

    @classmethod
    def get_one(cls,id):
        query = f"SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id WHERE comments.id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        pprint(results, sort_dicts=False)
        theComment = []
        for row in results:
            result = cls(row)
            comment_data = {
                'id': row['id'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id'],
                'discussion_id': row['discussion_id']
            }
            result.cmmnt = comment(comment_data)
            user_data = {
                'id': row['users.id'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'last_login': row['last_login']
            }
            result.user = user(user_data)
            theComment.append(result)
        return theComment[0]

    @classmethod
    def delete(cls,id):
        query = f"DELETE FROM comments WHERE id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        return results