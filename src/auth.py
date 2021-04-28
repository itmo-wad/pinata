# import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user, current_user
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.pinata


login_manager = LoginManager()
login_manager.init_app(app)


# app.secret_key = os.urandom(16).hex()

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(username):
    user = db.users.find_one({'username': username})
    return User(username=user['username'], password=user['password'])


# @app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    # return redirect(url_for('cabinet'))
    # if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    if db.users.find_one({'username': username, 'password': password}):
        user = User(username=username, password=password)
        login_user(user)
        return redirect('/cabinet')
    else:
        return redirect('/invalid')


# return render_template('login.html')


# Add registration function to append new users on http://localhost:5000/register/
# @app.route('/register', methods=['GET', 'POST'])
#def register():
    # if request.method == 'POST':
    #username = request.form.get('username')
    #password = request.form.get('password')
    #if db.users.find_one({'username': username}):
        #return "Login is taken"
    #else:
        #db.users.insert({'username': username, 'password': password})
        #return redirect('/login')
    # return render_template('register.html')


# @app.route('/cabinet')
# @login_required
# def cabinet():
# return render_template('cabinet.html', username=current_user.username)


# @app.route('/logout')
# @login_required
# def logout():
# logout_user()
# return redirect('/')


# @app.route('/invalid')
# def invalid():
# return render_template('invalid.html')


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
