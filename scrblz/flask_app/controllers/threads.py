from pprint import pprint
from unittest import mock
from flask import render_template, request, redirect, session, flash
from flask_app.models.thread import thread
from flask_app.models.request import rqst
from flask_app.models.comment import comment
from flask_app import app

@app.route('/homepage')
def dashboard():
    if session['user_id'] == 0:
        return redirect('/logout')
    threads_data = thread.get_all()
    requests = rqst.get_all()
    print(threads_data)
    print(requests)
    return render_template("homepage.html",threadsList=threads_data,requests=requests)

@app.route('/threads')
def viewAllThreads():
    if 'user_id' not in session:
        return redirect('/logout')
    threads_data = thread.get_all()
    return render_template("viewAllThreads.html",threads=threads_data)

@app.route('/thread/new')
def newThread():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("addThread.html")

@app.route('/thread/create', methods=['POST'])
def createThread():
    if 'user_id' not in session:
        return redirect('/logout')
    if not thread.validate_thread(request.form):
        return redirect('/thread/new')
    thread.save(request.form)
    return redirect('/threads')

@app.route('/thread/view/<int:id>')
def viewThread(id):
    if 'user_id' not in session:
        return redirect('/logout')
    thread_data=thread.get_one(id)
    commentsList = comment.get_all(id)
    return render_template("viewThreadAll.html",thread=thread_data,comments = commentsList)

@app.route('/thread/edit/<int:id>')
def editThread(id):
    # data = {
    #     "id":id
    # }
    if 'user_id' not in session:
        return redirect('/logout')
    thread_data=thread.get_one(id)
    if session['user_id'] != thread_data.user_id:
        return redirect('/thread/view/<int:id>')
    return render_template("editThread.html",thread=thread_data)

@app.route('/thread/update', methods=['POST'])
def upateThread():
    if 'user_id' not in session:
        return redirect('/logout')
    if not thread.validate_thread(request.form):
        return redirect(request.referrer)
    thread.update(request.form)
    return redirect('/threads')

@app.route('/thread/delete/<int:id>')
def deleteThread(id):
    if 'user_id' not in session:
        return redirect('/logout')
    thread_data=thread.get_one(id)
    if session['user_id'] != thread_data.user_id:
        return redirect('/threads')
    thread.delete(id)
    return redirect('/threads')