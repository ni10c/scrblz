from pprint import pprint
from flask import render_template, request, redirect, session, flash
from flask_app.models.request import rqst
from flask_app.models.interestedUser import interestedUser
from flask_app import app

@app.route('/requests')
def viewAllRequests():
    if 'user_id' not in session:
        return redirect('/logout')
    requests = rqst.get_all()
    return render_template("viewAllRequests.html",requests=requests)

@app.route('/request/new')
def newRequest():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("addRequest.html")

@app.route('/request/create', methods=['POST'])
def createRequest():
    if 'user_id' not in session:
        return redirect('/logout')
    if not rqst.validate_request(request.form):
        return redirect('/request/new')
    rqst.save(request.form)
    return redirect('/requests')

@app.route('/request/view/<int:id>')
def viewRequest(id):
    if 'user_id' not in session:
        return redirect('/logout')
    interested_data = interestedUser.get_all(id)
    return render_template("viewRequest.html",request=rqst.get_one(id),interested=interested_data)

@app.route('/request/interested', methods=['POST'])
def interested():
    if 'user_id' not in session:
        return redirect('/logout')
    interestedUser.interested(request.form)
    return redirect('/requests')

@app.route('/request/edit/<int:id>')
def editRequest(id):
    # data = {
    #     "id":id
    # }
    if 'user_id' not in session:
        return redirect('/logout')
    request_data=rqst.get_one(id)
    if session['user_id'] != request_data.user_id:
        return redirect('/thread/view/<int:id>')
    interested_data = interestedUser.get_all(id)
    return render_template("editRequest.html",request=request_data,interested=interested_data)

@app.route('/request/update', methods=['POST'])
def upateRequest():
    if 'user_id' not in session:
        return redirect('/logout')
    if not rqst.validate_request(request.form):
        return redirect('/thread/view/<int:id>')
    rqst.update(request.form)
    return redirect('/requests')

@app.route('/request/close/<int:id>', methods=['POST'])
def closeRequest(id):
    if 'user_id' not in session:
        return redirect('/logout')
    request_data=rqst.get_one(id)
    if session['user_id'] != request_data.user_id:
        return redirect('/threads')
    rqst.closeRequest(id)
    return redirect('/requests')

@app.route('/request/delete/<int:id>')
def deleteRequest(id):
    if 'user_id' not in session:
        return redirect('/logout')
    request_data=rqst.get_one(id)
    if session['user_id'] != request_data.user_id:
        return redirect('/threads')
    rqst.delete(id)
    interestedUser.delete(id)
    return redirect('/requests')