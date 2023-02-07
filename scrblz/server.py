from flask_app.controllers import users, requests, comments, threads
from flask_app import app

if __name__ == '__main__':
    app.run(debug=True)