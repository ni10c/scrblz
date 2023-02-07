from flask_app.models.thread import thread
from pprint import pprint
from flask import render_template, request, redirect, session, flash
from flask_app.models.comment import comment
from flask_app import app

@app.route('/thread/postComment', methods=['POST'])
def createComment():
    if 'user_id' not in session:
        return redirect('/logout')
    if not comment.validate_comment(request.form):
        return redirect(request.referrer)
    comment.save(request.form)
    return redirect(request.referrer)

@app.route('/thread/comment/edit/<int:id>')
def editComment(id):
    # data = {
    #     "id":id
    # }
    if 'user_id' not in session:
        return redirect('/logout')
    comment_data=comment.get_one(id)
    if session['user_id'] != comment_data.user_id:
        return redirect(request.referrer)
    thread_id = comment_data.discussion_id
    thread_data = thread.get_one(thread_id)
    return render_template("editComment.html",comment=comment_data,thread=thread_data)

@app.route('/thread/comment/update', methods=['POST'])
def upateComment():
    if 'user_id' not in session:
        return redirect('/logout')
    if not comment.validate_comment(request.form):
        return redirect(request.referrer)
    comment.update(request.form)
    return redirect('/threads')

@app.route('/thread/comment/delete/<int:id>')
def deleteComment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    comment_data=comment.get_one(id)
    if session['user_id'] != comment_data.user_id:
        return redirect('/threads')
    comment.delete(id)
    return redirect(request.referrer)

# @app.route('/thread/comment/delete/<int:id>')
# def deleteComment(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     comment_data=comment.get_one(id)
#     if session['user_id'] != comment_data.user_id:
#         return redirect('/threads')
#     comment.delete(id)
#     return redirect('/threads')