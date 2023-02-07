from pprint import pprint
from flask_app.models.user import user
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class thread:
    @staticmethod
    def validate_thread(thread):
        is_valid = True
        if len(thread['topic']) == 0:
            flash("Topic Required.",'thread_messages')
            is_valid = False
        elif len(thread['topic']) < 3:
            flash("Valid Topic Required. Must Be at Least 3 Characters.", 'thread_messages')
            is_valid = False
        if len(thread['description']) == 0:
            flash("Description Required.",'thread_messages')
            is_valid = False
        elif len(thread['description']) < 10:
            is_valid = False
        if not thread['description']:
            flash("Valid Description Required.", 'thread_messages')
            is_valid = False
        return is_valid
    def __init__(self, data):
        self.id = data['id']
        self.topic = data['topic']
        self.description = data['description']
        self.link = data['link']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.user_id = data['user_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO discussions (topic,description,link,user_id) VALUES (%(topic)s,%(description)s,%(link)s,%(user_id)s);"
        return connectToMySQL('producerSection').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE discussions SET topic=%(topic)s,description=%(description)s,link=%(link)s,updated_at=CURRENT_TIMESTAMP() WHERE id = %(id)s;"
        result = connectToMySQL('producerSection').query_db(query,data)
        return result

    @classmethod
    def postComment(cls,data):
        query = "INSERT INTO comments (comment,user_id,discussion_id) VALUES (%(comment)s,%(user_id)s,%(discussion_id)s)"
        result = connectToMySQL('producerSection').query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM discussions JOIN users ON discussions.user_id = users.id;"
        results = connectToMySQL('producerSection').query_db(query)
        pprint(results, sort_dicts=False)
        threads = []
        for row in results:
            list = cls(row)
            thread_data = {
                'id': row['id'],
                'topic': row['topic'],
                'description': row['description'],
                'link': row['link'],
                'status': row['status'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id']
            }
            list.thread = thread(thread_data)
            user_data = {
                'id': row['users.id'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'last_login': row['last_login']
            }
            list.user = user(user_data)
            threads.append(list)
        return threads

    @classmethod
    def get_one(cls,id):
        query = f"SELECT * FROM discussions LEFT JOIN users ON discussions.user_id = users.id WHERE discussions.id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        pprint(results, sort_dicts=False)
        tdata = []
        for row in results:
            list = cls(row)
            thread_data = {
                'id': row['id'],
                'topic': row['topic'],
                'description': row['description'],
                'link': row['link'],
                'status': row['status'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id']
            }
            list.thread = thread(thread_data)
            user_data = {
                'id': row['users.id'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'last_login': row['last_login']
            }
            list.user = user(user_data)
            tdata.append(list)
        return tdata[0]

    # @classmethod
    # def get_one(cls,id):
    #     query = f"SELECT * FROM discussions LEFT JOIN users ON discussions.user_id = users.id WHERE discussions.id = {id};"
    #     results = connectToMySQL('producerSection').query_db(query)
    #     pprint(results, sort_dicts=False)
    #     thread = []
    #     for row in results:
    #         list = cls(row)
    #         thread_data = {
    #             'id': row['id'],
    #             'topic': row['topic'],
    #             'description': row['description'],
    #             'link': row['link'],
    #             'status': row['status'],
    #             'created_at': row['created_at'],
    #             'updated_at': row['updated_at'],
    #             'user_id': row['user_id']
    #         }
    #         list.thread = thread(thread_data)
    #         user_data = {
    #             'id': row['users.id'],
    #             'username': row['username'],
    #             'email': row['email'],
    #             'password': row['password'],
    #             'created_at': row['users.created_at'],
    #             'last_login': row['last_login']
    #         }
    #         list.user = user(user_data)
    #         thread.append(list)
    #     return thread

    @classmethod
    def delete(cls,id):
        query = f"DELETE FROM discussions WHERE id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        return results

    @classmethod
    def deleteComment(cls,id):
        query = f"DELETE FROM comments WHERE id = {id};"
        results = connectToMySQL('producerSection').query_db(query)
        return results