from flask import render_template, request, redirect, session, flash
from flask_app.models.user import user
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def home():
    session['user_id'] = 0
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not user.validate_user_reg(request.form):
        return redirect('/')
    if not user.check_email(request.form):
        flash("Email Already Registered.", 'reg_messages')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = user.save(data)
    print(user_id)
    flash("User Created. Please Login.", "created_messages")
    return redirect("/")

@app.route('/login/validate', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = user.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email", "login_messages")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password", "login_messages")
        return redirect('/')
    if 'user_id' not in session:
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.username
    session['user_email'] = user_in_db.email
    session['is_interested'] = False
    id = session['user_id']
    user.login_success(id)
    return redirect('/homepage')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/deleteUser/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if session['user_id'] != id:
        return redirect('/dashboard')
    data = {"id":id}
    user.destroy(data)
    flash("User Deleted")
    return redirect('/')

# @app.route('/deleteUser/<int:id>')
# def destroy(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     if session['user_id'] != user.id:
#         return redirect('/dashboard')
#     data = {"id":id}
#     user.destroy(data)
#     flash("User Deleted")
#     return redirect('/')