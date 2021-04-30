from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.pinata

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(username):
    user = db.users.find_one({'username': username})
    return User(username=user['username'], password=user['password'])


def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if db.users.find_one({'username': username}):
        l_user = db.users.find_one({'username': username})
        if check_password_hash(l_user['password'], password):
            user = User(username=username, password=password)
            login_user(user)
            return redirect('/cabinet')
        else:
            return "Wrong password"
    else:
        return "user are not registered"


def reg():
    username = request.form.get('username')
    password_1 = request.form.get('password1')
    password_2 = request.form.get('password2')
    if db.users.find_one({'username': username}):
        return "Login is taken"
    if password_1 != password_2:
        return "Passwords don't match!"
    if password_1 == "" or password_2 == "" or username == "":
        return "Not all fields are filled in!"
    else:
        password = generate_password_hash(password_1)
        db.users.insert({'username': username, 'password': password, 'photo': '', 'wishlists': "[]"})
        return redirect('/login')


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
